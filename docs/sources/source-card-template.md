# Шаблон карточки источника

Source status: `official | community | experiment`

Используйте этот формат для каждого нового источника.

```yaml
title: ""
url: ""
type: "documentation | guide | changelog | issue | discussion | article | experiment"
status: "official | community | experiment"
checked_at: "YYYY-MM-DD"
summary: ""
relevance: ""
trust_level: "high | medium | low"
```

Правила:

- `official` получает приоритет над любым community-источником.
- `community` нельзя превращать в инструкцию без проверки.
- `experiment` должен иметь воспроизводимый сценарий проверки.
- Если источник противоречит официальной документации, фиксируйте конфликт и не переносите утверждение в основные инструкции.
