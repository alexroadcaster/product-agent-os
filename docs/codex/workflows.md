# Рабочие процессы Codex

Source status: `official`  
Источники: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Prompting](https://developers.openai.com/codex/prompting).

## Структура хорошей задачи

Codex работает лучше, когда получает явный контекст и definition of done. Минимальный task packet:

```text
Goal:
Context:
Constraints:
Allowed changes:
Out of scope:
Verification:
Expected output:
```

## Use cases как каталог workflow

Официальный раздел [Codex use cases](https://developers.openai.com/codex/use-cases) следует читать как практическую карту повторяемых задач: каждая карточка задает outcome, audience, starter prompt, skills/plugins, constraints, verification и related workflows.

Для проектной работы используйте [Deep analysis of Codex use cases](use-cases-deep-analysis.md):

- выберите ближайший official archetype;
- перенесите его inputs, constraints и verification в task packet;
- запустите workflow вручную;
- только после успешного runlog превращайте его в skill;
- если workflow нужен нескольким проектам или требует bundle из skills, MCP и app integrations, оформляйте plugin.

## Workflow: разобраться в кодовой базе

Используйте для onboarding, анализа сервиса, протокола или request flow.

```text
Изучи выбранный модуль и верни:
- краткую карту ответственности файлов;
- request/data flow по шагам;
- где данные валидируются;
- 2-3 риска при изменениях;
- список файлов, которые нужно читать дальше.
Не меняй файлы.
```

Verification:

- запросить numbered flow;
- сверить упомянутые файлы;
- проверить, что Codex не выдумал несуществующие entrypoints.

## Workflow: исправить баг

Для bugfix сначала нужен reproducible symptom.

```text
Bug:
Repro steps:
Expected:
Actual:
Suspected files:
Constraints:
Verification command:
```

Если reproduction не указан, первая задача Codex - найти или предложить минимальный воспроизводимый сценарий, а не сразу менять код.

## Workflow: обновить документацию

```text
Сравни официальные источники с текущими docs.
Не меняй утверждения без ссылки на source registry.
Верни:
- устаревшие утверждения;
- новые факты;
- proposed edits;
- verification checklist.
```

Этот workflow превращен в отдельный [playbook](../playbooks/docs-update.md).

## Минимальный достаточный процесс

Обычная задача: scope → изменение → affected checks → результат/ограничения. Для material multi-step work используйте [полный lifecycle](../product-agent/lifecycle.md). Команда, worktree и новый набор artifacts не обязательны. Повторение проверенного метода — отдельный [Scheduled tasks](../runtime/automations-github.md) route.
