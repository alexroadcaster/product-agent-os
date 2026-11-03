# Поверхности работы Codex

Source status: `official`  
Источники: [Codex app](https://developers.openai.com/codex/app), [Codex CLI](https://developers.openai.com/codex/cli), [Codex IDE extension](https://developers.openai.com/codex/ide), [Codex cloud](https://developers.openai.com/codex/cloud).

## Выбор поверхности

| Поверхность | Когда использовать | Сильная сторона | Риск |
| --- | --- | --- | --- |
| Codex App | Несколько потоков, review, worktrees, automations, artifacts | Командный центр для параллельной работы | Требует дисциплины в управлении ветками и approvals |
| CLI | Локальная работа из терминала, воспроизводимые команды, transcript | Явный контекст, контроль команд, удобство для power users | Нужно явно указывать файлы и границы |
| IDE extension | Работа рядом с редактором, open files, selections, `@file` | Быстрый контекст кода и follow-up по месту | Легко полагаться на неполный editor context |
| Codex cloud | Длинные фоновые задачи, PR, GitHub-linked work | Параллельность и изоляция от локальной машины | Нужно заранее описывать setup, network и secrets |

## Codex App

Официальная документация описывает Codex App как desktop command center для параллельных Codex threads, built-in worktree support, automations и Git functionality. Для продвинутого пользователя это основная поверхность для управления несколькими независимыми задачами.

Операционная инструкция:

- каждый thread должен иметь конкретный outcome;
- для write-heavy задач включайте worktree isolation;
- для повторяющихся проверок используйте automations;
- перед принятием результата смотрите diff, команды проверки и artifacts.

## CLI

Codex CLI запускается локально из терминала и может читать, менять и запускать код в выбранной директории. Это лучший режим для воспроизводимых workflow, потому что команды, approvals и контекст проще держать явными.

Шаблон CLI-задачи:

```text
Цель: ...
Контекст: @path/to/file.md @path/to/schema.json
Ограничения: не менять публичный API, не устанавливать зависимости без approval.
Definition of done: ...
Verification: запусти ...
```

## IDE extension

IDE extension полезен, когда важен editor context: открытые файлы, выделения, `@file` references, follow-up по cloud work. Для сложных задач фиксируйте контекст письменно, потому что open files не заменяют requirements.

## Codex cloud

Cloud подходит для фоновых задач, особенно когда работа может идти независимо от текущей локальной сессии. Для cloud-задач отдельно фиксируйте:

- repository и branch;
- setup steps;
- internet access policy;
- secrets availability only where needed;
- expected PR or artifact.

## Модели и границы поверхности

Версия CLI не доказывает версию Codex App или IDE extension. API-key и ChatGPT sign-in могут иметь разные availability/retirement условия. Сопоставляйте client/auth/model/effort по [единому справочнику](models-and-reasoning.md); account availability и runtime activation требуют собственного evidence.
