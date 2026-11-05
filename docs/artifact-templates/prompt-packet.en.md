# Universal Prompt Template

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

## Template applicability

Use the full prompt packet when complexity requires distinct fields. An ordinary task can state goal, scope, acceptance and limits concisely. Start zero-shot; add examples for a measured recurring failure or product requirement. [Prompt guidance](https://developers.openai.com/api/docs/guides/latest-model).
