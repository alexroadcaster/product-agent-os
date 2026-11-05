# Live runtime governance

Source status: `official + experiment`

## Purpose

This page describes the Product-Agent OS governance boundary: from approval packet and data classification to disabled-by-default local runtime, provider gates, review ledger, canonical mutation dry-run, audit/observability, real-testing readiness and runtime QA.

This document is an operator guide. It does not start a live server, run browser automation, perform provider/API calls, mutate the canonical graph or run git stage/commit/push/PR. All generated artifacts are staged evidence only and are not source of truth.

## Approvals And Source-Of-Truth Boundary

Source of truth remains checked-in Markdown/JSON/JSONL control-plane artifacts, official OpenAI documentation for Codex App, CLI, IDE extension, approvals, sandbox, MCP and project-authored source files. Generated graph/runtime/provider artifacts are review views and evidence packets.

Any live/runtime/provider/mutation step requires an approval packet with:

- `explicit_approval: true`;
- owner and allowed surfaces;
- data classification and redaction boundary;
- credential boundary: credentials only through environment or trusted local config, with no secrets in docs, prompts, fixtures, caches or logs;
- cache policy, TTL, invalidation and deletion proof;
- token/cost/latency budget and fallback on exceed;
- eval thresholds;
- rollback path;
- residual risks and accepted gaps.

Without a complete approval packet, the action remains `approval_required`, `blocked` or degrades to graph-only fallback.

## Inputs

Minimum inputs for live governance:

- governance packet from `project_graph_live_governance.py`;
- local read-only runtime packet from `project_graph_live_runtime.py`;
- provider gates for embeddings, reranker/hybrid retrieval and LLM proposals;
- human review ledger and proposal diff preview;
- canonical mutation dry-run, journal and rollback proof;
- audit/security/observability/handoff packets;
- real-testing readiness, target consent, pilot harness and Codex surface smoke;
- browser QA, performance budget and stabilization ledger.

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

1. Validate governance before any live surface.
2. Keep runtime disabled by default, local-only, read-only, authenticated where required, with graph-only fallback and clean shutdown evidence before real launch is considered.
3. Gate embedding provider with redaction, cache, budget and eval threshold. If threshold fails, keep `semantic_retrieval_or_graph_only`.
4. Gate reranker and hybrid retrieval with bounded candidates, explainable fusion and no canonical mutation.
5. Gate LLM proposal provider as proposal-only structured JSON. Provider output is never canonical fact and unsafe output routes to incident/fallback.
6. Route proposals through human review ledger: `accepted`, `rejected` or `accepted_gap` with evidence refs.
7. Use canonical mutation only as dry-run mutation planning unless accepted proposal, conflict checks, append-only journal and rollback proof are present.
8. Record redacted append-only audit events, negative security/privacy checks, runtime health, latency, provider errors, budget usage, degraded mode and handoff ownership.
9. Prove real-testing readiness with owner-approved target/data policy, dry-run pilot harness, Codex App/CLI/IDE extension smoke and use-case pilot mapping.
10. Record browser QA expectations, console/network checks, mobile overflow, generated-view labels, source-boundary labels, performance budget and stabilization status.

## Verification

Governance is acceptable only when evidence shows:

- `provider_call_allowed: false` and `external_call_performed: false` unless a later separately approved execution packet changes the specific surface;
- no live server launch during docs/governance preparation;
- no browser automation during docs/governance preparation;
- no canonical graph mutation outside approved dry-run/staged copy paths;
- no git stage/commit/push/PR;
- generated artifacts are labeled as staged evidence and not source of truth;
- budget breach disables live layer or records owner-accepted gap;
- no open P0/P1 before closure;
- fallback remains usable when live/provider layers are disabled.

For docs-only preparation, read-only inspection is enough unless a focused docs verification owner later runs targeted checks.

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

Use this page as the governance checklist before any approval-bound real-testing action. The next safe artifact is an approval packet that names exactly one planned action, its owner, allowed target, data policy, command scope, rollback and verification evidence.

## Current route and evidence

Local execution and cloud orchestration have different controls. MCP, connectors, browser and shell do not share one network policy. Apply the [surface matrix](../codex/surfaces.md) and [security guide](../codex/security.md) before any runtime claim.
