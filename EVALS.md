# EVALS.md

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-06-07

## Purpose

`EVALS.md` is the compact evaluation routing layer for the current Product-Agent OS work. It should not store full historical command logs, implementation ledgers or batch marker banks.

Evaluation ownership is distributed as follows:

| EVALS information class | Owning file now |
| --- | --- |
| Current rubrics, thresholds, unsupported-claim rules and eval routing | `EVALS.md` |
| Current verification commands and escalation rules | `TEST.md` |
| Current scope and acceptance baseline | `REQUIREMENTS.md` |
| Current sequencing and rollback | `PLAN.md` |
| Current-cycle handoff and residual risks | `RUNLOG.md` |
| Durable project safety boundaries | `AGENTS.md` |
| Track 8 scenario/methodology eval history | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 methodology eval history | `docs/sources/product-agent-os-track-9-backlog.md` |
| Track 10 execution/eval history | `docs/sources/product-agent-os-track-10-backlog.md` |
| Source-backed claim and verification registry | `docs/sources/registry.md` |
| Batch 35 approval and execution evidence | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Rubrics

- Source grounding: official sources and checked-in docs drive durable rules; community claims stay in insight/research layer.
- Evidence before completion: ready/completed/fixed/works/release claims require current command evidence, current eval evidence, current runtime evidence or an explicit inspection-only gap.
- Conditional applicability: methodology gates can be `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, `applicable_missing` or `approval_required`.
- Owner sufficiency: artifacts prove evidence shape and routing; a human owner still judges whether evidence is sufficient for real project risk.
- Source boundary: generated dashboards, graph outputs, HTML views, scorecards and `site/` builds are orientation evidence unless an owning source document says otherwise.
- Approval boundary: live servers, browser automation, provider/live external model/API calls, production data access, canonical graph source mutation, external writes and git stage/commit/push/PR remain approval-bound.
- Documentation quality: user-facing docs are Russian, behavior-level and name inputs, outputs, verification, risks and next artifact.
- Safety: secrets, private data, raw prompts/traces and absolute user-specific paths are not eval fixtures, examples or templates.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, transcript eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive changes, Codex compatibility regression or approval-bound action performed without approval.
- Accepted gap: allowed only when reason, owner, evidence owner, downstream risk and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and the final response.
- Unsupported claim: any quality, readiness, release, security, AI/RAG, runtime or product-success claim without current evidence must be rejected or labeled inspection-only.

## Current Evaluation State

- Task 26 Batch 35 is closed through `T10-LIVE-M41` as `owner_closed_no_op_git_release_pr` under `batch35_approval_bound_real_testing_execution`.
- `T10-LIVE-M41` performed no git stage/commit/push/PR; future git write requires exact release branch or push target, commit message, PR base branch, PR title and intent, explicit branch/current-branch write approval and fresh preflight.
- M41 post-B38 audit: Batch 35 `dirty_file_count: 15` is historical preflight evidence only; B37/B38/B38-S1 do not close M41, while the owner no-op closure does.
- B38-S2: M04 full verification is implemented; M05 read-only install/cache smoke found stale visible plugin cache and remains `blocked_pending_explicit_cache_mutation_approval`.
- Root `AGENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` are compact control-plane files. They preserve current routing and safety boundaries, not every historical batch result.
- Historical Batch 34E full-site i18n parity and Batch 35 real-testing evidence is source-owned by Track 10 backlog, source registry and dedicated source packets.

## Active Eval Routes

| Change type | Required eval route |
| --- | --- |
| Docs, source registry, control-plane or docs tests | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools\check_docs.py`, `git diff --check` |
| MkDocs navigation, Mermaid, localization, search/sitemap or generated `site/` evidence | Docs route plus strict MkDocs build |
| Plugin scripts, templates, lifecycle skills, runtime behavior or CLI contracts | Focused tests, full unittest, fixture eval, transcript eval, Codex compatibility, docs check and diff hygiene as routed by `TEST.md` |
| AI/RAG behavior, provider gates or model migration | Baseline eval, one focused change, rerun eval, inspect artifacts, record threshold/fallback and approval boundary |
| Frontend/browser/runtime UX | Build/test/lint where available, browser/runtime evidence, console/network checks, responsive/overflow evidence and screenshot/trace evidence or explicit gap |
| Release, external write, automation or git action | Explicit owner approval packet, current evidence, rollback/recovery path and no silent stage/commit/push/PR |

## Methodology Eval Map

