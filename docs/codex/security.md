# Безопасность, sandbox и approvals

Source status: `official`  
Источники: [Sandbox](https://developers.openai.com/codex/concepts/sandboxing), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex cloud](https://developers.openai.com/codex/cloud).

## Базовая модель

Sandbox - это техническая граница: какие файлы Codex может изменять, какие команды запускать и есть ли доступ к сети. Approval policy - управленческая граница: когда Codex должен остановиться и спросить разрешение.

Для локальной работы безопасный baseline:

```text
sandbox_mode = "workspace-write"
approval_policy = "on-request"
approvals_reviewer = "user"
```

Такой режим позволяет работать внутри workspace, но требует approval для действий за пределами границы, сетевых команд или иных чувствительных операций.

## Режимы sandbox

| Mode | Смысл | Использовать |
| --- | --- | --- |
| `read-only` | Codex может читать, но не должен менять файлы или выполнять существенные команды без разрешения | Планирование, review, аудит |
| `workspace-write` | Codex может читать, менять workspace и запускать routine commands в границах проекта | Большинство локальных задач |
| `danger-full-access` | Codex работает без sandbox-ограничений | Только осознанно и кратковременно |

## Network access

По официальной модели Codex по умолчанию не должен свободно ходить в сеть во время агентной работы. В cloud setup network может быть доступен на этапе подготовки окружения, а agent phase обычно требует отдельного решения по internet access.

Практическое правило:

- документацию можно сверять через официальные источники;
- install и package manager команды требуют явного понимания, что будет загружено;
- secrets не должны попадать в prompts, docs, memory или artifacts.

## Approval checklist

Перед approval спросите:

- Команда пишет за пределы workspace?
- Команда использует сеть?
- Команда может удалить, переписать или отправить данные?
- Есть ли менее широкий способ дать доступ?
- Можно ли заменить broad access на command prefix rule?

