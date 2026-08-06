# EVALS.md

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Purpose

`EVALS.md` is the compact evaluation routing layer for current Product-Agent OS work. It stores rubrics, thresholds, active eval routes and unsupported-claim rules. Historical eval narratives and batch evidence live in [current control-plane state](docs/product-agent-os/control-plane-current-state.md), source backlogs, registry entries and evidence packets.

## Rubrics

- Source grounding: official sources and checked-in docs drive durable rules; community claims stay in insight/research layer.
- Evidence before completion: ready/completed/fixed/works/release claims require current command evidence, current eval evidence, current runtime evidence or explicit inspection-only gap.
- Conditional applicability: methodology gates can be `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, `applicable_missing` or `approval_required`.
- Owner sufficiency: artifacts prove evidence shape and routing; a human owner still judges whether evidence is sufficient for real project risk.
- Source boundary: generated dashboards, graph outputs, HTML views, scorecards and `site/` builds are orientation evidence unless an owning source document says otherwise.
- Real-project evidence: deterministic fixtures prove contract shape, but Product-Agent OS product confidence requires real-project target evidence where the route depends on actual project structure, source policy, workflow, runtime signals or owner judgment.
- Approval boundary: live servers, browser automation, provider/live external model/API calls, production data access, canonical graph source mutation, external writes and git stage/commit/push/PR remain approval-bound.
- Documentation quality: user-facing docs are Russian, behavior-level and name inputs, outputs, verification, risks and next artifact.
- Safety: secrets, private data, raw prompts/traces and absolute user-specific paths are not eval fixtures, examples or templates.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, transcript eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive changes, Codex compatibility regression or approval-bound action performed without approval.
- Accepted gap: allowed only when reason, owner, evidence owner, downstream risk and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and the final response.
- Unsupported claim: any quality, readiness, release, security, AI/RAG, runtime or product-success claim without current evidence must be rejected or labeled inspection-only.
- Synthetic-only limitation: internal `codex_docs` fixtures cannot support broad real-project usefulness, product-success, release-readiness, automation promotion or mass-user readiness without representative real-project evidence or owner-reviewed accepted gap.
- Batch 45 promotion: no promotion unless current approved comparable evidence clears the configured threshold and reviewer gates. T14 `+3.27%` with reviewer `0` is below `>=20%` and not same-model comparable. T18 defines the same-model promotion-grade comparison, strict schema, quarantine, scoring/reviewer rubric and result contract; T19 defines cost/timeout/retry/abort/raw-temp-only retention; T20-A03 records the owner-confirmed cost-waived approval consumed by T21; T21 started one approved primary call and aborted on strict schema validation with `valid_pair_count=0`; T22-A02 records no-go because T21 produced no valid pairs and the reviewer gate was not run.

## Current Evaluation State

| Workstream | Eval state | Claim ceiling |
| --- | --- | --- |
| Batch 35 / Batch 38 | `T10-LIVE-M41` owner-closed no-op as `owner_closed_no_op_git_release_pr`; `B38-S2` cache refresh current; historical cache blocker preserved. | No future git/cache action without fresh approval. |
| Batch 39 | S5 decision: release `no_go`, owner-feedback `conditional_go`, runtime/browser `approval_required`. | Owner-feedback only; no release/runtime/browser/promotion claim. |
| Batch 41 | S9 generated-artifact modernization and Neural_Flow comparison. | Generated-artifact acceptance evidence only; no release/target-apply/Cosmos.gl-WebGL runtime proof. |
| Batch 42 | Planned-only instruction/tool-use matrix. | No fixed-auto-engagement claim. |
| Batch 44 | S0-S7 local/staged/manual Self-Learning Loop evidence. | No active automation, hidden telemetry, real session import, provider/model call, target mutation or auto-apply proof. |
| Batch 45 | M26/M27/M35/T12/T15 keep advisory-only/no-go; T14 is positive current-quality signal only; T20-A03 was consumed by T21; T21 started one approved primary call and aborted on strict schema validation with zero valid pairs; T22-A02 reviewer gate is not run because T21 result is invalid for scoring. | No promotion, blocker, CI, runtime/browser, target or release claim; no further provider/model/reviewer call without new exact approval. |
| Track 11 DOC-M25 | Generated root `site`, search and sitemap freshness packet exists. | No browser proof, broad scans, remediation, raw retention, publication/release/deploy/git claim. |
| GPT-5.6 model/config migration | Role-aware Sol/Terra pins remain; R1-R6 requires one native permission model, generic Terra/medium defaults, explicit write-skill authority, Docs MCP on source roles, resolvable paths, phase-neutral prompts and a 7000-character developer-prompt budget. Luna remains an unevaluated high-volume candidate. | Static contract evidence may support configuration consistency only. No quality, cost, latency, fresh-session MCP/hook, broad agent-behavior or promotion claim until bounded comparative/runtime evidence exists. |
| Lifecycle/control-plane sync | Config-routed Task Brief, lifecycle marker, control-plane sync and Completion Brief contract. | Hook output is reminder/evidence context only, not completion proof. |

## Active Eval Routes

| Change type | Required eval route |
| --- | --- |
| Docs, source registry, control-plane or docs tests | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools\check_docs.py`, `git diff --check` |
| MkDocs navigation, Mermaid, localization, search/sitemap or generated `site` evidence | Docs route plus strict MkDocs build |
| Plugin scripts, templates, lifecycle skills, runtime behavior or CLI contracts | Focused tests, full unittest, fixture eval, transcript eval, Codex compatibility, docs check and diff hygiene as routed by `TEST.md` |
| Batch 39 pilot/hardening matrix | `prod_test.md` attempt/failure/fix/retest ledger review plus focused tests, fixture/transcript eval, redaction/no-mutation proof and docs/diff hygiene |
| Self-Learning Loop | Focused state/extensions tests, staged initializer/runner/export checks where applicable, docs check and diff hygiene |
| Batch 45 Professional Code Authoring | Focused comment-sufficiency, coding-standards, behavioral, discovery/status/dashboard/template/fixture, self-learning, automation-policy, docs/source-link, manual-pilot ledger and diff hygiene |
| AI/RAG behavior, provider gates or model migration | Baseline eval, one focused change, rerun eval, inspect artifacts, record threshold/fallback and approval boundary |
| Frontend/browser/runtime UX | Build/test/lint where available, browser/runtime evidence, console/network checks, responsive/overflow evidence and screenshot/trace evidence or explicit gap |
| Release, external write, automation or git action | Explicit owner approval packet, current evidence, rollback/recovery path and no silent stage/commit/push/PR |

