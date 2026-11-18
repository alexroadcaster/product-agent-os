# Модели и reasoning: выбор и применимость

Source status: `official + experiment`

Проверено 2026-11-18. Источники: [модели Codex и ChatGPT Work](https://learn.chatgpt.com/docs/models), [Prompting GPT‑6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra), [API model catalog](https://developers.openai.com/api/docs/models) и [Using GPT‑6.2](https://developers.openai.com/api/docs/guides/latest-model). Справочник описывает применимость моделей и настройки в исходниках Product-Agent OS. Для доступа, активации и сравнения качества нужны отдельные свидетельства.

## Матрица API-моделей

| Model ID / источник | API reasoning.effort | Кандидатная область применения в проекте | Tools |
| --- | --- | --- | --- |
| [gpt-6.2-sol](https://developers.openai.com/api/docs/models/gpt-6.2-sol) | `low`, `medium`, `high`, `xhigh`, `max`. `none` отклоняется | Основная модель проекта для реализации, планирования, проверок, документации и сбора контекста | Tool calling и Structured Outputs через Responses |
| [gpt-6.2-astra](https://developers.openai.com/api/docs/models/gpt-6.2-astra) | `low`, `medium`, `high`, `xhigh`, `max`. `none` отклоняется | Архитектура, независимое ревью и сложные риски безопасности | Tool calling и Structured Outputs через Responses |
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

## Локальная диагностика — PAOS-AUD-G2, 09.11.2026

`validate_codex_compatibility.py` разделяет локальную структуру package и host diagnostics. Без дополнительных входов client/model receipt/trust остаются missing, not_verified или unknown; установленный CLI не используется как версия App. Подтверждённый минимум [CLI 0.159.0 для GPT-6.1 Terra](https://learn.chatgpt.com/docs/models) применяется только к этой паре model/surface. Для других сочетаний минимум не выдумывается.

Опциональный `--observations <file.json>` читает до 16 KiB несекретного JSON: `surface` (Codex App, CLI, IDE extension), `client_version` (три числовых компонента), `configured_model`, `observed_model` (model IDs из таблицы), `trust` (trusted/untrusted), `native_plugin_observed` и `standalone_skills_observed` (boolean). Остальные поля не копируются в output; неизвестные значения не становятся evidence. Duplicate keys и malformed files отклоняются. Эти входы — caller-supplied observations, а не аутентифицированные receipts; account access и promotion остаются not_verified/not_assessed. Exit 0 означает только local structure, а не отсутствие host gaps.

`--cache-root <explicit-directory>` сравнивает SHA-256 canonical и указанного cache по manifests, MCP JSON и SKILL.md; результат match/drift/needs_review. Без cache — cache_not_provided. Чтение ограничено размером/количеством, ссылки отклоняются, содержимое и абсолютные пути не печатаются. Scope не включает scripts/templates и не доказывает выбор skill host; полный package/host receipt остаётся отдельным gate. Cache не сканируется автоматически и не изменяется. Диагностика не меняет pins или effort. T23–T29 остаются историческими проверками.

## Контекст и стоимость

Для GPT‑6.2 Sol и Astra API model pages указывают context window 1 050 000, max input 922 000 и max output 128 000 tokens. Проверяйте ограничения совместно. Фактический контекст в Codex зависит от клиента, модели и effective configuration. Лимиты API относятся к соответствующему API endpoint.

Стоимость зависит от модели, service tier, cache reads/writes и условий длинного контекста. Не переносите тариф или surcharge одной модели на остальные. Используйте датированную модельную страницу и [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching); подписка Codex/ChatGPT не является API-тарифом. Метод учета — в [evals](../agent-systems/evals-observability.md).

## Работа с GPT‑6.2

- **Codex.** Укажите ожидаемый результат, ограничения и наблюдаемые критерии проверки. Для знакомого кода дайте целевой путь и существующий пример. Для UI приложите эталон, если он есть, и проверьте результат в рабочем размере. Субагентам поручайте независимые задачи с явным владением. [Prompting GPT‑6.2 in Codex](https://learn.chatgpt.com/guides/prompting-gpt-6-2-astra)
- **Reasoning effort.** В проектных профилях сохранён прежний effort каждой роли. Сравнивайте 6.1 и 6.2 на одинаковых задачах и при одинаковом effort. Затем отдельным прогоном проверяйте более низкий поддерживаемый effort. Учитывайте качество, ошибки инструментов, время и стоимость на завершённую задачу. [Playbook миграции](../playbooks/model-migration.md)
- **Собственный клиент Responses API.** Для GPT‑6.2 поле верхнего уровня `instructions` добавляется после `input`. Стабильные переиспользуемые инструкции поместите в первое `developer`-сообщение в `input`, чтобы они могли попадать в кэш префикса. `instructions` подходит для указаний на текущий запрос. Это правило относится к формированию API-запроса. `AGENTS.md` и `developerInstructions` Codex app-server остаются отдельными поверхностями. [Using GPT‑6.2](https://developers.openai.com/api/docs/guides/latest-model)

## Retirement и исторические результаты

GPT-5.5 выведена из Codex с ChatGPT sign-in 14 октября 2026 в 19:00 UTC; это не распространяется на API/API-key Codex sessions. GPT-5.4 и GPT-5.4-mini выведены из sign-in Codex 31 августа 2026. Проверяйте [retirement guidance](https://learn.chatgpt.com/docs/models) для выбранной поверхности. Здесь не утверждается, что GPT-5.6 удалена из API.

Исторические pins, approvals, frozen fixtures и eval results сохраняют исходные model ID и даты. Переписывание старого результата на новую модель разрушает доказательство.

## Действующее состояние Product-Agent OS

| Слой | Настройка в исходниках на 2026-11-18 | Граница утверждения |
| --- | --- | --- |
| 15 проектных профилей | 12 на `gpt-6.2-sol`, 3 на `gpt-6.2-astra` (`architect`, `reviewer`, `security-privacy-supply-chain-reviewer`). Общий default субагентов — Sol `medium` | Effort ролей сохранён. Доступ и эффективная конфигурация требуют отдельного наблюдения |
| 8 профилей в шаблонах плагина | 6 на Sol, 2 на Astra (`architect`, `reviewer`) | Подготавливаемые предложения для целевых проектов |
| Совместимость и откат | Валидаторы принимают GPT‑6.2 и прежние GPT‑6.1 Sol/Terra в профилях. Для общего default допускается GPT‑6.1 Sol при откате | Приём идентификатора локальным валидатором не подтверждает доступность модели |
| Поведенческая оценка | GPT‑6.1 Sol/Terra остаются baseline. `config_pinned_behavioral_promotion_pending` | Сравнительное качество, стоимость, задержка и загрузка в новой сессии пока не измерены |

Исполняемая конфигурация владеет pins. [Playbook](../playbooks/model-migration.md) задаёт процедуру сравнения, пороги и откат. [Compatibility](../product-agent-os/codex-compatibility.md) описывает диагностику клиента. Для передачи результата указывайте фактически наблюдавшуюся модель, effort и среду, если эти данные доступны.
