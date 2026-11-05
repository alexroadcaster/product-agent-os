# Безопасность, permissions и approvals

Source status: `official + experiment`

Проверено 2026-11-03: [Permissions](https://learn.chatgpt.com/docs/permissions), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference).

Sandbox и permissions технически ограничивают выполнение локальных команд. Approval policy управляет допустимыми запросами подтверждения. Описание роли, документ или skill не выдают привилегий. В этом проекте внешние записи, provider/model calls, browser, Git и изменение активации требуют отдельного разрешения.

## Выбрать одну схему конфигурации

Permission profiles имеют beta-статус. Используйте либо `default_permissions` / `[permissions]`, либо legacy `sandbox_mode` / `[sandbox_workspace_write]`, без смешивания. Проверяйте все effective layers и managed policy; примеры — в [конфигурации](configuration.md). `:workspace` защищает `.git`, `.agents`, `.codex`, `.aws`: разрешенная запись в каталог проекта не означает запись в любой дочерний путь. Legacy `read-only`, `workspace-write` и `danger-full-access` — разные режимы; последний снимает локальные sandbox-ограничения и не служит способом обхода неудобных approvals.

Custom agents наследуют permissions и approvals родителя. Инструкция reviewer не редактировать файлы задает поведение, а не отдельный технический read-only sandbox. Agent-local sandbox/MCP settings не переопределяют родителя. Реальная изоляция требует применимых механизмов исполнения и доказательств из свежей сессии.

## Сеть и поверхности инструментов

| Поверхность | Механизм контроля | Какой вывод недопустим |
| --- | --- | --- |
| Локальные команды | Effective filesystem/network policy и command sandbox | Writable workspace не означает доступ к сети |
| Фильтрация адресатов команд | Активный network proxy и domain rules | Одного `network.enabled = true` недостаточно для фильтрации |
| Web search | Product/tool policy | Command proxy allowlist не управляет этим поиском |
| MCP | Конфигурация родителя, tool/server policy и approvals | Декларация не доказывает подключение или успешный вызов |
| Apps/connectors | Авторизация и approvals приложения/инструмента | Command network policy не является политикой connector |
| Browser/computer tools | Собственные controls и разрешенный scope задачи | Command sandbox не обеспечивает универсальную изоляцию browser |

Domain rules требуют `features.network_proxy = true` или включенного managed proxy. Активный proxy без allow entries блокирует запросы доменов; deny имеет приоритет. Local, cloud setup и cloud agent phase имеют разные сетевые controls: проверяйте выбранную поверхность, не предполагая универсальный default.

## Approval и данные

Перед чувствительным действием определите адресата, данные, side effects, уже имеющееся разрешение и минимальные необходимые права. Чтение публичной документации отличается от установки зависимостей или provider operation. Не помещайте secrets и лишние private data в prompts, docs, memory или evidence. `approvals_reviewer` не расширяет sandbox и не проверяет повторно уже разрешенные действия.

## Граница проверки

Разбор конфигурации не доказывает effective runtime policy. Для заявления об активации нужны client/version/auth, загруженная конфигурация, permissions родителя, выбранный инструмент и наблюдаемое permitted/denied поведение. Обновление документации не меняет permissions; открытые контракты проекта перечислены в [Codex compatibility](../product-agent-os/codex-compatibility.md).

## Cloud и hooks

Network secrets current Cloud и direct variables имеют разные способы доставки; legacy setup-only правило не универсально. См. [Cloud setup](surfaces.md) и [hook trust/failure boundaries](../runtime/worktrees-hooks-rules.md). Проверяйте execution и orchestration отдельно.
