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
- Real-project evidence: deterministic fixtures prove contract shape, but Product-Agent OS product confidence requires real-project target evidence where the route depends on actual project structure, source policy, workflow, runtime signals or owner judgment. Real targets remain read-only unless a separate approval packet names the mutation/runtime surface.
- Approval boundary: live servers, browser automation, provider/live external model/API calls, production data access, canonical graph source mutation, external writes and git stage/commit/push/PR remain approval-bound.
- Documentation quality: user-facing docs are Russian, behavior-level and name inputs, outputs, verification, risks and next artifact.
- Safety: secrets, private data, raw prompts/traces and absolute user-specific paths are not eval fixtures, examples or templates.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, transcript eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive changes, Codex compatibility regression or approval-bound action performed without approval.
- Accepted gap: allowed only when reason, owner, evidence owner, downstream risk and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and the final response.
- Unsupported claim: any quality, readiness, release, security, AI/RAG, runtime or product-success claim without current evidence must be rejected or labeled inspection-only.
- Synthetic-only limitation: internal `codex_docs` fixtures cannot support broad real-project usefulness, product-success, release-readiness, automation promotion or mass-user readiness without representative real-project evidence or an owner-reviewed accepted gap.

## Current Evaluation State

- Task 26 Batch 35 is closed through `T10-LIVE-M41` as `owner_closed_no_op_git_release_pr` under `batch35_approval_bound_real_testing_execution`.
- `T10-LIVE-M41` performed no git stage/commit/push/PR; future git write requires exact release branch or push target, commit message, PR base branch, PR title and intent, explicit branch/current-branch write approval and fresh preflight.
- M41 post-B38 audit: Batch 35 `dirty_file_count: 15` is historical preflight evidence only; B37/B38/B38-S1 did not themselves close M41, while the later owner no-op closure did.
- B38-S2: M04 full verification is implemented; M05 read-only install/cache smoke first found stale visible plugin cache with historical pre-attempt marker `blocked_pending_explicit_cache_mutation_approval`. Owner cache-refresh approval is recorded; backup/stage were prepared; the sandbox write attempt was blocked with `plugin_cache_refresh_attempt_status: blocked_sandbox_cache_write_denied_after_backup_stage`; the owner then ran the prepared local PowerShell refresh successfully. Current evidence is `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`, `local_cache_refresh_result: REFRESH_OK`, `target_cache_files_after_refresh: 586`, `target_cache_skill_count_after_refresh: 11`, `target_cache_docs_maintainer_present_after_refresh: true` and `target_cache_still_stale: false`.
- B38-S3: `B38-PROD-M06..M09` real-project pilot design is implemented as operator packet, target consent matrix, success metrics and dry-run evidence ledger. `no_real_project_execution_performed`; no pilot-success claim is valid without current pilot evidence.
- B38-S4: `B38-PROD-M10..M11` safety and rollback is current. M03 is owner-confirmed local-only/internal R&D distribution, so public/team trust fields remain out of scope until a future release decision. M10 is `reviewed_gap_recorded` and records read-only security/privacy/supply-chain gaps instead of a security-certified readiness claim; M11 documents rollback/remove/cache recovery. A production-pilot or public/team release claim remains invalid without target-specific approval, current pilot evidence, resolved or accepted M10 gaps, real public/team trust fields and rollback evidence.
- B38-PILOT-NF01: the first target-specific docs-only `Neural_Flow` pilot has current read-only evidence. It improves pilot eval confidence for route accuracy and staged-output usefulness, but it is not a product-success, release-readiness or target-apply claim because `source_policy_status: blocked` and target control-plane/source registry gaps remain.
- Batch 39: `B39-S1` foundational local contracts `B39-TEST-M01..M10` have current local evidence for inventory, pilot manifest, command results, target mutation proof, redaction, session visibility, rollup, dashboard projection, failure taxonomy and scorecard gates. `B39-TEST-M11` has current approved `Neural_Flow` read-only target fixture-pack evidence for relative-path/digest/count-only target signals, control-plane presence, design signals and archetype candidates. `B39-TEST-M12` has current synthetic docs-only happy-path evidence for `docs_research`; `B39-TEST-M13` has current expected-block evidence showing `Neural_Flow` is blocked by source policy before clean-positive, target-apply, release-readiness or promotion claims; `B39-TEST-M14` has current synthetic web/frontend contract evidence showing frontend gates are detected and browser/runtime UI proof remains unsupported without approval; `B39-TEST-M15` has current synthetic backend/API contract evidence showing backend/API gates are detected and approval-bound runtime/security/integration claims are blocked by `needs_approval`; `B39-TEST-M16` has current synthetic AI/RAG contract evidence showing AI/RAG, quality-testing and security-sensitive signals are detected and approval-bound live model/provider/vector/eval/grounding claims are blocked by `needs_approval`; `B39-TEST-M17` has current synthetic data/migration contract evidence showing database/data and migration/schema signals are detected and approval-bound live DB, migration execution, production data, backup/restore, rollback, quality, lineage, performance and retention claims are blocked by `needs_approval`; `B39-TEST-M18` has current synthetic PR/review `code_check` evidence showing `pr_review` routing is selected and approval-bound real PR, GitHub, CI, merge, git and release-readiness claims are blocked by `needs_approval`; `B39-TEST-M19` has current synthetic automation/release evidence showing `release_packaging` routing is selected, `delivery_release_operations` is detected, automation remains `candidate_only`, and approval-bound publish, deploy, tag, release creation, package registry, marketplace, external write and active automation claims are blocked by `needs_approval`; `B39-FRIA-M20.1..M20.10` have current first-run analysis packet schema, CLI boundary, adapter, offline renderer, manifest-diff, guardrail, status/rollup, scorecard, docs/registry and `accepted_risk` verification packet evidence showing generated-view-only, no-completion-claim, generated-analysis-only write, provenance/unsupported-claim, page/source digest, previous-baseline comparison, no-secret/no-raw-source/no-local-path, source-policy apply/promotion gate, dashboard/rollup reference, operator-usability scorecard policy, artifact-contract/source-registry visibility and completion-skeptic separation of supported and unsupported claims. Owner clarified that future tests should include real-project target evidence, not only internal `codex_docs` fixtures; `SOL 0.6` is current `B39-TEST-M20` read-only candidate context and must not be modified. This is not full first-run artifact evidence, real-project value, live backend/API behavior, live model quality, grounding quality, provider/runtime behavior, live database safety, migration safety, real PR approval, GitHub check success, merge safety, real release readiness, deploy safety, publication safety, package registry safety, external write safety, active automation readiness or promotion evidence. `B38-PROD-M12` still cannot make a release/readiness recommendation until Batch 39 records complete `prod_test.md` per-test attempt/failure/fix/retest evidence, comparable pilot manifests, command-result evidence, redaction/no-mutation proof, dashboard/rollup evidence, representative archetype coverage or accepted gaps, real-project target evidence where applicable, functional regression/repeatability evidence, public docs/site acceptance, offline/dependency readiness, full CLI contracts, graph extension approval gates, security/privacy/compliance/supply-chain evidence, template/workflow and skill/subagent contract evidence, MCP boundary evidence, onboarding and cross-platform evidence, source freshness, cleanup, incident/recovery and release/distribution governance evidence plus final no-unapproved-actions proof.
- Batch 39 M21: `B39-TEST-M21-A01..A03` adds current three-target plugin/skill evidence. A01 is a synthetic plugin/skill fixture pass/fail contract with 11 generated first-run pages rendered only in a temporary copy; A02 is a `Neural Flow` read-only expected-block/source-policy comparison; A03 is a `SOL` read-only first-run artifact usefulness signal. Evidence refs are `docs/superpowers/specs/batch39-m21-synthetic-plugin-skill-summary.json`, `docs/superpowers/specs/batch39-m21-neural-flow-readonly-summary.json`, `docs/superpowers/specs/batch39-m21-sol-readonly-summary.json` and `docs/superpowers/specs/batch39-m21-three-target-rollup.json`. This evidence supports contract shape, expected-block behavior and inspection-only usefulness; it does not support target apply, runtime/browser/provider behavior, release readiness, promotion or automation readiness.
- Batch 39 M22: `B39-TEST-M22-A01..A03` adds current route-accuracy evidence for generated first-run artifacts and read-only real-target retests. Evidence refs are `docs/superpowers/specs/batch39-m22-route-accuracy-summary.json`, `docs/superpowers/specs/batch39-m22-retest-neural_flow-summary.json`, `docs/superpowers/specs/batch39-m22-retest-sol_0_6-summary.json`, `docs/superpowers/specs/batch39-m22-real-target-retest-rollup.json`, `tests/product_agent_os/test_discovery.py`, `plugins/product-agent-os/scripts/product_agent_os/discovery.py` and `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`. The eval value is narrower but important: generated first-run pages remain orientation-only, `detect_project.py` preserves that boundary, methodology audit does not consume generated analysis as source truth, benchmark/template false positives no longer force PR/native routes, `Neural Flow` remains an expected `ai_eval_regression` source-policy block, and `SOL 0.6` now routes `desktop_local_first` while still blocked by source policy/runtime contract. This does not support release readiness, runtime/browser/provider behavior, target apply, promotion or automation readiness.
- Batch 39 S3: `B39-TEST-M23..M33` adds current functional regression and repeatability evidence. Evidence ref is `docs/superpowers/specs/batch39-s3-functional-regression-summary.json`. The eval value is that generated first-run orientation wording no longer forces AI/security/release methodology gates, real cross-domain signals still route, runtime/browser/provider/git safe-next-action wording remains approval-bound, trimmed status dashboard JSON preserves bounded system hygiene, and focused infrastructure, merge/rollback, source-policy, hygiene, graph, metrics, fixture/transcript, repeatability and full verification suites passed. This is local functional regression evidence only; it does not support B39-S4 hardening closure, real target mutation, runtime/browser/provider behavior, release readiness, promotion or automation readiness.
- Agent lifecycle and control-plane sync: current local agents and packaged Product-Agent OS templates now route Task Brief / Completion Brief through `.codex/config.toml` `[product_agent_os.lifecycle_contract]` plus `[workflows]`; the eval contract fails duplicated lifecycle prose, missing config route, missing visible briefs, or closing a state-changing task without control-plane sync.
- Root `AGENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` are compact control-plane files. They preserve current routing and safety boundaries, not every historical batch result.
- Historical Batch 34E full-site i18n parity and Batch 35 real-testing evidence is source-owned by Track 10 backlog, source registry and dedicated source packets.

## Active Eval Routes

| Change type | Required eval route |
| --- | --- |
| Docs, source registry, control-plane or docs tests | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools\check_docs.py`, `git diff --check` |
| MkDocs navigation, Mermaid, localization, search/sitemap or generated `site/` evidence | Docs route plus strict MkDocs build |
| Plugin scripts, templates, lifecycle skills, runtime behavior or CLI contracts | Focused tests, full unittest, fixture eval, transcript eval, Codex compatibility, docs check and diff hygiene as routed by `TEST.md` |
| Product-Agent OS pilot runner, result collector, dashboard rollup or Batch 39 pilot/hardening matrix | `prod_test.md` attempt/failure/fix/retest ledger review, focused schema/collector/dashboard/route tests, redaction and no-mutation proof, CLI contract checks, graph extension gates, security/privacy/compliance/supply-chain checks, template/workflow and skill/subagent contract checks, fixture eval, transcript eval, docs check and diff hygiene; full plugin verification when runtime/scripts/templates change |
| Agent/control-plane sync contract | Current-project task lifecycle test, packaged infrastructure template test, config-route inspection, agent-context eval contract inspection, docs check and diff hygiene |
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
