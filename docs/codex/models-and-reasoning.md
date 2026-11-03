# Модели и reasoning: выбор и применимость

Source status: `official + experiment`

Проверено 2026-11-03. Источники: [API model catalog](https://developers.openai.com/api/docs/models), [модели Codex и ChatGPT Work](https://learn.chatgpt.com/docs/models), [migration guide](https://developers.openai.com/api/docs/guides/latest-model). Это справочник и кандидатная политика Product-Agent OS, а не переключение моделей или результат benchmark.

## Матрица API-моделей

| Model ID / источник | API reasoning.effort | Кандидатная область применения в проекте | Tools |
| --- | --- | --- | --- |
| [gpt-6-astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | `low`, `medium`, `high`, `xhigh`, `max`; без `none` | Наиболее сложная архитектура, исследования и неоднозначные решения | Tool calling через Responses |
| [gpt-6.1-sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | `low`, `medium` (API default), `high`, `xhigh`, `max` | Кандидат для сложной разработки и длительных инженерных задач | Tool calling через Responses |
| [gpt-6.1-terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | `none`, `low`, `medium` (API default), `high`, `xhigh`, `max` | Документы, визуальные задачи, computer use; не автоматическая замена прежних builder-ролей | Tool calling через Responses |
| [gpt-6-luna](https://developers.openai.com/api/docs/models/gpt-6-luna) | `none`, `low`, `medium` (API default), `high`, `xhigh`, `max` | Узкие повторяемые задачи после ограниченного eval | Responses; Chat Completions function calling только при `none` |

Кандидатные роли — интерпретация официального позиционирования для проекта. Их качество здесь не измерено. Модельные страницы перечисляют endpoints, но не доказывают поддержку любой комбинации endpoint/effort/tool. Применяйте [матрицу API-совместимости](../agent-systems/sdk-patterns.md).

## Поверхность, авторизация и версия

| Поверхность | Условия | Что проверить до выбора |
| --- | --- | --- |
| OpenAI API / API-key session | Доступность модели и параметры соответствующего API | Account access, model ID, endpoint, service tier, бюджет |
| Codex App / CLI / IDE с ChatGPT sign-in | Plan, workspace policy, версия клиента и rollout | Доступный picker/каталог и effective configuration |
| GPT-6.1 Terra в CLI | Официальный minimum: CLI 0.159.0 | Версию именно используемого клиента; версия CLI не доказывает версию App |
| ChatGPT Work | Продуктовые режимы и доступность плана | Значения UI и поддержку выбранной моделью |

Доступность конкретному аккаунту в этом обновлении не проверялась. Для остальных строк здесь не заявляется неподтвержденная минимальная версия. `Light` соответствует `low` в указанном продуктовом контексте. `Max` усиливает single-agent reasoning; `Ultra` использует subagents в поддерживаемых продуктах. Luna не поддерживает Ultra. Не передавайте UI `Ultra` как обычный API `reasoning.effort`; API-значения определяются модельной страницей.

## Контекст и стоимость

На дату проверки все четыре API model pages указывают context window 1 050 000, max input 922 000 и max output 128 000 tokens. Эти ограничения проверяются совместно, а не складываются как независимые квоты. Для GPT-6.1 Sol официальный default context в Codex — 500 000 tokens; API-лимит нельзя автоматически переносить в клиент.

Стоимость зависит от модели, service tier, cache reads/writes и условий длинного контекста. Не переносите тариф или surcharge одной модели на остальные. Используйте датированную модельную страницу и [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching); подписка Codex/ChatGPT не является API-тарифом. Метод учета — в [evals](../agent-systems/evals-observability.md).

## Retirement и исторические результаты

GPT-5.5 выведена из Codex с ChatGPT sign-in 14 октября 2026 в 19:00 UTC; это не распространяется на API/API-key Codex sessions. GPT-5.4 и GPT-5.4-mini выведены из sign-in Codex 31 августа 2026. Проверяйте [retirement guidance](https://learn.chatgpt.com/docs/models) для выбранной поверхности. Здесь не утверждается, что GPT-5.6 удалена из API.

Исторические pins, approvals, frozen fixtures и eval results сохраняют исходные model ID и даты. Переписывание старого результата на новую модель разрушает доказательство.

## Действующее состояние Product-Agent OS

| Слой | Состояние на 2026-11-03 | Граница утверждения |
| --- | --- | --- |
| Активные 15 профилей | 13 GPT-6.1 Sol, 2 GPT-6.1 Terra; generic subagent — Sol medium | Pins обновлены; effort сохранён; активация и качество ещё не подтверждены |
| 8 packaged profiles и обе model-reasoning-policy templates | 6 Sol, 2 Terra; единая политика GPT-6 | Предложения для целевых проектов, без активации |
| GPT-6 Astra / Luna | Кандидаты для отдельного сравнения | Не назначены профилям |
| Validator/model allowlist и permissions/MCP | Согласованы с родительским наследованием | Локальные проверки не доказывают эффективные настройки новой сессии |

Исполняемая конфигурация владеет pins; этот справочник — применимостью и источниками; [playbook](../playbooks/model-migration.md) — процедурой сравнения. [Compatibility](../product-agent-os/codex-compatibility.md) содержит техническую очередь. Присутствие модели в каталоге, синтаксически корректный TOML и успешный docs build не доказывают качество, доступность аккаунту или активацию.