| Area | Gate or evidence key | Primary evidence owner |
| --- | --- | --- |
| Track 8 scenario routing | `T8-S16`, `T8-A3..A16`, `T8-B`, `T8-C`, `T8-D`, `T8-F`, `T8-GX`, `T8-GY`, `T8-H` | Track 8 detailed backlog, Product-Agent OS docs and fixture/transcript evals |
| Business/product | `business_product_contract_present` | Track 9 backlog and methodology docs |
| Requirements/domain | `requirements_domain_contract_present`, `domain_model_when_complex_domain`, `bounded_context_architecture_boundary_trace`, `ubiquitous_language_traceability` | Track 9 backlog, methodology docs and generated artifact templates |
| Solution architecture | `solution_architecture_contract_present` | Track 9 backlog and architecture methodology docs |
| Quality/testing/evals | `quality_testing_evals_contract_present`, `evidence_before_completion` | Track 9 backlog, `TEST.md` and fixture/transcript evals |
| Codex/agentic workflow | `codex_agentic_workflow_contract_present`, fresh-context handoff, skill/plugin/automation routing | Track 9 backlog, Product-Agent OS plugin skills and control-plane docs |
| Frontend | `frontend_contract_present`, responsive/runtime/visual evidence | Track 9 backlog and frontend methodology docs |
| Backend | `backend_contract_present`, runtime/failure/observability/rollback evidence | Track 9 backlog and backend methodology docs |
| API/integrations | `api_integrations_contract_present`, contract/security/consumer evidence | Track 9 backlog and API methodology docs |
| Database/data | `database_data_contract_present`, migration/rollback/privacy/lineage evidence | Track 9 backlog and database/data methodology docs |
| LLM/AI/RAG | `llm_ai_rag_contract_present`, baseline/rerun/grounding/tool/guardrail evidence | Track 9 backlog and AI/RAG methodology docs |
| Security/privacy/compliance | `security_privacy_compliance_contract_present`, security evidence before completion | Track 9 backlog and security methodology docs |
| Delivery/release/operations | `delivery_release_operations_contract_present`, release evidence before completion | Track 9 backlog and delivery methodology docs |
| Cross-domain synthesis | `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered` | Track 9 backlog and runtime runner evidence |
| Track 10 guided questions/dashboard | `T10-Q-M15..M25`, question queue, status snapshot, generated dashboard, stale-evidence guard | Track 10 backlog and Product-Agent OS docs |
| Track 10 self-verification | `T10-SV-M58..M62`, `agent_skill_metrics_loop`, scorecards, candidates, no active automation | Track 10 backlog and metrics-loop source packets |
| Track 10 project graph | `T10-CG-V2-M01..M62`, generated graph/cockpit/search/backend/semantic/LLM proposal/extension closure gates | Track 10 backlog, registry and graph source packets |
| Track 10 live layer | `T10-LIVE-M01..M41`, approval-bound live/runtime/provider/mutation/git gates | Track 10 backlog, registry and Batch 35 packet |
| Full-site i18n and product docs | `B34E-I18N-M34..M49`, language switcher/search/sitemap parity, public forbidden-term gates | Track 10 backlog and Batch 34 source packets |

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

## Historical Eval Evidence Owners

- Track 8 scenario, readiness, false-positive and transcript/session evidence: `docs/sources/product-agent-os-track-8-detailed-backlog.md`.
- Track 9 methodology intelligence evidence across all 12 domains, synthesis and runtime runner: `docs/sources/product-agent-os-track-9-backlog.md` and `docs/sources/registry.md`.
- Track 10 Task 23 through Task 26 evidence, including project graph, live-layer gates, Batch 34 docs/i18n/product-docs closure and Batch 35 real-testing execution: `docs/sources/product-agent-os-track-10-backlog.md` and `docs/sources/registry.md`.
- Batch 35 approval-bound local runtime, browser automation, provider pilot, canonical mutation pilot and git preflight evidence: `docs/sources/product-agent-os-batch35-approval-packet-draft.md`.

## Verification For This EVALS Maintenance

- Current run: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` first exposed stale historical `EVALS.md` aggregate expectations; after compact eval ownership sync it ran 59 tests with `OK`. `python tools\check_docs.py` returned `OK: documentation structure checks passed`; `git diff --check` exited `0`.
- Focused docs contract: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`.
- Documentation structure: `python tools\check_docs.py`.
- Diff hygiene: `git diff --check`.
- Full unittest, fixture eval, transcript eval and strict MkDocs are not required for a docs/control-plane-only compaction unless the focused checks expose contract drift or MkDocs-sensitive files change.
<!-- product-agent-os:end evals -->
