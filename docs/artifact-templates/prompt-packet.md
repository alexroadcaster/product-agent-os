# Универсальный prompt template

Source status: `official + experiment`

```text
# Role
You are ...

# Goal
...

# Audience
...

# Context
<source id="S1" type="official" url="...">
...
</source>

# Constraints
- ...

# Unknowns and assumptions
- Ask a clarifying question if ...
- If not blocked, assume ...

# Tools
- Use ... when ...
- Do not use ... unless ...

# Output format
Return:
- ...

# Verification
- ...

# Fallback
If context is insufficient, return:
- missing_context
- clarifying_question
- unsupported_claims
```

## Применимость шаблона

Полный prompt packet нужен, когда сложность требует отдельных fields. Для обычной задачи достаточно goal, scope, acceptance и limits. Начинайте zero-shot; примеры добавляйте для measured recurring failure или product requirement. [Prompt guidance](https://developers.openai.com/api/docs/guides/latest-model).
