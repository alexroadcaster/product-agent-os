# Live runtime governance

Source status: `official + experiment`

## Назначение

Эта страница описывает governance-контур Product-Agent OS: от approval packet и data classification до disabled-by-default local runtime, provider gates, review ledger, canonical mutation dry-run, audit/observability, real-testing readiness и runtime QA.

Документ является операторским guide. Он не запускает live server, не выполняет browser automation, не делает provider/API calls, не мутирует canonical graph и не выполняет git stage/commit/push/PR. Все generated artifacts являются staged evidence только и не являются каноническим источником.

## Approvals And Source-Of-Truth Boundary

канонический источник остаются checked-in Markdown/JSON/JSONL control-plane artifacts, официальная документация OpenAI для Codex App, CLI, IDE extension, approvals, sandbox, MCP и project-authored source files. Generated graph/runtime/provider artifacts являются review views и evidence packets.

Любой live/runtime/provider/mutation шаг требует approval packet с:

- `explicit_approval: true`;
- owner и allowed surfaces;
- data classification и redaction boundary;
- credential boundary: credentials только через environment или trusted local config, без secrets в docs, prompts, fixtures, caches или logs;
- cache policy, TTL, invalidation и deletion proof;
- token/cost/latency budget и fallback на exceed;
- eval thresholds;
- rollback path;
- residual risks и accepted gaps.

Без полного approval packet действие остается `approval_required`, `blocked` или деградирует в graph-only fallback.

## Входы

Минимальные входы для live governance:

- governance packet из `project_graph_live_governance.py`;
- local read-only runtime packet из `project_graph_live_runtime.py`;
- provider gates для embeddings, reranker/hybrid retrieval и LLM proposals;
- human review ledger и proposal diff preview;
- canonical mutation dry-run, journal и rollback proof;
- audit/security/observability/handoff packets;
- real-testing readiness, target consent, pilot harness и Codex surface smoke;
- browser QA, performance budget и stabilization ledger.

Входы не должны включать raw secrets, credentials, raw private source bodies, raw private chat logs, private customer data или unredacted PII.

## Выходы и артефакты

Ожидаемые артефакты являются staged evidence packets, не canonical truth:

- `live-runtime-approval.json`, `data-classification.json`, cache/budget policies;
- live runtime contract с local-only, read-only routes и `disabled_by_default_not_started`;
- embedding provider gate и eval baseline;
- reranker provider gate и hybrid retrieval pipeline;
- LLM proposal provider gate и safety eval;
- `graph-review-ledger.json` и `proposal-diff.json`;
- `mutation_plan.json`, `graph-mutation-journal.jsonl` и rollback proof;
- `audit-log.jsonl`, `security-privacy.json`, `runtime-observability.json`, `agent-skill-handoff.json`;
- `real-testing-readiness.json`, `real-testing-targets.json`, `pilot-harness.json`, `codex-surface-smoke.json`, `real-testing-pilot-matrix.json`;
- `project-code-graph-runtime-browser-qa.json`, `project-code-graph-performance-budget.json`, `project-code-graph-stabilization-ledger.json`.

## Workflow

1. Validate governance до any live surface.
2. Keep runtime disabled через default, local-only, read-only, authenticated где required, с graph-only fallback и clean shutdown evidence до real launch является considered.
3. Gate embedding provider с redaction, cache, budget и eval threshold. Если threshold fails, keep `semantic_retrieval_or_graph_only`.
4. Gate reranker и hybrid retrieval с bounded candidates, explainable fusion и нет canonical mutation.
5. Gate LLM proposal provider как proposal-only structured JSON. Provider output является never canonical fact и unsafe output routes к incident/fallback.
6. Route proposals через human review ledger: `accepted`, `rejected` или `accepted_gap` с evidence refs.
7. Используйте canonical mutation только как dry-run mutation planning пока accepted proposal, conflict checks, append-only journal и rollback proof являются present.
8. Record redacted append-only audit events, negative security/privacy checks, runtime health, latency, provider errors, budget usage, degraded mode и handoff ownership.
9. Prove real-testing readiness с owner-approved target/data policy, dry-run pilot harness, Codex App/CLI/IDE extension smoke и use-case pilot mapping.
10. Record browser QA expectations, console/network checks, mobile overflow, generated-view labels, source-boundary labels, performance budget и stabilization status.

## Проверка

Governance является acceptable только когда evidence shows:

- `provider_call_allowed: false` и `external_call_performed: false` пока later separately approved execution packet changes specific surface;
- нет live server launch during docs/governance preparation;
- нет browser automation during docs/governance preparation;
- нет canonical graph mutation outside approved dry-run/staged copy paths;
- нет git stage/commit/push/PR;
- generated artifacts являются labeled как staged evidence и не является каноническим источником;
- budget breach disables live layer или records owner-accepted gap;
- нет open P0/P1 до closure;
- fallback остается usable когда live/provider layers являются disabled.

Для docs-only preparation достаточно read-only inspection, если focused docs verification owner не запускает targeted checks отдельно.

## Риски And Failure Modes

- Generated views may look authoritative если source-boundary и generated-view labels являются missing.
- Provider payloads может leak secrets, paths или raw source если redaction является bypassed.
- Credentials может leak если stored в docs, fixtures, prompts, caches или logs.
- Cache может make stale evidence look текущий без fingerprint invalidation и deletion proof.
- Provider eval может быть misleading если это lacks baseline, threshold или fallback.
- LLM proposals может hallucinate или overstate unsupported claims.
- Human review ledger является invalid если accepted proposals lack owner decision и evidence refs.
- Canonical mutation является unsafe без dry-run, conflict checks, journal и rollback proof.
- Runtime QA является incomplete если mobile overflow, console/network, source-boundary labels или performance budget являются missing.

## Next Action

Используйте эта page как governance checklist до any approval-bound real-testing action. Этот next safe artifact является approval packet который names exactly один planned action, его owner, allowed target, data policy, command scope, rollback и verification evidence.

## Актуальный маршрут и evidence

Local execution и cloud orchestration имеют разные controls. MCP, connectors, browser и shell не разделяют одну network policy. [Surface matrix](../codex/surfaces.md) и [security](../codex/security.md) применяются до любого runtime claim.