## Methodology Eval Map

| Area | Gate or evidence key | Primary evidence owner |
| --- | --- | --- |
| Track 8 scenario routing | `T8-S16`, `T8-A3..A16`, `T8-B`, `T8-C`, `T8-D`, `T8-F`, `T8-GX`, `T8-GY`, `T8-H` | Track 8 detailed backlog, Product-Agent OS docs and fixture/transcript evals |
| Track 9 methodologies | `business_product_contract_present`, `requirements_domain_contract_present`, `solution_architecture_contract_present`, `quality_testing_evals_contract_present`, `codex_agentic_workflow_contract_present`, `frontend_contract_present`, `backend_contract_present`, `api_integrations_contract_present`, `database_data_contract_present`, `llm_ai_rag_contract_present`, `security_privacy_compliance_contract_present`, `delivery_release_operations_contract_present`, `cross_domain_synthesis_contract_present` | Track 9 backlog, methodology docs, templates and eval fixtures |
| Track 10 guided questions/dashboard | `question_queue_contract_present`, `status_dashboard_present`, stale-evidence guard | Track 10 backlog and Product-Agent OS docs |
| Track 10 live layer | `T10-LIVE-M01..M41`, approval-bound live/runtime/provider/mutation/git gates | Track 10 backlog, registry and Batch 35 packet |
| Batch 39 | `B39-S1..S5`, `B39-TEST-M01..M54`, generated-view-only, source-policy and no-unapproved-actions gates | `prod_test.md`, B39 packets |
| Batch 44 | Self-Learning Loop state, due-check, manual pilot, Promptfoo export, HALO-style packet and candidate-only repair routing | B44 packets and `docs/product-agent-os/self-learning-loop.md` |
| Batch 45 | Professional Code Authoring checklist, advisory validator, behavior eval, retest protocol, post-Q4 decision gates and S8 promotion-grade eval design route | B45 packets and `docs/product-agent-os/coding-standards.md` |
| Track 11 docs/site | G1.1 docs-toolchain, G2-G5 source docs, DOC-M25 site freshness | Track 11 plan, registry and documentation-refresh packets |

## Unsupported Claims

Use this triage shape when a claim lacks evidence:

```text
Claim:
Missing source:
Verification needed:
Current status: unsupported | inspection-only | explicit_gap_accepted | approval_required
Owner:
Follow-up:
```

Reject or downgrade these claim patterns unless current evidence exists:

- Tests pass, build works, feature works, release ready, deployment safe or security reviewed from inspection alone.
- AI/RAG quality, grounding, model improvement, prompt safety or tool safety without baseline and rerun eval evidence.
- Generated graph/dashboard/site output as source of truth.
- Approval-bound live/provider/runtime/canonical-mutation/git action implied by a planning packet or generated artifact.
- Methodology artifact presence as proof that a human owner accepted semantic correctness.
- Batch 45 promotion from T14/T15/T16-T22/T17/T18/T19/T20/T21/T22; current result has no valid pair set and the reviewer gate did not run. `B45-POSTQ4-T20-A03` was consumed/aborted by `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`; any rerun needs strict output/schema normalization plus a new exact approval before another provider/model/reviewer call.

## Historical Eval Evidence Owners

- Track 8 scenario, readiness, false-positive and transcript/session evidence: `docs/sources/product-agent-os-track-8-detailed-backlog.md`.
- Track 9 methodology intelligence evidence across all domains, synthesis and runtime runner: `docs/sources/product-agent-os-track-9-backlog.md` and `docs/sources/registry.md`.
- Track 10 evidence, including project graph, live-layer gates, Batch 34 docs/i18n/product-docs closure and Batch 35 real-testing execution: `docs/sources/product-agent-os-track-10-backlog.md` and `docs/sources/registry.md`.
- Batch 35 approval-bound local runtime, browser automation, provider pilot, canonical mutation pilot and git preflight evidence: `docs/sources/product-agent-os-batch35-approval-packet-draft.md`.
- Batch 39 production-test evidence: `prod_test.md` and B39 packets.
- Batch 44/45 and Track 11 evidence: `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`, `docs/product-agent-os/control-plane-current-state.md` and `docs/superpowers/specs/*.json`. Batch 45 compact anchors: `B45-PCA-M37-A01`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`.

## Verification For This EVALS Maintenance

For this control-plane compaction, the required route is:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Full unittest, fixture eval, transcript eval and strict MkDocs are required only if the focused checks expose contract drift or the slice changes plugin/runtime behavior or MkDocs-sensitive site surfaces.

<!-- product-agent-os:end evals -->
