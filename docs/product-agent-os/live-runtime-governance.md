# Live runtime governance

Source status: `official + experiment`

## Назначение

Эта страница описывает governance-контур Product-Agent OS для Task 26 Batch 24-33: от approval packet и data classification до disabled-by-default local runtime, provider gates, review ledger, canonical mutation dry-run, audit/observability, real-testing readiness и runtime QA.

Документ является операторским guide. Он не запускает live server, не выполняет browser automation, не делает provider/API calls, не мутирует canonical graph и не выполняет git stage/commit/push/PR. Все generated artifacts являются staged evidence only и не являются source of truth.

## Approvals And Source-Of-Truth Boundary

Source of truth остаются checked-in Markdown/JSON/JSONL control-plane artifacts, официальная документация OpenAI для Codex App, CLI, IDE extension, approvals, sandbox, MCP и project-authored source files. Generated graph/runtime/provider artifacts являются review views и evidence packets.

Любой live/runtime/provider/mutation шаг требует approval packet с:

- `explicit_approval: true`;
- owner и allowed surfaces;
- data classification и redaction boundary;
- credential boundary: credentials только через environment или trusted local config, без secrets в docs, prompts, fixtures, caches или logs;
- cache policy, TTL, invalidation и deletion proof;
- token/cost/latency budget и fallback on exceed;
- eval thresholds;
- rollback path;
- residual risks и accepted gaps.

Без полного approval packet действие остается `approval_required`, `blocked` или деградирует в graph-only fallback.

## Inputs

Минимальные входы для live governance:

- Task 26 plan rows `T10-LIVE-M01..M34`;
- Batch 24 governance packet from `project_graph_live_governance.py`;
- Batch 25 local read-only runtime packet from `project_graph_live_runtime.py`;
- Batch 26-28 provider gates for embeddings, reranker/hybrid retrieval and LLM proposals;
- Batch 29 human review ledger and proposal diff preview;
- Batch 30 canonical mutation dry-run, journal and rollback proof;
- Batch 31 audit/security/observability/handoff packets;
- Batch 32 real-testing readiness, target consent, pilot harness and Codex surface smoke;
- Batch 33 browser QA, performance budget and stabilization ledger.

Inputs must not include raw secrets, credentials, raw private source bodies, raw private chat logs, private customer data or unredacted PII.

## Outputs And Artifacts

Expected artifacts are staged evidence packets, not canonical truth:

- `live-runtime-approval.json`, `data-classification.json`, cache/budget policies;
- live runtime contract with local-only, read-only routes and `disabled_by_default_not_started`;
- embedding provider gate and eval baseline;
- reranker provider gate and hybrid retrieval pipeline;
- LLM proposal provider gate and safety eval;
- `graph-review-ledger.json` and `proposal-diff.json`;
- `mutation_plan.json`, `graph-mutation-journal.jsonl` and rollback proof;
- `audit-log.jsonl`, `security-privacy.json`, `runtime-observability.json`, `agent-skill-handoff.json`;
- `real-testing-readiness.json`, `real-testing-targets.json`, `pilot-harness.json`, `codex-surface-smoke.json`, `real-testing-pilot-matrix.json`;
- `project-code-graph-runtime-browser-qa.json`, `project-code-graph-performance-budget.json`, `project-code-graph-stabilization-ledger.json`.

## Workflow

1. Validate Batch 24 governance before any live surface.
2. Keep Batch 25 runtime disabled by default, local-only, read-only, authenticated where required, with graph-only fallback and clean shutdown evidence before real launch is considered.
3. Gate Batch 26 embedding provider with redaction, cache, budget and eval threshold. If threshold fails, keep `semantic_retrieval_or_graph_only`.
4. Gate Batch 27 reranker and hybrid retrieval with bounded candidates, explainable fusion and no canonical mutation.
5. Gate Batch 28 LLM proposal provider as proposal-only structured JSON. Provider output is never canonical fact and unsafe output routes to incident/fallback.
6. Route Batch 29 proposals through human review ledger: `accepted`, `rejected` or `accepted_gap` with evidence refs.
7. Use Batch 30 only as dry-run mutation planning unless accepted proposal, conflict checks, append-only journal and rollback proof are present.
8. Record Batch 31 redacted append-only audit events, negative security/privacy checks, runtime health, latency, provider errors, budget usage, degraded mode and handoff ownership.
9. Use Batch 32 to prove real-testing readiness, owner-approved target/data policy, dry-run pilot harness, Codex App/CLI/IDE extension smoke and Track 8 use-case pilot mapping.
10. Use Batch 33 to record browser QA expectations, console/network checks, mobile overflow, generated-view labels, source-boundary labels, performance budget and stabilization status.

## Verification

Governance is acceptable only when evidence shows:

- `provider_call_allowed: false` and `external_call_performed: false` unless a later separately approved execution packet changes the specific surface;
- no live server launch in Batch 24-34 docs/governance work;
- no browser automation in Batch 24-34 docs/governance work;
- no canonical graph mutation outside approved dry-run/staged copy paths;
- no git stage/commit/push/PR;
- generated artifacts are labeled as staged evidence and not source of truth;
- budget breach disables live layer or records owner-accepted gap;
- no open P0/P1 before closure;
- fallback remains usable when live/provider layers are disabled.

For docs-only Batch 34 work, read-only inspection is enough unless the owning Batch 34 tester later runs focused docs checks.

## Risks And Failure Modes

- Generated views may look authoritative if source-boundary and generated-view labels are missing.
- Provider payloads can leak secrets, paths or raw source if redaction is bypassed.
- Credentials can leak if stored in docs, fixtures, prompts, caches or logs.
- Cache can make stale evidence look current without fingerprint invalidation and deletion proof.
- Provider eval can be misleading if it lacks baseline, threshold or fallback.
- LLM proposals can hallucinate or overstate unsupported claims.
- Human review ledger is invalid if accepted proposals lack owner decision and evidence refs.
- Canonical mutation is unsafe without dry-run, conflict checks, journal and rollback proof.
- Runtime QA is incomplete if mobile overflow, console/network, source-boundary labels or performance budget are missing.

## Next Action

Use this page as the Batch 24-33 governance checklist before Batch 35. The next safe artifact is an approval-bound Batch 35 packet that names exactly one planned action, its owner, allowed target, data policy, command scope, rollback and verification evidence.
