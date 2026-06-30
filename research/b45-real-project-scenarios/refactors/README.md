# B45-PCA-M33 Refactor Arms

Source status: fixture-local refactor comparison evidence for `B45-PCA-M33`.
These arms are stored inside `codex_docs` copied fixtures only. They do not
mutate `SOL 0.6`, `myPartners`, runtime state, databases, git, deployment,
publication, provider/API surfaces, browser automation, hooks or automations.

`B45-PCA-M33` compares original, checklist-guided and advisory-guided arms
against the `B45-PCA-M32` baseline:

- `mypartners/MP-CRM-CHAT-OPEN-01/` contains copied source-file arms for the
  CRM contact/chat-open fixture.
- `sol/SOL-AGENT-ORCH-01/` records no-code arms because the SOL fixture still
  lacks runnable TypeScript/static test proof and TypeScript advisory coverage.

The source-owned comparison packet is:

```text
docs/superpowers/specs/batch45-real-project-refactor-comparison.json
```

Unsupported claims remain explicit: target behavior, runtime behavior, browser
behavior, provider/live API behavior, production-data safety, release readiness,
git readiness and real AI-agent behavior improvement are not proved by these
fixture-local arms.
