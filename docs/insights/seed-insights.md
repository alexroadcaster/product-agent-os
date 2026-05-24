# Начальный backlog insights

Source status: `official + community + experiment`

Эти карточки задают формат слоя insights. Часть из них основана на официальных источниках и уже может считаться adopted; community-only утверждения должны добавляться отдельно после проверки.

```yaml
claim: "Для multi-agent workflow сначала разделяйте read-heavy задачи; write-heavy задачи требуют непересекающихся файлов и явного ownership."
source: "https://developers.openai.com/codex/concepts/subagents"
evidence: "Official guidance recommends subagents for exploration, tests, triage, summarization, and warns that parallel write-heavy work increases coordination overhead."
works_for: "Research, review, log analysis, documentation audit."
risks: "Если несколько агентов редактируют одни файлы, растет риск конфликтов и потери решений."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Правила, которые должны выполняться всегда, должны жить в AGENTS.md или checked-in docs, а не только в memory."
source: "https://developers.openai.com/codex/memories"
evidence: "Official docs say to keep required team guidance in AGENTS.md or checked-in documentation and treat memories as helpful local recall."
works_for: "Team standards, test commands, documentation policy, source policy."
risks: "Memory can be local, disabled, unavailable, stale, or inappropriate for shared team rules."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Если workflow повторяется три и более раза, кандидат на Skill должен иметь явные inputs, outputs и deterministic scripts только там, где это нужно."
source: "https://developers.openai.com/codex/skills"
evidence: "Official skills guidance emphasizes focused jobs, imperative steps, explicit inputs/outputs, and scripts for deterministic behavior or external tooling."
works_for: "Source card creation, insight intake, docs refresh, claim verification."
risks: "Слишком широкий skill становится скрытой политикой проекта и ухудшает predictability."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Community tips should be harvested as candidate claims, not copied into official guides."
source: "https://community.openai.com/"
evidence: "Community sources vary in version, platform, local config, and user assumptions."
works_for: "Insight backlog and experiment design."
risks: "Unverified tricks can conflict with current Codex behavior or security policy."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "medium"
```

```yaml
claim: "Для source-sensitive documentation workflows Manager pattern безопаснее Handoff pattern, потому что один orchestrator удерживает source policy и acceptance criteria."
source: "https://github.com/openai/openai-agents-python"
evidence: "Agents SDK documentation describes Manager pattern and Handoffs as distinct multi-agent design patterns."
works_for: "Research synthesis, documentation updates, claim verification."
risks: "Manager can become bottleneck if every task is serialized."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Structured outputs should be used for handoff payloads and verifier outputs when downstream automation depends on exact fields."
source: "https://developers.openai.com/api/docs/guides/structured-outputs"
evidence: "OpenAI API documentation describes JSON Schema-based structured outputs for constrained model responses."
works_for: "Source cards, insight cards, handoff contracts, eval outputs."
risks: "Overly rigid schemas can reject useful exploratory notes."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Granular approvals should be documented as part of agent architecture, not treated as a local runtime detail."
source: "https://developers.openai.com/codex/agent-approvals-security"
evidence: "Codex documentation supports granular approval configuration for sandbox approvals, rules, MCP elicitations, permissions, and skill approval."
works_for: "Local implementation, Codex MCP workflows, skill design."
risks: "Too many approval prompts can slow iteration; too few increase blast radius."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Structured Outputs solve output-shape reliability, not factual reliability; factual tasks still need grounding, citations, and verification."
source: "https://developers.openai.com/api/docs/guides/structured-outputs"
evidence: "OpenAI documentation notes that structured outputs can still contain mistakes and require prompt adjustments, examples, or task decomposition."
works_for: "Handoff contracts, source-card generation, verifier outputs, eval result schemas."
risks: "Schema forcing can make a model fill required fields even when the input is unrelated unless fallback behavior is specified."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "For hallucination-sensitive workflows, design the eval before optimizing the prompt."
source: "https://developers.openai.com/api/docs/guides/model-optimization"
evidence: "OpenAI model optimization guidance recommends establishing eval baselines and iterating prompts against representative test inputs."
works_for: "Prompt versioning, grounded answering, documentation QA, agent reliability."
risks: "A narrow eval can overfit prompts and miss real-world failure modes."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```

```yaml
claim: "Session memory should never be used as a citation source; retrieve authoritative context again for factual answers."
source: "https://developers.openai.com/codex/memories"
evidence: "Codex memory guidance distinguishes helpful recall from required project guidance, and official docs remain source of truth."
works_for: "Long-running agent sessions, research loops, support assistants, documentation updates."
risks: "Over-retrieval can increase latency and cost; use targeted retrieval."
verification_status: "adopted"
checked_at: "2026-05-14"
trust_level: "high"
```
