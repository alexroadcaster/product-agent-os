# Цикл context, memory и verification

Source status: `official + experiment`

Эта диаграмма объясняет, как собирать context, memory и verification loop так, чтобы уменьшить hallucinations в проектной агентной работе.

## Диаграмма

```mermaid
flowchart TD
    A["Official sources"] --> D["Context packet"]
    B["Project files"] --> D
    C["RUNLOG.md session facts"] --> D
    E["AGENTS.md durable rules"] --> D
    F["Community insights"] --> G{"Verified?"}
    G -->|Yes| D
    G -->|No| H["insights layer only"]
    D --> I["Prompt contract"]
    I --> J["Agent / model output"]
    J --> K["Structured answer или diff"]
    K --> L["Verifier"]
    L --> M{"Result"}
    M -->|Supported| N["Accept и cite"]
    M -->|Missing context| O["Retrieve more или ask"]
    M -->|Conflict| P["Escalate source conflict"]
    M -->|Unsupported| Q["Reject или mark needs_source"]
    N --> R["Update RUNLOG.md"]
    O --> R
    P --> R
    Q --> R
    R --> S["Update AGENTS.md или skill только если durable"]
```

## Как применять

Перед тем как агент отвечает, пишет код или меняет документацию, сформируйте context packet:

```text
Goal:
  Что должно измениться.

Sources:
  Official docs, repo files, source IDs, checked_at.

Constraints:
  Что запрещено, какие approvals нужны, какие claims нельзя делать.

Memory:
  Только релевантные решения из RUNLOG.md и durable rules из AGENTS.md.

Output contract:
  Формат результата, citations, verification evidence.

Verification:
  Команды, eval rubric, reviewer role, stop conditions.
```

## Разделение памяти

| Слой | Что хранит | Когда обновлять |
| --- | --- | --- |
| `AGENTS.md` | Постоянные правила проекта | После повторяющегося решения |
| `RUNLOG.md` | Ход конкретной сессии | После важных действий и failures |
| `EVALS.md` | Quality rubric и score history | После eval loop |
| `docs/insights` | Community tricks и hypotheses | До официальной проверки |
| Skill instructions | Повторяемый метод | После ручных прогонов и eval cases |

## Антигаллюцинационный baseline

- Каждый factual claim должен иметь source, file reference или статус assumption.
- Community insight не становится правилом без verification status.
- Если context недостаточен, агент должен запросить недостающий input или пометить claim как unsupported.
- LLM-as-judge не заменяет deterministic checks.
- Session summary не заменяет source registry и `RUNLOG.md`.

## Полномочия и переходы контекста

Граф показывает маршрутизацию evidence, а не приоритет инструкций. Текущий source проекта отвечает на вопросы реализации, текущие официальные docs — внешней платформы. Полномочия имеют только применимые загруженные инструкции; обычные Markdown, memory и generated views их не получают. Discovery и scope AGENTS — в [context engineering](../prompting/context-engineering.md).

При уточнении пользователя сохраняйте задачу и ограничения до выбора steering, summary, compaction или новой сессии. Их state contracts различаются. `configuration_update` нельзя совмещать с automatic compaction/truncation; explicit compaction требует повторного задания измененных settings. До выбора маршрута читайте [session control](../agent-systems/session-control.md). Диаграмма не доказывает загрузку инструкций, сохранение state или runtime activation.
