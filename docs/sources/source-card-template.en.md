# Source Card Template

Source status: `official | community | experiment`

Use this format for every new source.

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

Rules:

- `official` has priority over any community source.
- `community` cannot become an instruction without verification.
- `experiment` must include a reproducible verification scenario.
- If a source conflicts with official documentation, record the conflict and do not move the claim into core instructions.

## Claim scope

For drift-prone product claims also record these fields; do not update `checked_at` without reading the source.

```yaml
product: ""
client_and_version: ""
auth_and_plan_scope: ""
claim: ""
current_or_legacy: ""
evidence_kind: "documentation | local_check | runtime"
limitations: []
```
