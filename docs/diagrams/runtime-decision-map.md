# Runtime Decision Map

Source status: `official + experiment`

Эта диаграмма помогает выбрать, где запускать задачу Codex: в App, CLI, Cloud, non-interactive mode, MCP, GitHub Action или scheduled automation.

## Диаграмма

```mermaid
flowchart TD
    A["New task"] --> B{"Needs close human steering?"}
    B -->|Yes| C["Codex App / IDE"]
    B -->|No| D{"Runs из terminal contract?"}
    D -->|Yes| E["Codex CLI"]
    D -->|No| F{"Needs repeatable non-interactive execution?"}
    F -->|Yes| G["codex exec"]
    F -->|No| H{"Needs orchestration из agent app?"}
    H -->|Yes| I["Codex MCP"]
    H -->|No| J{"Triggered через PR или CI?"}
    J -->|Yes| K["GitHub Action"]
    J -->|No| L{"Runs на schedule?"}
    L -->|Yes| M["Codex automation"]
    L -->|No| N["Manual playbook run"]

    C --> O["Используйте для ambiguous product work"]
    E --> P["Используйте для local repo tasks"]
    G --> Q["Используйте для scripted jobs и eval loops"]
    I --> R["Используйте как execution backend для Agents SDK"]
    K --> S["Используйте для review, CI, release checks"]
    M --> T["Используйте только после workflow является stable"]
```

## Как применять

Выбирайте runtime по уровню неопределенности и цене ошибки.

| Поверхность | Когда использовать | Что проверить |
| --- | --- | --- |
| Codex App / IDE | Нужно много steering, review, уточнений | Видны ли файлы, diff и результаты команд |
| CLI | Локальная инженерная задача с понятным scope | Есть ли команды проверки и sandbox policy |
| `codex exec` | Non-interactive job, повторяемый eval, batch update | Prompt должен быть самодостаточным |
| Codex MCP | Agent app должна делегировать работу Codex | Нужны границы tools, logs и approvals |
| GitHub Action | PR review, разбор CI и проверки release | Нужны permissions и предсказуемый output. |
| Automation | Регулярная задача с устойчивым workflow | Нужны skill, schedule и failure policy. |

## Правило выбора

Если задачу трудно описать как контракт, оставляйте ее в App/IDE. Если задачу можно описать как стабильный контракт с входами, выходами и проверкой, переносите ее в CLI, `codex exec`, MCP или automation.

## Антипаттерны

- Запускать scheduled automation до появления eval criteria.
- Использовать MCP как обходной путь вокруг неясного prompt contract.
- Отправлять в non-interactive mode задачу, где нужен product judgment.
- Делать GitHub Action, которая пишет большие изменения без review gate.
