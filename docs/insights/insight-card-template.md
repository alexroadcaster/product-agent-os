# Шаблон карточки insight

Source status: `community | experiment`

```yaml
claim: ""
source: ""
evidence: ""
works_for: ""
risks: ""
verification_status: "unverified | reproduced | adopted | rejected | stale"
checked_at: "YYYY-MM-DD"
trust_level: "high | medium | low"
```

Минимальный пример:

```yaml
claim: "Subagents стоит запускать только для независимой read-heavy работы."
source: "https://developers.openai.com/codex/concepts/subagents"
evidence: "Official docs describe subagents as useful for parallel exploration, tests, log analysis, and warn about write-heavy coordination risk."
works_for: "Large review, source research, test triage."
risks: "Overuse increases token spend and can fragment context."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```
