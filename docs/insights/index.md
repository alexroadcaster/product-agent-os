# Слой insights

Source status: `community | experiment`

Insights - это неофициальный слой: пользовательские трюки, наблюдения, GitHub issues, Reddit-паттерны, blog posts и локальные эксперименты. Они полезны для улучшения работы, но не являются источником истины.

## Правила

- Insight не переносится в основной guide без проверки.
- Каждый insight имеет `verification_status`.
- Если insight противоречит официальной документации, он остается в insights с пометкой конфликта.
- Если insight подтвержден локально, добавьте reproduction или transcript summary.
- Если insight устарел после changelog update, пометьте его как `stale`.

## Статусы проверки

| Статус | Значение |
| --- | --- |
| `unverified` | Найдено в community/source, не проверено |
| `reproduced` | Проверено локально один раз |
| `adopted` | Стало частью project workflow |
| `rejected` | Проверка не подтвердила |
| `stale` | Было полезно, но могло устареть |

## Добавление insight

1. Скопируйте [шаблон карточки](insight-card-template.md).
2. Укажите источник и дату.
3. Опишите риск.
4. Определите проверку.
5. Только после проверки переносите вывод в playbook.

