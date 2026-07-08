# Текущий control-plane state

Source status: `experiment`

Эта страница является site-facing owner artifact для холодной истории и detailed
evidence, которые больше не должны жить в root `PLAN.md`, `RUNLOG.md`,
`TEST.md` и `EVALS.md`. Root control-plane files остаются компактными
диспетчерами: они показывают текущий маршрут, verification gates, claim ceilings
и pointers на эту страницу, source registry, track backlogs и evidence packets.

## Source Matrix

| Source | Claim | Relevance | Freshness | Confidence | Conflicts |
| --- | --- | --- | --- | --- | --- |
| `PLAN.md` | Root план хранит текущую очередь, rollback и source pointers. | Сокращается до active routing. | Current run, 2026-07-08. | High. | Исторические batch matrices должны уйти из root. |
| `RUNLOG.md` | Root runlog хранит current handoff, latest evidence и residual risks. | Сокращается до current-cycle summary. | Current run, 2026-07-08. | High. | Long evidence ledgers должны быть source-owned. |
| `TEST.md` | Root test file хранит routing для проверок, не batch command archive. | Сокращается до командных классов и ownership. | Current run, 2026-07-08. | High. | Batch-specific длинные suites живут в packets/backlogs. |
| `EVALS.md` | Root evals хранит rubrics, thresholds и active claim ceilings. | Сокращается до текущих eval routes. | Current run, 2026-07-08. | High. | Historical eval state живет в source/spec artifacts. |
| `docs/sources/registry.md` | Registry является source-backed claim index. | Ведет к конкретным source artifacts. | Current workspace. | High. | Generated `site/` не является source truth сам по себе. |
| `docs/superpowers/specs/*.json` | Evidence packets являются owner artifacts для batch details. | Замещают detailed ledgers из root files. | Current workspace. | High. | Каждый packet имеет собственный claim ceiling. |

## Root File Contract

| Root file | Оставить в root | Вынести сюда или в source artifacts |
| --- | --- | --- |
| `PLAN.md` | Active sequencing, next queue, rollback, source pointers. | Старые batch tables, detailed row matrices, long evidence lists. |
| `RUNLOG.md` | Latest handoff, current residual risks, latest verification summary. | Historical attempt/failure/fix ledgers and batch marker banks. |
| `TEST.md` | Required command routes, escalation boundaries, current verification state. | Batch-specific command archives and old completed check logs. |
| `EVALS.md` | Rubrics, thresholds, active eval routes and unsupported-claim rules. | Historical eval evidence narratives and long batch state. |

Size pressure is `overflow_refactor_required`: move cold detail to the owning
source artifact first, then keep the root file current. It is never permission
to skip a required control-plane update.

## Current Product-Agent OS State

| Workstream | Current state | Root pointer |
| --- | --- | --- |
| Track 9 / Track 10 history | Source-owned historical context. Use the detailed backlogs and registry for completed methodology and execution history. | `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/product-agent-os-track-10-backlog.md`. |
| Batch 35 / Batch 38 | `T10-LIVE-M41` is owner-closed as `owner_closed_no_op_git_release_pr`; B38 cache refresh is historical/current evidence according to registry entries. | `docs/sources/product-agent-os-batch35-approval-packet-draft.md`, registry. |
| Batch 39 | Closed for owner-feedback testing only. Release/distribution is `no_go`; runtime/browser pilot is `approval_required`; target projects remain read-only unless separately approved. | `prod_test.md`, `docs/superpowers/specs/batch39-s5-closure-summary.json`. |
| Batch 40 | Completion-skeptic local manual foundation closed as `manual_only` and `not_promoted`. | `docs/sources/product-agent-os-batch40-doubt-verifier-pilot-closure.md`. |
| Batch 41 | First-run cockpit work through S9 is local/read-only/staged/generated-artifact evidence. It does not prove release readiness, target apply safety, automation promotion or Cosmos.gl/WebGL runtime execution. | `docs/superpowers/specs/batch41-s9-html-modernization-summary.json`. |
| Batch 42 | Instruction/tool-use compliance remains planned-only until execution evidence exists. | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`. |
| Batch 44 | Self-Learning Loop S0-S7 is local/schema/fixture/staged manual evidence. S8 remains the closure/promotion decision route; no active automation or auto-apply is proven. | `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`. |
| Batch 45 | Professional Code Authoring remains advisory/no-go. `B45-POSTQ4-T15` records that T14 is a positive current-quality signal only: `gpt-5.5`, 16/16, `+3.27%`, reviewer `0`, below `>=20%`, and same-model comparability is false. `B45-POSTQ4-T20-A01` stages exact owner approval text with current pricing/USD cap for the same-model promotion-grade route; `owner_confirmed=false`, `run_authorized_by_this_artifact=false`, and it does not run baseline/treatment, reviewer/model/provider calls or reverse M26/M35/T15. | `docs/superpowers/specs/batch45-postq4-t15-model-change-decision-packet.json`, `docs/superpowers/specs/batch45-postq4-t16-t22-promotion-grade-eval-task-group.json`, `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json`, `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json`, `docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json`, `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet.json`. |
| Track 11 docs/site | DOC-M25 generated-site freshness packet records the approved root site/search/sitemap refresh; browser proof, broad scans, remediation, raw retention, publication, release/deploy and git actions remain separate. | `docs/superpowers/specs/documentation-refresh-doc-m25-site-freshness-summary.json`. |

## Current Queue

1. Keep root control-plane files compact after every non-mechanical slice.
2. For Batch 44, review S7 manual-pilot evidence before any S8 promotion decision.
3. For Batch 45, continue the `B45-S8` promotion-grade eval route in order only:
   T17 frozen corpus manifest done -> T18 design/schema done -> T19 cost/timeout/retention done -> T20 exact approval packet done but owner confirmation required
   -> approved T21 run -> T22 reviewer decision. Until that route clears threshold and
   reviewer gates, keep advisory/no-go.
4. For Track 11, keep source docs, registry, generated site evidence and
   approval-bound browser/broad-scan claims separate.

## Evidence Owners

| Evidence class | Owner |
| --- | --- |
| Source-backed claim registry | `docs/sources/registry.md`, `docs/sources/registry.en.md` |
| Track 8 history | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 history | `docs/sources/product-agent-os-track-9-backlog.md` |
| Track 10 history | `docs/sources/product-agent-os-track-10-backlog.md` |
| Batch 35 approval/closure | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |
| Batch 39 detailed production-test ledger | `prod_test.md` |
| Batch 41, 44, 45 evidence packets | `docs/superpowers/specs/*.json` |
| Current root routing | `PLAN.md`, `RUNLOG.md`, `TEST.md`, `EVALS.md` |

## Verification Routes

Use these checks after control-plane or docs changes:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs when navigation, localized pages, search/sitemap or generated
`site/` evidence changes. Full discovery remains the broad regression route:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Unsupported Claims

Эта страница не доказывает runtime/browser/provider поведение, безопасность
мутации target workspace, активную automation, выполнение hooks в новой trusted
session, release readiness, publication readiness, git release/PR action,
production readiness или public docs acceptance за пределами конкретных source
packets, перечисленных выше.


## Pre-Compaction Root Marker Archive

This appendix preserves the cold marker text that was moved out of root control-plane files on 2026-07-07. It is historical/search context only and does not override the compact current-state tables above.


### Archived PLAN.md

```text
# PLAN.md

<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Purpose

`PLAN.md` is the compact sequencing and rollback layer for current Product-Agent OS work. It points to source-owned plans/backlogs for detailed history and keeps active execution boundaries visible.

## Current Planning Contract

- Work in focused slices with explicit scope, acceptance criteria, risks, rollback and verification gates.
- Use Product-Agent OS skills for requirements, implementation planning, test/eval design, docs maintenance, risk review and completion-skeptic loops when the task matches them.
- Keep historical batch matrices in source-owned files, not in this root plan.
- Do not create/switch branches, stage, commit, push, open PRs, mutate target workspaces, run browser automation, call providers/live APIs, publish, deploy or create automations without exact approval for that action.
- For Product-Agent OS pilots, prefer real-project target evidence where it improves confidence. Keep `codex_docs` as the control-plane, runner and evidence workspace; keep target projects read-only unless a test row names an approved mutation surface, rollback and owner.
- Preserve unrelated dirty work and record only the evidence needed for current handoff.

## Current State

| Workstream | State | Planning impact |
| --- | --- | --- |
| Track 9 / Track 10 history | Source-owned and closed for completed historical slices. | Use backlogs and registry for historical detail. |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no branch, stage, commit, push or PR. | Future git-write work needs fresh preflight and exact approval. |
| Batch 38 package-source/readiness | Implemented/recorded. `B38-S2` current cache evidence is `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat prior blockers as historical evidence, not current active blockers unless the same condition recurs. |
| `B38-PILOT-NF01` | Docs-only target addendum completed; target apply blocked by `source_policy_status: blocked` and missing target control-plane/source registry artifacts. | Do not mutate target project until source policy and artifacts are resolved. |
| Batch 39 | Executed through `prod_test.md`; `B39-S1` foundational local contracts, `B39-S2` archetype/first-run/three-target evidence, `B39-S3` functional regression/repeatability, `B39-S4` hardening and `B39-S5` closure/go-no-go are recorded through `B39-S5-CLOSURE-A01`. `B39-S5` consumes S4 blockers into a `release=no_go`, `owner_feedback_testing=conditional_go`, `runtime_browser_pilot=approval_required` decision. | Start owner-feedback testing manually from the S5 test plan. No release/readiness claim until owner feedback and any approval-gated runtime/browser evidence exist. |
| Batch 39 real-project targets | Owner clarified that future Product-Agent OS testing should run on real projects, not only internal `codex_docs` fixtures. `SOL 0.6` is the current `B39-TEST-M20` candidate context as a local-first web-desktop target, but it must not be modified. | Use real targets for read-only discovery and evidence first; record target labels, relative paths, counts, digests and approval boundaries in `codex_docs`. Runtime/browser/provider/git/external actions need separate exact approval. |
| Batch 40 completion-skeptic | Local manual foundation closed; automation status `manual_only` and `not_promoted`. | Keep automation promotion candidate-only until gates are satisfied. |
| Batch 41 first-run orchestration | `B41-S1-M01..M05` command/UX contract, `B41-S2-M06..M09` help-only script matrix, `B41-S3-M10..M16` project-analysis summaries, `B41-S4-M17..M20` HTML artifact integration, `B41-S5-M21..M23` guided question UX and `B41-S6-M24..M30` closure evidence are recorded as local/read-only/staged behavior. Owner review of the Neural_Flow artifact exposed a product UX failure: the current HTML is structurally valid but reads as raw white-page diagnostic output. `B41-S7-M31..M39` implements the corrective cockpit foundation, graph rendering and local UX/safety hardening. `B41-S7-M40` regenerated the Neural_Flow cockpit artifact, captured Playwright screenshots, passed static runtime interaction, console/network and WCAG-oriented browser checks, and fixed the canonical visible `generated-view-only` label. A later owner design review rejected the current HTML as still not architecture-rich or designed enough, so `B41-S8-M41..M47` is now planned for architecture-dossier redesign, diagram layer, visual shell, evidence/decision sections, graph runtime/fallback clarity, Playwright visual/a11y acceptance and regenerated Neural_Flow before/after proof. | Treat S6 closure as no-go for release/readiness. M40 supports conditional static Neural_Flow acceptance only. S8 is the active planned corrective route for design quality and architecture diagrams; Cosmos.gl runtime/WebGL execution remains blocked unless a later vendored-runtime slice is approved. Release/git/provider/external writes and target source mutation remain out of scope without separate approval. |
| Batch 42 instruction/tool-use compliance | Owner-requested planning matrix added for Product-Agent OS auto-engagement, skill exposure, implicit invocation policy, route/eval hardening, staged `self-learning-loop` and system-file hygiene triage. Source matrix: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; Track 10 source addendum: `docs/sources/product-agent-os-track-10-backlog.md`. | Planned-only. Do not claim auto-engagement is fixed until Batch 42 execution produces source/cache/session inventory, official-doc source status, route/eval evidence, fresh-session proof if required and no-unapproved-actions closure. Global config writes, installed-cache refresh, browser/provider/git/external actions, target mutation and automation activation require separate exact approval. |
| Batch 44 Self-Learning Loop | `B44-S0` through `B44-S7` are implemented as local/schema/fixture/docs/staged-manual-pilot evidence: scoped discovery, state/trigger UX, staged manual runner/progress, feedback/preferences, metrics/evals, candidate-only safety, docs/contracts/closure, stage-only state initializer, explicit staged state runner path, durable eval taxonomy, Promptfoo export, HALO-style recommendation packet and staged repair worker contract. `B44-S7-SELF-LEARNING-MANUAL-PILOT-A01` records approved manual pilot evidence. | Continue with `B44-S8` closure/promotion decision only after owner review of S7 evidence. Do not activate scheduler/hooks/Codex App automation, global session analysis, raw private ingestion, real session import without consent, Promptfoo/provider/model/HALO calls, target mutation, git/release/deploy/publish, external writes or auto-apply. |
| Batch 45 Professional Code Authoring | `B45-S0..S5` are implemented as source-owned docs/contract/synthetic evidence for the professional coding synthesis, activation policy, core checklist/workflow, existing workflow/agent/skill retrofit, behavioral evals, readiness/discovery/runtime-route/HTML/status visibility, candidate-only hook governance, public RU/EN coding standards page, nav/source cross-linking, focused regression tests, learning-loop/automation-candidate policy and full Batch 45 source closure after `B45-PCA-M23`. `B45-PILOT-MANUAL-6-CODE-TASKS-A02` extends the owner-approved local manual pilot to six real non-mechanical code tasks. `B45-PCA-M24-A01` records the S6 broad false-positive audit; `B45-PCA-M24-TUNING-A02` records scoped default tuning; `B45-PCA-M25` records approved local non-blocking `PostToolUse` advisory wiring; `B45-PCA-M26` records approved live held-out baseline/treatment eval with `no_go_real_behavior_improvement_not_proven_after_live_eval`; `B45-PCA-M27` records the final keep-advisory-only/no-go promotion decision. Evidence: `docs/superpowers/specs/batch45-comment-sufficiency-false-positive-audit.json`, `docs/superpowers/specs/batch45-comment-sufficiency-tuning-comparison.json`, `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json`, `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`, `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json` and earlier B45 packets. | Preserve Batch 45 as source/evidence-bound only. M24/M25 prove advisory mechanics; M26 ran approved live baseline/treatment model eval on 8 held-out tasks: baseline avg `4.22`, treatment avg `3.88`, 15/16 task runs completed, 1 timeout, advisory warnings fell `29 -> 15`, and the independent reviewer decision is `no_go`. `B45-S6` is closed only as advisory/no-go decision evidence: M25 remains local, non-blocking and reversible; M27 rejects stronger advisory, CI workflow creation and blocker enforcement. Do not claim real AI-agent behavior improvement, active automation, schedule creation, browser/runtime proof, plugin-cache refresh, target mutation, root site freshness for the updated page, git/release/deploy/publish or production readiness from S0-S6 evidence. Future provider/model reruns still require exact approval. |
| Batch 45 S7 real-project scenario harness and M37 remediation | `B45-PCA-M28..M35` now has source-owned architecture v2, read-only scenario inventory/rereview, sanitized fixture policy, two `analysis_only` fixture packs, fixture-local baseline evidence, refactor-arm comparison, promotion-risk scorecard and post-real-project decision packet for `SOL-AGENT-ORCH-01` and `MP-CRM-CHAT-OPEN-01`. `B45-PCA-M37-A01` adds local hook/validator hardening plus review remediation docs/control-plane/source sync; `B45-PCA-M36` remains reserved for optional runtime/browser approval packet. Evidence: `research/batch45-professional-code-authoring-architecture-v2.md`, `research/b45-real-project-scenarios/`, `docs/superpowers/specs/batch45-real-project-baseline-results.json`, `docs/superpowers/specs/batch45-real-project-refactor-comparison.json`, `docs/superpowers/specs/batch45-real-project-scorecard.json`, `docs/superpowers/specs/batch45-real-project-decision-packet.json`, `docs/superpowers/specs/batch45-review-remediation-summary.json` and per-scenario packets. | Treat S7/M37 evidence as fixture-local/source-only/local-advisory-hardening evidence. M37 hardens only the local non-blocking advisory path with TS/TSX scanning, fail-open diagnostics, redacted paths and active/template hook parity; it does not change promotion state. M35 keeps advisory-only/no-go for treatment v2 promotion; smaller treatment v2 is source-only future design, more fixture pilots are deferred, disposable runtime/browser pilot is approval-required, and CI/blocker promotion is rejected. Do not run target commands, mutate targets, launch runtime/browser, call providers/live APIs, use production/local databases, stage/commit/push/PR, deploy, publish or activate automation without fresh exact approval. |
| Batch 45 retest Q0-Q2 | `B45-RETEST-Q0-Q2-A01` source-owns the protocol in `docs/superpowers/specs/batch45-quality-retest-protocol.json`: Q0 source freeze, Q1 held-out tasks, Q2 harness schema. | Local/static route only; M26/M27/M35/M37 remain active. No live/model/runtime/browser/provider/target/CI/git/release/deploy/automation. |
| Batch 45 retest Q3 fixture-static | `B45-RETEST-Q3-FIXTURE-STATIC-A01` source-owns the 37-file sanitized fixture replay in `docs/superpowers/specs/batch45-quality-retest-fixture-static-summary.json`: 14 advisory warnings, `blocking=false`. | Local/static evidence only; keep `continue_investigation_keep_advisory_only_no_go`. Live/model and `B45-PCA-M36` remain approval-required. |
| Batch 45 retest Q4 project-slices-static | `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01` source-owns five sanitized slices in `docs/superpowers/specs/batch45-quality-retest-project-slices-static-summary.json`: 46 files, 14 advisory warnings, `blocking=false`. | Static slice localization only; M26/M27/M35/M37 stay active. `B45-RETEST-Q5-LIVE-MODEL-RERUN` and `B45-PCA-M36` remain approval-required. |
| Batch 45 post-Q4 T01-T20 | `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01/RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01` and `B45-POSTQ4-T20-A01` cover static `14 -> 0`, T05 timeout, T12 no-go, T13/T14, T15 model-change decision, T16-T22 route design, T17 frozen corpus manifest, T18 eval design/schema, T19 cost/timeout/raw-temp-only retention and T20 exact approval packet. | T20 is approval-packet/no-run: owner has not restated the exact text, so there is no baseline/treatment execution, reviewer/model/provider call, promotion or M26/M35/T15 reversal. |
| Agent lifecycle hooks and control-plane sync | Current project agents and Product-Agent OS templates route Task Brief / Completion Brief and control-plane sync through `.codex/config.toml` `[product_agent_os.lifecycle_contract]` plus `[workflows]`; project-local `.codex/hooks.json` is now installed through `product_agent_os_LIFECYCLE-HOOKS-A01`, with scripts and the Product-Agent OS policy mirror under `.codex/hooks/`. `PreToolUse` keeps the marker guard for mutating commands. | Future Product-Agent OS tasks must show the visible Task Brief, record `.codex/product-agent-os/lifecycle-state.json` before mutating execution, then run control-plane sync and show Completion Brief. Codex may require `/hooks` trust review or a new session before the installed non-managed hooks execute. |
| Track 11 G1.1 documentation toolchain | Active control-plane implementation route for project-local docs tooling. `DOC-M34` implements the contract-only folder/config boundary; `DOC-M35` has project-local MkDocs runtime evidence through `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`; `DOC-M36` has project-local Node docs tooling evidence through `documentation_refresh_G1_1-DOC-M36-NODE-A01`; `DOC-M37` has project-local Vale language-guard evidence through `documentation_refresh_G1_1-DOC-M37-VALE-A01`; `DOC-M38` has project-local lychee/gitleaks evidence through `documentation_refresh_G1_1-DOC-M38-LINK-SECRET-A01`; `DOC-M39` has vendored Mermaid evidence through `documentation_refresh_G1_1-DOC-M39-MERMAID-A01`; `DOC-M40` has audit/SBOM governance evidence through `documentation_refresh_G1_1-DOC-M40-AUDIT-SBOM-A01`; `DOC-M41` has deferred Docusaurus, Storybook and Structurizr DSL trigger governance through `documentation_refresh_G1_1-DOC-M41-DEFERRED-PLATFORMS-A01`; `DOC-M25` is deferred to the final `G5` row after G2-G5 source updates. | Continue in approval-bounded slices: use `.venv-docs\Scripts\python.exe` for MkDocs checks, `npm.cmd --prefix .docs-tools\node run ...` for Node docs-tooling checks, `.docs-tools\bin\vale.exe --config=.vale.ini ...` for advisory language checks, `.docs-tools\bin\lychee.exe --offline ...` / `.docs-tools\bin\gitleaks.exe dir ... --redact ...` only for approved scoped checks, `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js` only as static MkDocs vendor evidence unless browser proof is explicitly approved, and `tools\docs_dependency_audit.ps1` for local dependency inventory/SBOM governance. Root `site/` freshness is a final `DOC-M25` gate after G2-G5 unless separately approved earlier; browser Mermaid rendering proof, broad docs autoformat/lint, Redocly enforcement, broad Vale enforcement, external URL crawling, broad link/secret scans, raw report retention, Python vulnerability audit, dependency remediation, Docusaurus/Storybook/Structurizr installation and docs automation remain unclaimed until their own approved slices run. |
| Track 11 G2 first-run cockpit and artifact docs | Implemented through `documentation_refresh_G2-A01`: `DOC-M04`, `DOC-M05`, `DOC-M06`, `DOC-M19`, `DOC-M20` and `DOC-M33` now have source docs, RU/EN parity, nav/check_docs/test sync and registry markers. | Continue with G3-G5 source/docs slices; keep `docs/product-agent-os/first-run-architecture-cockpit.md` in `DOC_M25_PENDING_SITE_PAGES` until final root `site` rebuild/search/sitemap freshness runs under `DOC-M25`. |
| Track 11 G3 diagram atlas and architecture maps | Implemented through `documentation_refresh_G3-A01`: `DOC-M07`, `DOC-M08`, `DOC-M09`, `DOC-M10` and `DOC-M23` now have RU/EN diagram pages, diagrams index routing, MkDocs nav, check_docs/test sync and registry markers. | Continue with G4-G5 source/docs slices; keep the new G2/G3 pages in `DOC_M25_PENDING_SITE_PAGES` until final root `site` rebuild/search/sitemap freshness runs under `DOC-M25`; browser proof and Structurizr DSL remain approval-required/uninstalled. |
| Track 11 G4 operator flows and system behavior docs | Implemented through `documentation_refresh_G4-A01`: `DOC-M11`, `DOC-M12`, `DOC-M26`, `DOC-M27`, `DOC-M31` and `DOC-M32` now have RU/EN source docs, Product-Agent OS route updates, CLI/methodology sync, MkDocs nav, check_docs/test sync and registry markers. | Continue with G5 source/docs slices; keep the new G2/G3/G4 pages in `DOC_M25_PENDING_SITE_PAGES` until final root `site` rebuild/search/sitemap freshness runs under `DOC-M25`; auto-engagement/cache/global config/fresh-session proof remains unsupported. |
| Track 11 G5 evidence quality and final site gate docs | Implemented through `documentation_refresh_G5-A01`: `DOC-M21`, `DOC-M24`, `DOC-M28`, `DOC-M29` and `DOC-M30` now have RU/EN source docs, Product-Agent OS route updates, MkDocs nav, check_docs/test sync and registry markers; `DOC-M25` remains `approval_required_not_run`. | DOC-M25 remains approval_required_not_run until owner approves a final root `site` rebuild/search/sitemap freshness slice; keep the new G2/G3/G4/G5 pages in `DOC_M25_PENDING_SITE_PAGES`, and keep browser proof, broad scans, remediation and raw report retention approval-required. Evidence: `docs/superpowers/specs/documentation-refresh-g5-evidence-quality-site-gate-summary.json`. |
| Track 11 DOC-M25 generated site freshness | Implemented through `documentation_refresh_DOC-M25-A01`: root `site`, search and sitemap now cover the former `DOC_M25_PENDING_SITE_PAGES` set after the owner-approved root MkDocs build. | Keep browser proof, broad scans, dependency remediation, raw report retention, publication, release, deploy and git actions separate. Evidence: `docs/superpowers/specs/documentation-refresh-doc-m25-site-freshness-summary.json`. |

## Next Implementation Queue

| Slice | Scope | Owner action | Codex action | Verification |
| --- | --- | --- | --- | --- |
| `B39-S1` | Foundational local evidence package closed for `B39-TEST-M01..M10`. | Review only if S1 evidence needs rework. | Preserve S1 artifacts as source evidence; do not promote to readiness by themselves. | `prod_test.md` attempt rows, focused tests and synthetic artifacts exist; no target mutation occurred. |
| `B39-S2` | First approved Batch 39 subset is recorded through `B39-TEST-M21-A01..A03` with accepted gaps for generated-view-only, read-only real-target evidence and unsupported release/readiness claims. | Review accepted gaps if they affect product confidence; approve any escalation beyond read-only target discovery. | Preserve S2 evidence in `codex_docs`; do not modify `SOL 0.6`, `Neural Flow` or any target without exact approval. | Deterministic commands and manual evidence recorded in `prod_test.md`; target mutation proof and redaction/no-raw-source rules apply. |
| `B39-S3` | Functional regression and repeatability is closed through `B39-TEST-M23..M33`. M23/M24/M28 added new fixes; M25-M27/M29-M32 focused subsystem suites passed; M33 full verification passed. | Review S3 residual risks and approve any escalation beyond local code/tests or read-only target discovery. | Preserve S3 evidence and do not convert it into release/readiness proof. | `docs/superpowers/specs/batch39-s3-functional-regression-summary.json`; full unittest discover 949 OK / 1 skipped; fixture eval 91/91; transcript eval 26/26; Codex compatibility compatible; docs/check/diff OK. |
| `B39-S4` | Production/mass-user hardening has been executed through current local/read-only/contract gates with explicit expected blockers. The remaining blockers are not hidden: MkDocs is unavailable for fresh public site acceptance, runtime/browser proof needs exact disposable target approval, MCP/Context7 live calls need approval, and release/distribution is held for B39-S5. | Review expected blockers and decide which approval-gated real pilot to run after B39-S5. | Preserve S4 evidence; do not claim release readiness, runtime/browser behavior or promotion. | `docs/superpowers/specs/batch39-s4-all-script-cli-matrix.json`; `docs/superpowers/specs/batch39-s4-full-hardening-comparison.json`; `docs/superpowers/specs/batch39-s4-remaining-gates-summary.json`; `docs/superpowers/specs/batch39-s4-closure-readiness-matrix.json`; plus graph-depth and M37-M39 artifacts. |
| `B39-S5` | Closure and next-route decision is recorded as `closed_for_owner_feedback_testing_not_release_ready`. | Review the S5 owner-feedback scenarios and decide which manual test to run first. | Preserve S5 artifacts and keep release/runtime/browser/provider/external actions approval-gated. | `docs/superpowers/specs/batch39-s5-closure-summary.json`; `batch39-s5-go-no-go-decision-packet.json`; `batch39-s5-no-unapproved-actions-proof.json`; `batch39-s5-owner-feedback-test-plan.json`; focused S5 tests. |
| `B41-S1` | First-run command/UX contract implemented for `B41-S1-M01..M05`. | Review B41-S1 behavior only if CLI wording or write boundary should change. | Preserve implemented source evidence; do not claim full B41, real-target pilot, runtime/browser proof or plugin-cache readiness. | `docs/superpowers/specs/batch41-s1-command-contract-summary.json`; focused B41/first-run tests; docs contract tests. |
| `B41-S2` | Help-only all-script registry and safe command matrix implemented for `B41-S2-M06..M09`. | Review approval-gated classification if any skipped script should later get a narrower read-only mode. | Preserve `partial_with_skips` evidence and continue with S3 integrations. | `docs/superpowers/specs/batch41-s2-script-matrix-summary.json`; focused B41 tests. |
| `B41-S3` | Bounded project-analysis summaries implemented for `B41-S3-M10..M16`. | Review whether the first-run packet answers the expected product questions before HTML integration. | Preserve source-policy blocks, graph orientation-only status, static dependency boundary and runtime/browser `approval_required` status. | `docs/superpowers/specs/batch41-s3-project-analysis-summary.json`; focused B41 tests. |
| `B41-S4` | HTML artifact integration implemented for `B41-S4-M17..M20`. | Review generated artifact usefulness and decide whether guided question UX should ask first or render first in ambiguous projects. | Preserve generated-view-only status, baseline comparison visibility and cleanup preview-only boundary; continue with S5. | `docs/superpowers/specs/batch41-s4-html-artifact-summary.json`; focused B41 and first-run renderer tests. |
| `B41-S5` | Guided question UX and answer-ledger routing implemented for `B41-S5-M21..M23`. | Review whether the first response and route options are useful before real-target pilots. | Preserve one-blocking-question maximum, staged-only answer ledger and generated-view-only status; continue with S6. | `docs/superpowers/specs/batch41-s5-guided-questions-summary.json`; focused B41 tests. |
| `B41-S6` | First-run QA/closure evidence recorded for `B41-S6-M24..M30`: M24 synthetic E2E passed, M25 Neural_Flow read-only expected block passed, M26 app-like pilot timed out before clean static evidence, M27 scorecard is owner-feedback pending, M28 verification sweep packet exists, M29 installed plugin cache readiness is approval-required, and M30 records no-go closure. | Review S6 artifacts and choose the next approval-gated route: owner feedback, disposable runtime/browser pilot, plugin cache refresh, or narrower app-like target retest. | Do not claim release readiness, runtime/browser behavior, provider/API quality, target apply safety or installed-plugin readiness from S6 evidence. | `docs/superpowers/specs/batch41-s6-closure-summary.json`; `docs/superpowers/specs/batch41-s6-real-target-pilots-summary.json`; `docs/superpowers/specs/batch41-s6-plugin-cache-readiness.json`; focused S6 tests and final verification sweep. |
| `B41-S7` | `B41-S7-M31..M40` implemented the cockpit foundation, graph rendering, static UX controls, progressive diagnostics, static visual QA, offline/privacy/accessibility hardening and the owner-approved Neural_Flow acceptance pilot after owner review of the white-page output. Playwright evidence captured desktop/mobile screenshots, static interaction, clean console/network and WCAG-oriented browser checks. `Cosmos.gl` remains the selected graph visualization library, but runtime WebGL execution is blocked by missing vendored runtime asset and script-free static fallback. | Decide whether a later slice should vendor and verify Cosmos.gl runtime/WebGL execution, or keep M40 as conditional static acceptance. | Convert first-run HTML from diagnostic multi-page output into one primary offline cockpit artifact with navigation, project/source graph, code graph where available, Cosmos.gl rendering boundary, progressive disclosure and visual QA. | `docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json`; `docs/superpowers/specs/batch41-s7-m34-m35-graph-rendering-summary.json`; `docs/superpowers/specs/batch41-s7-m36-m39-cockpit-ux-safety-summary.json`; `docs/superpowers/specs/batch41-s7-m40-owner-approval-packet.json`; `docs/superpowers/specs/batch41-s7-m40-neural-flow-acceptance-summary.json`; `docs/superpowers/specs/batch41-s7-m40-neural-flow-stage/`; `output/playwright/b41-s7-m40/playwright-runtime-proof.json`; `docs/superpowers/specs/batch41-s7-html-cockpit-analysis.txt`; `docs/superpowers/specs/batch41-first-run-automation-matrix.json`; focused B41/first-run tests. |
| `B41-S8` | Corrective architecture-dossier redesign after owner rejected the current M40 HTML as still too text-file-like and missing project architecture diagrams. `B41-S8-M41` is implemented as design-contract-only. `B41-S8-M42` is implemented as a static architecture diagram layer. `B41-S8-M43` is implemented as an architecture-dossier shell with first-viewport identity, target context, next route, architecture signal, proof strip and desktop/mobile Playwright proof. `B41-S8-M44` is implemented as visible evidence/decision/risk/source-blueprint acceptance surfaces with desktop/mobile Playwright proof. `B41-S8-M45` is implemented as explicit Graphology/Cosmos.gl static-vs-runtime boundary labeling with desktop/mobile Playwright proof and no WebGL runtime claim. `B41-S8-M46` is implemented as Playwright visual/interaction/accessibility-oriented acceptance with screenshots and explicit WCAG-certification non-claim. `B41-S8-M47` is implemented with regenerated Neural_Flow before/after proof and staged redesigned artifact evidence. | S8 is implemented with accepted gaps: final owner visual acceptance remains pending, Cosmos.gl/WebGL runtime execution remains blocked by static fallback, and WCAG certification/release readiness/target apply safety are not claimed. | Use the M41 design artifact, M42 diagram layer, M43 shell, M44 evidence-decision layer, M45 graph-runtime boundary, M46 visual proof and M47 Neural_Flow before/after proof as the current architecture-dossier evidence set. | `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-artifact.txt`; `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-summary.json`; `docs/superpowers/specs/batch41-s8-m42-architecture-diagram-layer-summary.json`; `docs/superpowers/specs/batch41-s8-m43-cockpit-shell-redesign-summary.json`; `docs/superpowers/specs/batch41-s8-m44-evidence-decision-risk-summary.json`; `docs/superpowers/specs/batch41-s8-m45-graph-runtime-boundary-summary.json`; `docs/superpowers/specs/batch41-s8-m46-visual-a11y-acceptance-summary.json`; `docs/superpowers/specs/batch41-s8-m47-neural-flow-before-after-summary.json`; `docs/superpowers/specs/batch41-s8-m47-neural-flow-stage/`; `output/playwright/b41-s8-m42/playwright-diagram-proof.json`; `output/playwright/b41-s8-m43/playwright-shell-proof.json`; `output/playwright/b41-s8-m44/playwright-evidence-decision-proof.json`; `output/playwright/b41-s8-m45/playwright-graph-runtime-proof.json`; `output/playwright/b41-s8-m46/playwright-visual-a11y-proof.json`; `output/playwright/b41-s8-m47/playwright-neural-flow-before-after-proof.json`; `docs/superpowers/specs/batch41-first-run-automation-matrix.json`; focused renderer tests; docs/control-plane checks. |
| `B42-S1..S5` | Planned instruction/tool-use compliance hardening for Product-Agent OS auto-engagement: scope/source contract, plugin exposure audit, official-doc source check, implicit invocation policy, metadata validator, fresh-session exposure smoke, runtime route tests, instruction/tool-use evals, staged `self-learning-loop`, hygiene triage and closure. | Decide whether later execution may touch source tree, installed cache, global Codex config or remain read-only; provide any real failed prompts for regression coverage. | Keep Batch 42 planned-only until execution approval; when approved, produce evidence before claiming fixed auto-engagement. | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; `docs/sources/product-agent-os-track-10-backlog.md`; future focused Batch 42 tests, Codex compatibility validation, route/eval evidence, docs/control-plane checks and fresh-session proof if required. |
| `B44-S8` | Remaining Self-Learning Loop closure/promotion decision after completed `B44-S0` through `B44-S7`. | Review S7 staged manual pilot, redacted feedback, eval taxonomy, Promptfoo/HALO export and repair contract before any promotion decision. | Preserve S7 as staged/manual evidence only; fail closed on scope/privacy/approval ambiguity and never auto-apply candidate changes. | Track 11 plan Batch 44 section; `B44-S0..S7` packets including `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; focused self-learning extensions/state tests; docs checks; `git diff --check`. |
| `B45-S5` | Professional Code Authoring learning-loop and automation-candidate policy for `B45-PCA-M23` implemented as candidate-only; `B45-PCA-M14` records full Batch 45 source closure after M23. | Review future manual pilot candidates before any promotion. | Preserve S0-S5 as source evidence; do not activate hooks, schedules or automation without exact approval and activation proof. | Track 11 Batch 45 matrix; `docs/superpowers/specs/batch45-professional-code-s5-learning-automation-summary.json`; focused self-learning/automation/B45 tests; docs unittest; `python tools\check_docs.py`; strict MkDocs smoke; `git diff --check`. |
| `B45-PILOT-MANUAL-6-CODE-TASKS-A02` | Owner-approved local manual pilot of Professional Code Authoring on six real non-mechanical code tasks: automation threshold, first-run summary vocabulary, self-learning candidate target scope, failed manual-run stability, human-spaced regression aliases and privacy-safe evidence references. | Review false-positive, flake, cost and reviewer-usefulness results before deciding whether to run more pilot tasks, keep advisory-only, or approve a future advisory hook/blocker slice. | Preserve pilot as local code/test evidence only; keep hook/blocker/automation activation forbidden without separate exact approval. | `docs/superpowers/specs/batch45-manual-pilot-6-code-tasks-summary.json`; `.codex/product-agent-os/b45-manual-pilot/coding-standard-checklists.md`; focused automation/B45/self-learning tests run twice; docs/control-plane checks; `git diff --check`. |
| `B45-S6` | Advisory-validation and behavior-proof continuation is closed as no-go promotion evidence. `B45-PCA-M24..M27` are implemented with audit, tuning, local advisory wiring, approved live no-go behavior-eval evidence and final keep-advisory-only promotion decision. | Keep the M25 advisory local, non-blocking and reversible; any future stronger advisory, CI or blocker route needs a fresh approval-gated behavior eval. | Do not add CI/blocker enforcement or claim behavior improvement because the live eval result is no-go. Future provider/model reruns still require exact approval. | Track 11 Batch 45 matrix; `docs/superpowers/specs/batch45-comment-sufficiency-false-positive-audit.json`; `docs/superpowers/specs/batch45-comment-sufficiency-tuning-comparison.json`; `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json`; `docs/superpowers/specs/batch45-agent-behavior-eval-results.json`; `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`; focused validator/hook/eval tests; docs/control-plane checks; `git diff --check`. |
| `B45-S7/M37` | Real-project Professional Code Authoring scenario harness is implemented through `B45-PCA-M35` as architecture/inventory/policy/fixture/baseline/refactor-comparison/scorecard/decision evidence with gaps. `B45-PCA-M37-A01` adds local hook/validator review-remediation hardening plus docs/control-plane sync without occupying M36. | Optional `B45-PCA-M36` can prepare a disposable runtime/browser pilot approval packet only if owner wants that route; no pilot is approved by M35/M37. | Keep all S7 follow-up work inside copied fixtures unless a new approval names the target command/mutation/runtime/browser/provider/git/external surface; keep M37 as local non-blocking advisory hardening and docs/source sync only. | `docs/superpowers/specs/batch45-real-project-baseline-results.json`; `docs/superpowers/specs/batch45-real-project-refactor-comparison.json`; `docs/superpowers/specs/batch45-real-project-scorecard.json`; `docs/superpowers/specs/batch45-real-project-decision-packet.json`; `docs/superpowers/specs/batch45-review-remediation-summary.json`; per-scenario packets; focused hook/validator/B45 tests; docs/control-plane checks; `git diff --check`. |
| `B45-RETEST-Q0-Q2` | Protocol source-owned. | Review before Q3. | Q3 local/static only; stop before approval-gated routes. | `docs/superpowers/specs/batch45-quality-retest-protocol.json`; focused tests/docs/diff. |
| `B45-RETEST-Q3-FIXTURE-STATIC` | 37-file static replay source-owned; 14 warnings, `blocking=false`. | Review before live/model or M36 decision. | Preserve local/static ceiling. | `docs/superpowers/specs/batch45-quality-retest-fixture-static-summary.json`; focused tests/docs/diff. |
| `B45-RETEST-Q4-PROJECT-SLICES-STATIC` | 5-slice static replay source-owned; 46 files, 14 warnings, `blocking=false`. | Review before Q5 live/model or M36 decision. | Preserve static ceiling; no approval-gated actions. | `docs/superpowers/specs/batch45-quality-retest-project-slices-static-summary.json`; focused tests/docs/diff. |
| `B45-POSTQ4-T01-T04` | T01/T02 copied-fixture static fix, T03 delta verify and T04 live-model approval packet. | T05 approval was used; review timeout/no-go before T06. | Do not promote from static-only evidence. | `docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json`; `docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json`; focused tests/docs/diff. |
| `B45-POSTQ4-T05/T05B` | T05 exact-approved rerun stopped on baseline timeout; T05B is a separate revised approval packet. | T06 can record no-go, or owner may issue a new exact T05B approval. | No treatment/reviewer comparison, no M26/M35 reversal, no reused approval. | `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json`; `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json`; focused tests/docs/diff. |
| `T11-G1.1` | Project-local documentation toolchain implementation for `DOC-M34..DOC-M41`: local MkDocs, Node docs tooling, Vale, lychee/gitleaks, Mermaid vendor and audit/SBOM governance are recorded; `DOC-M25` remains final generated-site freshness after G2-G5. | Continue G5 source/docs slices after G4. Defer root `site` rebuild/search/sitemap freshness to final `DOC-M25` unless explicitly approved earlier. | Keep root control-plane files, Track 11 plan, registry and tests aligned; do not claim root `site`, search/sitemap freshness, broad scans, remediation or deferred platform readiness until current checks run. | Project-local docs-toolchain checks plus final `DOC-M25` root site rebuild only after approval; docs/control-plane tests; `tools/check_docs.py`; diff hygiene. |
| `T11-G2` | First-run cockpit and artifact docs implemented for `DOC-M04`, `DOC-M05`, `DOC-M06`, `DOC-M19`, `DOC-M20`, `DOC-M33` with RU/EN docs and source/nav/test routing. | Review G2 page usefulness, then continue to G4-G5 docs routes after G3. | Preserve generated-view/source-truth claim ceilings and `DOC_M25_PENDING_SITE_PAGES` until final root site freshness. | `documentation-refresh-g2-first-run-cockpit-artifact-docs-summary.json`; docs tests; `check_docs.py`; strict MkDocs smoke to `.docs-tools/reports`; diff hygiene. |
| `T11-G3` | Diagram atlas and architecture maps implemented for `DOC-M07`, `DOC-M08`, `DOC-M09`, `DOC-M10`, `DOC-M23` with RU/EN docs and source/nav/test routing. | Review diagram naming and usefulness, then continue to G5 docs routes after G4. | Preserve source/generated, browser-proof, Structurizr DSL and `DOC_M25_PENDING_SITE_PAGES` boundaries until final root site freshness. | `documentation-refresh-g3-diagram-atlas-architecture-maps-summary.json`; docs tests; `check_docs.py`; strict MkDocs smoke to `.docs-tools/reports`; diff hygiene. |
| `T11-G4` | Operator flows and system behavior docs implemented for `DOC-M11`, `DOC-M12`, `DOC-M26`, `DOC-M27`, `DOC-M31`, `DOC-M32` with RU/EN docs and source/nav/test routing. | Review operator route usefulness, then continue to G5 generated-artifact UX, graph ontology, browser-boundary and final site-freshness routes. | Preserve instruction/tool-use claim ceilings, staged question ledger, command approval boundaries, source/cache/session state boundaries and `DOC_M25_PENDING_SITE_PAGES` until final root site freshness. | `documentation-refresh-g4-operator-flows-system-behavior-summary.json`; docs tests; `check_docs.py`; strict MkDocs smoke to `.docs-tools/reports`; diff hygiene. |
| `T11-G5` | Evidence quality and final site gate docs implemented for `DOC-M21`, `DOC-M24`, `DOC-M28`, `DOC-M29`, `DOC-M30`; `DOC-M25` remains approval-required/not run. | Ask owner whether to run final `DOC-M25` root `site`/search/sitemap freshness as a separate approved slice, or keep source-docs closure only. | Preserve generated artifact UX, graph orientation, privacy/supply-chain/report-retention, local HTML interaction and residual-routing claim ceilings; do not run root `site`, browser proof, broad scans, remediation or report retention without approval. | `documentation-refresh-g5-evidence-quality-site-gate-summary.json`; docs tests; `check_docs.py`; strict MkDocs smoke to `.docs-tools/reports`; diff hygiene. |
| `T11-DOC-M25` | Generated root site freshness implemented after owner approval. | Use `documentation_refresh_DOC-M25-A01` as the current generated-site evidence; do not rerun browser, broad scans, remediation, publication, release or git steps without separate approval. | Root `site`, search and sitemap are current for G2-G5 pages; browser/runtime/publication/release claims remain unsupported. | `documentation-refresh-doc-m25-site-freshness-summary.json`; root MkDocs build; docs tests; `check_docs.py`; diff hygiene. |

## Batch 39 Execution Rules

- `prod_test.md` is the required attempt/failure/fix/retest ledger for Batch 39.
- Each task must record:
  - test id and slice;
  - objective and product value;
  - technical action;
  - owner action vs Codex action;
  - prerequisites and approvals;
  - evidence path or command;
  - result, failure, fix and retest status;
  - residual risk or accepted gap.
- Choosing a project is not automatically required for every preparatory task. It becomes required when a test step needs real target discovery, target-specific evidence, runtime behavior or mutation.
- When a real project is chosen, the default mode is `read_only_target_discovery`: inspect structure, source-policy state, route signals and evidence shape only. Any live server, browser, provider/API, database, git, release, external write or target mutation action must be approved as a separate surface.

## Source Planning Artifacts

| Artifact | Role |
| --- | --- |
| `REQUIREMENTS.md` | Current scope, acceptance and constraints. |
| `TEST.md` | Current verification commands and escalation rules. |
| `EVALS.md` | Current eval rubrics, thresholds and subjective gates. |
| `RUNLOG.md` | Current-cycle handoff and residual risks. |
| `AGENTS.md` | Durable operating rules and current operating status. |
| `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` | Track 9 implementation plan. |
| `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md` | Track 10 staged plan and status-dashboard history. |
| `docs/sources/product-agent-os-track-8-detailed-backlog.md` | Track 8 detailed scenario/methodology history. |
| `docs/sources/product-agent-os-track-9-backlog.md` | Source-owned Track 9 methodology and verification history. |
| `docs/sources/product-agent-os-track-10-backlog.md` | Source-owned Track 10, Batch 35, Batch 38, Batch 39 and Batch 40 history. |
| `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json` | Source-owned planned Batch 42 instruction/tool-use compliance matrix. |
| `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md` | Active Track 11 documentation architecture, G1.1 docs-toolchain task matrix, Batch 44 Self-Learning Loop plan and Batch 45 Professional Code Authoring matrix. |
| `docs/sources/registry.md` and `docs/sources/registry.en.md` | Claim/source registry. |
| `docs/sources/product-agent-os-batch35-approval-packet-draft.md` | Batch 35 approval and execution packet. |
| `prod_test.md` | Batch 39 production test ledger. |
| `.codex/workflows/control-plane-sync.md` | Mandatory before-completion control-plane sync checklist for non-mechanical Product-Agent OS tasks. |

Evidence ownership stays source-routed; `git diff --check` remains part of docs/control-plane verification.

## Compatibility Marker Bank

These lines are compact anchors for existing tests and source-owned history. They are not execution evidence by themselves.

- B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18`, task-matrix contract, `task-matrix-plan.md`.
- B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17`, `renderer_file_count: 195`, plugin cache remains stale until an explicit publication/cache refresh action is approved.
- B37-S3 `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`, `validate_task_matrix.py`, `task_matrix_validator_contract_present`.
- B37-S4 `T10-PLAN-M07..M09`, `T10-PLAN-M20`, `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present`, `task_matrix_planning_control_governance_present`.
- B37-S5 `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`, `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- `B38-DOC-M01..M10` implemented.
- `B38-DOC-M04` | P1 | Add end-user first-run walkthrough.
- `B38-DOC-M05` | P1 | Add artifact/output gallery for user-facing value.
- `B38-DOC-M06` | P1 | Define public vs internal documentation IA boundary for `site/`.
- `B38-DOC-M07` | P1 | Compact README sync after source docs are corrected.
- `B38-DOC-M08` | P2 | Keep RU/EN parity for every changed user-facing page.
- `B38-DOC-M09` | P2 | Update source registry and control-plane pointers only where source-backed claims change.
- `B38-DOC-M10` | P2 | Final docs verification and generated `site/` refresh decision.
- B38-S1 `B38-PROD-M01..M03`; M01 `owner_closed_no_op_git_release_pr`; M02 `implemented`; M03 `accepted_gap`.
- B38-S2 `B38-PROD-M04..M05`; M04 `implemented`; M05 `implemented`; blocked_sandbox_cache_write_denied_after_backup_stage; plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage; Next release/install/cache action: no remaining M05 cache refresh action is required.
- B38-S3 `B38-PROD-M06..M09`; M06 `implemented`; M07 `implemented`; M08 `implemented`; M09 `implemented`; no_real_project_execution_performed.
- B38-S4 `B38-PROD-M10..M11`; M10 `reviewed_gap_recorded`; M11 `implemented`; source_policy_status ok; system_file_hygiene_status blocked; fixture_dependency_boundary synthetic_non_install_fixtures_unpinned_dependencies.
- B38-PILOT-NF01 `Neural_Flow`, source_policy_status blocked.
- T10-LIVE-M41 post-B38 audit, historical_preflight_snapshot, future git write, fresh preflight is required before any git write, B37/B38/B38-S1 did not themselves close M41.

| Task | Priority | Summary | Status |
| --- | --- | --- | --- |
| `B38-DOC-M04` | P1 | Add end-user first-run walkthrough. | `implemented` |
| `B38-DOC-M05` | P1 | Add artifact/output gallery for user-facing value. | `implemented` |
| `B38-DOC-M06` | P1 | Define public vs internal documentation IA boundary for `site/`. | `implemented` |
| `B38-DOC-M07` | P1 | Compact README sync after source docs are corrected. | `implemented` |
| `B38-DOC-M08` | P2 | Keep RU/EN parity for every changed user-facing page. | `implemented` |
| `B38-DOC-M09` | P2 | Update source registry and control-plane pointers only where source-backed claims change. | `implemented` |
| `B38-DOC-M10` | P2 | Final docs verification and generated `site/` refresh decision. | `implemented` |
| `B38-PROD-M01` | P0 | Resolve or explicitly defer `T10-LIVE-M41` git release/PR gate. | `owner_closed_no_op` |
| `B38-PROD-M02` | P0 | Freeze install source and package surface. | `implemented` |
| `B38-PROD-M03` | P0 | Finalize public and organization-facing plugin metadata. | `accepted_gap` |
| `B38-PROD-M04` | P0 | Run full pre-install verification. | `implemented` |
| `B38-PROD-M05` | P0 | Refresh or install the new plugin version and prove no stale plugin cache is used. | `implemented` |
| `B38-PROD-M06` | P1 | Create first-run operator packet for real users. | `implemented` |
| `B38-PROD-M07` | P1 | Build real-project pilot target and consent matrix. | `implemented` |
| `B38-PROD-M08` | P1 | Define pilot success criteria and product metrics. | `implemented` |
| `B38-PROD-M09` | P1 | Prepare pilot harness and evidence ledger. | `implemented` |
| `B38-PROD-M10` | P1 | Reconfirm security, privacy and supply-chain readiness. | `reviewed_gap_recorded` |
| `B38-PROD-M11` | P2 | Define rollback, removal and cache-recovery procedure. | `implemented` |

## Historical Planning Markers

These markers are preserved here only as compact routing anchors for tests and future discovery:

- B37: `T10-PLAN-M01..M03`, `T10-PLAN-M04..M05`, `T10-PLAN-M06`, `T10-PLAN-M07..M09`, `task_matrix_system_file_hygiene_owner_present`.
- Batch 35: `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr`.
- Batch 38: `B38-S1`, `B38-S2`, `B38-S3`, `B38-S4`, `B38-PILOT-NF01`, `blocked_pending_explicit_cache_mutation_approval`.
- Batch 39: `B39-S1`, `B39-S2`, `B39-S3`, `B39-S4`, `B39-S5`, `B39-TEST-M01..M54`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`.
- Batch 41: `B41-S1`, `B41-S2`, `B41-S3`, `B41-S4`, `B41-S5`, `B41-S6`, `B41-S7`, `B41-S8`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `B41-S8-M41..M47`, `first_run_guided_question_protocol_v1`, `first_run_answer_ledger_v1`, `first_run_ambiguous_route_intake_v1`, `batch41_s6_closure_packet_v1`, `first_run_cockpit_artifact_v1`, `html_redesign_after_owner_review`, `closed_conditional_go_not_release_ready`.
- Batch 42: `B42-S1-M01..M03`, `B42-S2-M04..M06`, `B42-S3-M07..M08`, `B42-S4-M09..M10`, `B42-S5-M11`, `batch42_instruction_tool_use_compliance_matrix_v1`, `planned_task_matrix_added`.
- Track 11 G1.1: `DOC-M34..DOC-M41`, `.venv-docs/`, `.docs-tools/node/`, `.docs-tools/bin/`, `.docs-tools/vale/`, `.docs-tools/link-secret/`, `.docs-tools/reports/`, `docs/assets/javascripts/vendor/`, `documentation_refresh_G1_1-SYSTEM-FILES-A01`, `documentation_refresh_G1_1-DOC-M34-A01`, `documentation_refresh_G1_1-DOC-M35-PREFLIGHT-A01`, `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`, `documentation_refresh_G1_1-DOC-M36-NODE-A01`, `documentation_refresh_G1_1-DOC-M37-VALE-A01`, `documentation_refresh_G1_1-DOC-M38-LINK-SECRET-A01`, `documentation_refresh_G1_1-DOC-M39-MERMAID-A01`, `documentation_refresh_G1_1-DOC-M40-AUDIT-SBOM-A01`, `documentation_refresh_G1_1-DOC-M41-DEFERRED-PLATFORMS-A01`, `implemented_contract_only_no_install`, `installed_smoke_passed`, `installed_advisory_smoke_passed`, `installed_scoped_smoke_passed`, `installed_offline_vendor_smoke_passed`, `implemented_audit_sbom_governance_current_findings_recorded`, `implemented_deferred_platform_trigger_governance_no_install_no_site_rebuild`.
- Batch 40: `B40-S2`, `B40-S3`, `B40-S4`, `B40-S5`, `manual_only`, `not_promoted`.

## Rollback

- Revert only files touched by the current slice.
- Preserve unrelated dirty changes.
- Do not use destructive git operations without explicit approval.
- For target-workspace pilots, rollback must be defined before mutation and must name owner, files, commands and stop condition.

## Verification

For docs/control-plane changes, run:

- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `git diff --check`

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

<!-- product-agent-os:end plan -->
```

### Archived RUNLOG.md

```text
# RUNLOG.md

<!-- product-agent-os:start runlog -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Purpose

`RUNLOG.md` is now the compact handoff layer. It records current-cycle decisions, latest evidence summaries, residual risks and routing pointers. Detailed historical ledgers and batch marker banks belong in source-owned backlog files, `prod_test.md` and registry entries.

## Latest Handoff Summary

- track10_task26_batch35_closed_through_m41_owner_closed_no_op_git_release_pr_b38_s2_m05_cache_refresh_completed_b38_s3_m09_design_only_no_real_project_execution_b38_s4_m11_safety_rollback_gap_recorded.
- Task 26 Batch 35 `T10-LIVE-M41` closed as `owner_closed_no_op_git_release_pr`; `blocked_pending_explicit_cache_mutation_approval` is preserved as historical evidence; `done_through_m40`.
- Root control-plane hygiene was audited in response to system-file review. Recommended remediation: compact `REQUIREMENTS.md`, `PLAN.md`, `TEST.md` and `RUNLOG.md`; remove mojibake from `REQUIREMENTS.md`; remove UTF-8 BOM from `TEST.md`; move historical density to source-owned artifacts.
- `rg` is installed and available as `ripgrep 14.1.0`; future searches should prefer `rg`/`rg --files` before PowerShell fallbacks.
- Agent lifecycle/control-plane audit found the root cause of missing visible `Task Brief` / `Completion Brief`: lifecycle rules existed as prose in agents/workflows/evals, but not as a single config-routed contract loaded through `.codex/config.toml`; hooks/automation were not active and remain inactive.
- Current remediation: `.codex/config.toml` and packaged Product-Agent OS config templates now declare `[product_agent_os.lifecycle_contract]` plus `[workflows]` for `task_plan_lifecycle`, `control_plane_sync` and `agent_context_contract`; agent profiles reference that route instead of duplicating lifecycle rules. Current verification passed: focused lifecycle/template 7/7, infrastructure templates 94/94, docs 78/78, Batch 39 command/manifest 10/10, docs structure OK and diff hygiene OK.
- Lifecycle hook hardening after owner RCA is implemented for packaged Product-Agent OS templates: hooks now include a `PreToolUse` lifecycle marker guard for mutating commands, workflow/eval/docs/tests reference `.codex/product-agent-os/lifecycle-state.json`, and focused checks passed (`test_lifecycle_hooks`, `test_task_plan_lifecycle`, `test_infrastructure_templates`, `test_infrastructure_renderer`, `test_render_infrastructure_cli`, `test_product_agent_os_docs`, `check_docs.py`, `validate_hooks.py`, `git diff --check`). Local `.codex/hooks` installation and `.codex/config.toml` update are blocked by current ACL (`UnauthorizedAccessException` creating `.codex/hooks`; apply_patch denied `.codex/config.toml`). This is a local permission blocker, not hook-template readiness evidence.
- Owner clarified future Product-Agent OS tests should use real-project targets, not only internal `codex_docs` fixtures. `codex_docs` remains the control-plane/evidence workspace; real targets default to read-only discovery unless an attempt row records exact approval for mutation/runtime/browser/provider/git/external action. `B39-FRIA-M20.1..M20.10` have current first-run packet schema, CLI boundary, adapter, renderer, manifest-diff, guardrail, status/rollup, scorecard, docs/registry and accepted-risk verification packet contracts. `B39-TEST-M21-A01..A03` records synthetic plugin/skill, `Neural Flow` expected-block and `SOL` read-only first-run usefulness evidence. `B39-TEST-M22-A01..A03` records route accuracy plus read-only `Neural Flow` / `SOL 0.6` retests for first-run generated artifacts as orientation-only inputs. `B39-TEST-M23..M33` closes `B39-S3` functional regression/repeatability. `B39-S4` is executed through local/read-only/contract hardening gates as `executed_remaining_s4_gates_with_expected_approval_blocks_not_release_ready`: graph-depth, SOL/Neural_Flow static dependency readiness, all-script CLI help, remaining production gates and explicit approval blockers are recorded, while release readiness, runtime/browser pass and promotion remain unsupported.
- `B39-S4-GRAPH-DEPTH-03-A01` records the read-only SOL real-target graph-depth retest after local graph-depth slices. Evidence: `docs/superpowers/specs/batch39-s4-graph-depth-03-real-target-retest-summary.json`; SOL graph validation passed at 2,830 nodes / 2,914 edges / 5,751 observations versus prior 2,539 / 2,551 / 5,090 baseline; normalized real-target evidence now preserves coverage, freshness, rejected-link and framework-semantic summaries; checked target generated-artifact paths were unchanged. This is bounded orientation evidence only, not source-read completion, semantic correctness, target apply safety, runtime/browser/provider proof, readiness, promotion or automation readiness.
- `B39-S4-M37-M39-A01` records the next broader B39-S4 hardening slice with subagents and skills. Evidence: `docs/superpowers/specs/batch39-s4-m37-m39-hardening-summary.json`; docs-maintainer inventory found M37 RED for public site acceptance because rendered `site/` evidence is stale, and tester inventory found M38/M39 only partially covered by adjacent M20/M28/M40 checks. Local TDD added `batch39_s4_hardening.py` and `test_batch39_s4_hardening.py`: M37 now has internal-scope first-run generated page classification, M38 has a first-run HTML no-external URL/script audit, and M39 has a first-run CLI mode/unsafe-packet matrix. This is partial hardening evidence only; full public docs/site rebuild acceptance, full offline/dependency readiness, all-script CLI matrix, runtime/browser/provider proof, readiness, promotion and automation readiness remain unsupported.
- `B39-S4-FULL-HARDENING-A01` records the requested read-only SOL 0.6 / Neural_Flow offline/dependency, all-script CLI and runtime/browser harness pass. Evidence: `docs/superpowers/specs/batch39-s4-all-script-cli-matrix.json`, `docs/superpowers/specs/batch39-s4-full-hardening-sol_0_6-summary.json`, `docs/superpowers/specs/batch39-s4-full-hardening-neural_flow-summary.json`, `docs/superpowers/specs/batch39-s4-full-hardening-comparison.json`. SOL static dependency inventory is partial-pass with frontend/backend package manifests and lockfiles, but runtime/browser is blocked by `.next` / `.sol_data` write risk, provider-sensitive backend dependencies and unavailable Playwright; graph counts remain 2,830 nodes / 2,914 edges / 5,751 observations versus the latest graph-depth baseline. Neural_Flow is docs/research-only with no runtime manifests; current graph dry-run is 557 nodes / 556 edges / 1,113 observations. All-script `--help` matrix now covers 32 scripts with 32 passed and zero gaps after the remaining CLI wrapper fixes. Selected target digests were unchanged. No install, target mutation, live server, browser automation, provider/API, git, release, deploy, publish or automation action was performed.
- `B39-S4-REMAINING-GATES-A01` records execution of the remaining S4 gates. Evidence: `docs/superpowers/specs/batch39-s4-remaining-gates-summary.json` and `docs/superpowers/specs/batch39-s4-closure-readiness-matrix.json`; all-script CLI help is now 32/32 with zero gaps. M37 remains blocked because MkDocs is unavailable; M42 remains blocked until an approved disposable runtime/browser pilot exists; M46 and M54 remain approval-required for live/external surfaces and release governance. S4 is not release-ready, but the remaining hardening gates are now represented as current evidence or explicit blockers.
- `B39-FIX-M40-PARTIAL-LANGUAGE-SUMMARY-001` records the full-discovery regression fix found after S4 remaining gates. Evidence: `project_graph_analysis.py` now separates `partial_language_summary` from `unsupported_language_summary`, so TypeScript/JavaScript conservative stdlib support is visible without being mislabeled unsupported; focused graph-analysis tests passed and full unittest discovery passed 983 tests with 1 skipped.
- `B39-S5-CLOSURE-A01` records Batch 39 closure/go-no-go with agents and skills. Evidence: `docs/superpowers/specs/batch39-s5-closure-summary.json`, `docs/superpowers/specs/batch39-s5-go-no-go-decision-packet.json`, `docs/superpowers/specs/batch39-s5-no-unapproved-actions-proof.json` and `docs/superpowers/specs/batch39-s5-owner-feedback-test-plan.json`. Decision: release/distribution `no_go`, owner-feedback testing `conditional_go`, runtime/browser pilot `approval_required`; all no-unapproved-actions surfaces remain false.
- `B41-S1-COMMAND-CONTRACT-A01` records Batch 41 first-run command/UX contract implementation with agents and skills. Evidence: `docs/superpowers/specs/batch41-s1-command-contract-summary.json`; `B41-S1-M01..M05` are implemented for `first_run_orchestrator_contract_v1`, no-args help, `--full-dry-run`, external `--stage <dir>`, approved `--write-analysis`, stage-inside-target blocking and renderer stage output support. Agent `Archivist` provided read-only fresh-context handoff. No live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation or external write was performed.
- `B41-S2-SCRIPT-MATRIX-A01` records Batch 41 first-run script-matrix implementation with agents and skills. Evidence: `docs/superpowers/specs/batch41-s2-script-matrix-summary.json`; `B41-S2-M06..M09` are implemented for `first_run_script_registry_v1`, `first_run_command_matrix_v1`, `first_run_evidence_summary_v1` and `first_run_resume_ledger_v1`. The current local help-only matrix covers 34 top-level scripts: 26 passed safe help commands, 7 skipped approval-required rows and 1 skipped live-bound row; completion remains `not_claimed`. Agent `Scout` provided read-only inventory and stop-condition handoff. No live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation or external write was performed.
- `B41-S3-PROJECT-ANALYSIS-A01` records Batch 41 first-run project-analysis summary implementation with agents and skills. Evidence: `docs/superpowers/specs/batch41-s3-project-analysis-summary.json`; `B41-S3-M10..M16` are implemented for discovery route, methodology audit, source-policy boundary, project graph dry-run, docs/logging detection, static dependency readiness and runtime/browser boundary. Synthetic fixture evidence keeps source-policy `blocked` as `approval_required`, graph as orientation evidence, dependency readiness as static inventory only and runtime/browser as `approval_required`; completion remains `not_claimed`. Agents `Cartographer` and `Index` provided read-only implementation and control-plane handoffs. No live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation or external write was performed.
- `B41-S4-HTML-ARTIFACT-A01` records Batch 41 first-run HTML artifact integration with agents and skills. Evidence: `docs/superpowers/specs/batch41-s4-html-artifact-summary.json`; `B41-S4-M17..M20` are implemented for orchestrator renderer output, complete 11-page offline HTML artifact, previous-baseline comparison in CLI/HTML/manifest and cleanup/rollback guidance as preview-only. Generated HTML remains orientation evidence only; cleanup/delete is not performed by default. Agents `Scout the 2nd` and `Scribe the 2nd` provided read-only code/docs handoffs. No live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation or external write was performed.
- `B41-S5-GUIDED-QUESTIONS-A01` records Batch 41 guided question UX and answer-ledger routing with agents and skills. Evidence: `docs/superpowers/specs/batch41-s5-guided-questions-summary.json`; `B41-S5-M21..M23` are implemented for top-level `first_response`, packet `question_queue`, one blocking question maximum, staged `answer-ledger-template.json`, `answer_ledger_routing` and two or three route options for ambiguous intake. Unreviewed answers are not source truth and do not mutate source docs. Agents `Cartographer the 2nd` and `Index the 2nd` provided read-only code/docs handoffs. No live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation or external write was performed.
- `B41-S6-CLOSURE-A01` records Batch 41 first-run QA pilots and closure. Evidence is source-owned by `docs/superpowers/specs/batch41-s6-closure-summary.json` plus S6 synthetic, real-target, scorecard, verification, plugin-cache, no-unapproved-actions and go/no-go packets. Result: synthetic E2E and Neural_Flow expected-block passed; app-like pilot is `blocked_timeout`; owner feedback and installed plugin-cache readiness remain pending/approval-required; closure is `closed_conditional_go_not_release_ready`. No live/browser/provider/git/release/automation/plugin-cache/external write was performed.
- `B41-S7-HTML-COCKPIT-ANALYSIS-A01` records owner-feedback correction for the Neural_Flow first-run HTML artifact. Evidence: `docs/superpowers/specs/batch41-s7-html-cockpit-analysis.txt` and `docs/superpowers/specs/batch41-first-run-automation-matrix.json`; `B41-S7-M31..M40` plan cockpit artifact, graph, visual QA, offline/privacy/accessibility hardening and Neural_Flow acceptance. Root cause: diagnostic HTML was structurally valid but not wired to the cockpit visual direction. No target/live/browser/provider/git/release/automation/plugin-cache/external write was performed.
- `B41-S7-GRAPH-LIBRARY-SELECTION-A01` records owner selection of `Cosmos.gl` as the graph visualization library for the cockpit artifact. Planning impact: Graphology-compatible payloads remain the internal graph/query interchange format, Sigma.js becomes fallback/compatibility-only, vendored Cosmos.gl requires version/license/hash and offline validation evidence, and 1k/5k/10k+/50k-edge scale checks must cover LOD, link sampling, label suppression and fallback behavior. No dependency install, vendoring, browser automation, network fetch, target mutation or external write was performed.
- `B41-S7-M31-M33-A01` implements the first cockpit foundation with agents and skills. Evidence: `docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json`; `B41-S7-M31..M33` are implemented for `first_run_cockpit_artifact_v1`, primary single-file `index.html`, manifest `cockpit_contract`, manifest `primary_cockpit.view_model`, static cockpit shell, eight-section cockpit model and bounded first-run packet/source-artifact adapter. Focused B41 first-run tests passed 18/18 and first-run analysis tests passed 14/14. Agents `Ariadne` and `Archivist` provided read-only acceptance and technical handoffs. No target mutation, live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation, plugin-cache write or external write was performed.
- `B41-S7-M34-M35-A01` implements first-run cockpit graph rendering with agents and skills. Evidence: `docs/superpowers/specs/batch41-s7-m34-m35-graph-rendering-summary.json`; `B41-S7-M34..M35` are implemented for Graphology-compatible file/source graph, Cosmos.gl static adapter payload, selected-file panel, legend/status coloring, table fallback, omitted counts, explicit code-graph `not_available` state and graph-summary code hotspots when packet data exists. Focused M31..M35 tests passed, and the full B41 first-run automation suite passed 19/19. Agents `Cartographer` and `Vector` provided read-only graph-adapter and architecture handoffs. Cosmos.gl runtime/WebGL execution, browser visual QA and Neural_Flow acceptance remain unsupported. No target mutation, live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation, plugin-cache write or external write was performed.
- `B41-S7-M36-M39-A01` implements first-run cockpit UX and safety hardening with agents and skills. Evidence: `docs/superpowers/specs/batch41-s7-m36-m39-cockpit-ux-safety-summary.json`; `B41-S7-M36..M39` are implemented for static offline search/filter controls, stable anchors, detail-panel links, progressive diagnostics, static visual QA, white-page regression guards and offline/privacy/accessibility contracts. Focused M31..M39 tests passed, and the full B41 first-run automation suite passed 20/20. Agents `Cartographer`, `Gauge` and `Index` provided read-only renderer, test-design and docs/control-plane handoffs. Browser visual proof, runtime interaction, WCAG verification, Cosmos.gl runtime/WebGL execution and Neural_Flow acceptance remain unsupported. No target mutation, live server, browser automation, provider/API, MCP external call, git action, release/deploy/publish, active automation, plugin-cache write or external write was performed.
- `B41-S7-M40-OWNER-APPROVAL-A01` records owner approval for M40 to include Neural_Flow acceptance, browser visual proof, runtime interaction checks, WCAG-oriented static/browser checks, Cosmos.gl runtime/WebGL checks where local assets/tooling are available, and necessary `codex_docs` cockpit fixes. Evidence: `docs/superpowers/specs/batch41-s7-m40-owner-approval-packet.json`. This was approval evidence only at the time it was recorded; execution evidence is now recorded by `B41-S7-M40-A01`. Git stage/commit/push/PR, release/deploy/publish, provider/API calls, external writes and target source mutation remain out of scope without separate approval.
- `B41-S7-M40-A01` executes the owner-approved Neural_Flow acceptance pilot with agents, Context7 and Playwright evidence. Evidence: `docs/superpowers/specs/batch41-s7-m40-neural-flow-acceptance-summary.json`, `docs/superpowers/specs/batch41-s7-m40-neural-flow-stage/`, `output/playwright/b41-s7-m40/playwright-runtime-proof.json` and screenshots under `output/playwright/b41-s7-m40/`. Result: generated staged Neural_Flow cockpit artifact, browser visual proof passed, static runtime interaction passed, console/network clean, WCAG-oriented browser checks passed without certification claim, and a renderer/test fix made the visible policy label canonical as `generated-view-only`. Cosmos.gl runtime/WebGL execution is blocked by missing vendored runtime asset and the intentional script-free SVG/table fallback. No target mutation, live server, provider/API, MCP external call, git action, release/deploy/publish, active automation, plugin-cache write or external write was performed.
- `B41-POST-NF-RERUN-A01` records the post-Batch41 Neural_Flow rerun and old/new HTML artifact comparison. Evidence: `docs/superpowers/specs/batch41-post-neural-flow-rerun-task-plan.txt`, `docs/superpowers/specs/batch41-post-neural-flow-rerun-summary.json`, `docs/superpowers/specs/batch41-post-neural-flow-rerun-comparison.json`, `docs/superpowers/specs/batch41-post-neural-flow-rerun-stage/` and `output/playwright/b41-post-neural-flow-rerun/playwright-proof.json`. Result: fresh read-only plugin rerun wrote staged artifacts only, `target_workspace_mutation=false`, the new artifact is identical to the M47 redesign output, and compared with M40 it adds architecture-dossier/diagram/evidence/runtime-boundary surfaces. Full WCAG certification, Cosmos.gl/WebGL runtime execution, release readiness, target apply safety and owner final visual acceptance remain unsupported.
- `B41-S9-HTML-MODERNIZATION-A01` records implementation of `B41-S9-M48..M57` with agents and skills. Evidence: `docs/superpowers/specs/batch41-s9-html-modernization-summary.json`, `docs/superpowers/specs/batch41-s9-m57-neural-flow-summary.json`, `docs/superpowers/specs/batch41-s9-m57-neural-flow-comparison.json`, `docs/superpowers/specs/batch41-s9-m57-neural-flow-stage/`, updated Track 10 B41-S9 matrix rows and focused B41 tests. Result: the first-run cockpit renderer now has architecture intelligence design contract, operator first viewport, approved inline local JS, static diagram workbench, DB/schema/API/config contract surface, graph/file/code surface, guided read route, evidence/risk hierarchy and static visual/accessibility gate. Neural_Flow was rerun read-only into a staged artifact, comparison checks passed, and target fingerprint evidence reported `target_workspace_mutation=false` with 19 files before and after. No browser automation, live runtime, Cosmos.gl/WebGL execution, provider/API call, external request, installed plugin cache refresh, git action, release/deploy/publish or target apply was performed in S9.
- `B42-PLANNING-A01` records the owner-requested Track 10 instruction/tool-use compliance hardening matrix. Evidence: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`, Track 10 plan Batch 42 addendum and Track 10 backlog planned addendum. Scope: Product-Agent OS auto-engagement, source/cache/session skill exposure, official-doc source check, implicit invocation policy, metadata validator, fresh-session smoke, runtime route/eval hardening, staged `self-learning-loop`, system-file hygiene triage and closure. Status: `planned_task_matrix_added`, not implementation evidence. No target mutation, global config write, installed-plugin-cache write, live server, browser automation, provider/API call, MCP external call, git action, release/deploy/publish, active automation or external write was performed.
- `documentation_refresh_G0-A01` records execution of the governance group for the documentation refresh with agents and skills. Evidence: `docs/superpowers/specs/documentation-refresh-g0-governance-summary.json` and `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`; `DOC-M00`, `DOC-M01`, `DOC-M03`, `DOC-M15` and `DOC-M22` are closed for G0 scope only. Result: reader-facing terminology policy, documentation requirements/non-goals, capability source map, claim ceiling matrix, no-unapproved-actions proof and closure boundary are source-owned. G1-G5 remain planned. No source registry update, MkDocs nav change, generated `site/` rebuild, browser automation, live runtime, provider/API call, installed cache refresh, global config write, git action, release/deploy/publish, target mutation or automation activation was performed.
- `documentation_refresh_G1-A01` records execution of the source records, registry and generated-site parity group with agents and skills. Evidence: `docs/superpowers/specs/documentation-refresh-g1-source-site-parity-summary.json`, `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`, `docs/sources/registry.md` and `docs/sources/registry.en.md`; `DOC-M02`, `DOC-M13`, `DOC-M14`, `DOC-M16` and `DOC-M17` are closed for G1 source-record scope, while `DOC-M25` is `blocked_mkdocs_unavailable` because plain active Python reports `No module named mkdocs`. Follow-up inventory found historical dependency targets at `C:\tmp\codex_docs_mkdocs` and `tmp\mkdocs_deps_b40s4`, but they are not currently usable as a runnable MkDocs module from this process; `TEST.md` records the future docs-runtime route. Result: pre-G1 generated `site/` stale state was recorded, registry/source markers were added, one reader-facing internal/private pilot label leak was neutralized, no new public product page was introduced in G1, and generated site/search/sitemap freshness is not claimed. G2-G5 remain planned. No browser automation, live runtime, provider/API call, installed cache refresh, global config write, target mutation, git action, release/deploy/publish or automation activation was performed.
- `documentation_refresh_G1_1-PLANNING-A01` adds planned project-local documentation toolchain tasks. Evidence: `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md` plus compact registry markers. `DOC-M34..DOC-M41` plan `.venv-docs/` for MkDocs Material, `.docs-tools/node/` for `markdownlint-cli2`, Prettier and Redocly CLI, `.docs-tools/bin/` for Vale, lychee and gitleaks, `.docs-tools/reports/`, optional `docs/assets/javascripts/vendor/`, and deferred Docusaurus, Storybook and Structurizr DSL trigger criteria. This is planned-only: no dependency install, network download, binary vendoring, hook/automation activation, site rebuild, browser/runtime/provider call, target mutation, git action, release/deploy/publish or global config write was performed.
- `documentation_refresh_G1_1-SYSTEM-FILES-A01` syncs root system files for G1.1 implementation. Evidence: `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `AGENTS.md`, `RUNLOG.md`, Track 11 plan and docs contract tests. Result: G1.1 is now routed as an active project-local docs-toolchain implementation path with requirements, sequencing, verification commands, eval claim ceilings, durable no-global-tooling rule and current handoff. No dependency install, network download, binary vendoring, hook/automation activation, strict site rebuild, browser/runtime/provider call, target mutation, git action, release/deploy/publish or global config write was performed.
- `documentation_refresh_G1_1-DOC-M34-A01` implements the first G1.1 row as a contract-only folder/config boundary. Evidence: `.gitignore`, `.docs-tools/README.md`, `.docs-tools/node/README.md`, `.docs-tools/bin/README.md`, `.docs-tools/reports/README.md`, `docs/superpowers/specs/documentation-refresh-g1-1-doc-m34-folder-contract-summary.json`, Track 11 plan and focused docs contract tests. Result: `.venv-docs/`, `.docs-tools/node/node_modules/`, local caches, standalone binaries and generated reports are ignored; allowed checked-in config, forbidden content, approval boundaries and unsupported install/site claims are explicit. `DOC-M35..DOC-M41` remain planned or approval-gated. No dependency install, network download, binary vendoring, report retention, hook/automation activation, strict site rebuild, browser/runtime/provider call, target mutation, git action, release/deploy/publish or global config write was performed.
- `documentation_refresh_G1_1-DOC-M35-PREFLIGHT-A01` preserves the 2026-06-20 failed MkDocs runtime install attempt as historical evidence: the owner-approved network install hit `WinError 10013`, leaving only a partial `.venv-docs/` scaffold at that time. This blocker is superseded by the 2026-06-21 retry evidence below.
- `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`: successful project-local MkDocs runtime retry passed; `.docs-tools/reports/mkdocs-strict-smoke-2026-06-21` strict smoke exists; root `site` freshness remains unclaimed.
- `documentation_refresh_G1_1-DOC-M36-NODE-A01`: approved `.docs-tools/node` install and scoped README markdownlint/Prettier smoke passed; install reported 3 moderate vulnerabilities, so audit/SBOM stays with `DOC-M40`.
- `documentation_refresh_G1_1-DOC-M37-VALE-A01`: approved local Vale `3.15.1` install/checksum passed with fixture and negative readiness-wording smoke; broad Vale enforcement and report retention remain unclaimed.
- `documentation_refresh_G1_1-DOC-M38-LINK-SECRET-A01`: approved local lychee `0.24.2` / gitleaks `8.30.0` install/checksum passed with offline link fixture and redacted clean secret fixture; external URL crawl, broad link/secret scans, raw finding publication and report retention remain unclaimed.
- `documentation_refresh_G1_1-DOC-M39-MERMAID-A01`: approved Mermaid `10.9.6` vendoring replaced the floating CDN asset in `mkdocs.yml` with `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js`; strict MkDocs/static external-runtime smoke passed, while browser rendering, root `site` freshness and dependency safety remain unclaimed.
- `documentation_refresh_G1_1-DOC-M40-AUDIT-SBOM-A01`: dependency audit/SBOM governance is implemented for G1.1 docs tooling. Local evidence captures Python inventory, `pip check`, Node CycloneDX SBOM generation, current approved `npm audit --audit-level=high` output with 3 moderate / 0 high / 0 critical findings, and checksum consistency for Vale, lychee, gitleaks and Mermaid. No dependency remediation, `npm audit fix`, Python vulnerability audit, raw report retention, root `site` rebuild, browser automation, git or publication action was performed.
- `documentation_refresh_G1_1-DOC-M41-DEFERRED-PLATFORMS-A01`: deferred platform trigger governance is implemented for G1.1 docs tooling. Local evidence records Docusaurus, Storybook and Structurizr DSL trigger criteria, owner decision path, proposed local install folders, acceptance criteria and unsupported claims. No Docusaurus, Storybook or Structurizr install, dependency download, scaffold, root `site` rebuild, browser/render proof, git, automation or publication action was performed.
- `documentation_refresh_G1_1-RESIDUAL-ROUTING-A01`: Track 11 now carries the G1.1 residual routing matrix, `G5 / DOC-M30` residual handoff and final `G5 / DOC-M25` generated-site freshness gate. Root `site` rebuild routes to final `DOC-M25` after G2-G5 source updates; Mermaid/browser/Structurizr proof routes to `DOC-M08` and `DOC-M23`; broad lint/format/Vale/link/secret/Redocly enforcement routes to `DOC-M26` and `DOC-M21`; supply-chain, Python vulnerability audit, complete repository SBOM, Node remediation and report-retention follow-ups route to `DOC-M24`. No install, root site rebuild, browser proof, dependency remediation, report retention, external crawl, automation, git, release, deploy or publication action was performed.
- `documentation_refresh_G2_G5-G1_1-RESIDUAL-HOOKS-A01`: G2-G5 task rows now carry G1.1 residual hooks directly; `DOC-M30` checks row-level residual closure before final `DOC-M25`. No root site rebuild, browser proof, dependency remediation, report retention, install, automation, git, release, deploy or publication action was performed.
- `documentation_refresh_G2-A01`: G2 closes `DOC-M04`, `DOC-M05`, `DOC-M06`, `DOC-M19`, `DOC-M20`, `DOC-M33` as source docs/nav/test sync; `DOC_M25_PENDING_SITE_PAGES` defers root `site`. No root site, browser/runtime/provider, target, git, release or automation action.
- `documentation_refresh_G3-A01`: G3 closes `DOC-M07`, `DOC-M08`, `DOC-M09`, `DOC-M10`, `DOC-M23` as source diagram atlas/nav/test sync; `DOC_M25_PENDING_SITE_PAGES` now covers G2/G3 pending pages until final `DOC-M25`. No root site, browser/runtime/provider, target, git, release or automation action.
- `documentation_refresh_G4-A01`: G4 closes `DOC-M11`, `DOC-M12`, `DOC-M26`, `DOC-M27`, `DOC-M31`, `DOC-M32` as instruction/tool-use, operator command, guided question, methodology integration and source/cache/session source docs/nav/test sync; `DOC_M25_PENDING_SITE_PAGES` now covers G2/G3/G4 pending pages until final `DOC-M25`. No root site, cache refresh, global config, browser/runtime/provider, target, git, release or automation action.
- `documentation_refresh_G5-A01`: G5 closes `DOC-M21`, `DOC-M24`, `DOC-M28`, `DOC-M29`, `DOC-M30` as evidence-quality source docs/nav/test sync; `DOC_M25_PENDING_SITE_PAGES` covers G2-G5 until final `DOC-M25`, which remains `approval_required_not_run`. No root site, browser/runtime/provider, target, dependency remediation, raw report retention, git, release or automation action.
- `documentation_refresh_DOC-M25-A01`: Root `site`/search/sitemap freshness now covers the former `DOC_M25_PENDING_SITE_PAGES` set. Out of scope: browser proof, broad scans, remediation, raw retention, provider/target/cache/global-config/git/release/deploy/publish/automation.
- `product_agent_os_LIFECYCLE-HOOKS-A01` records owner-approved project-local lifecycle hook activation after the DOC-M36 Task Brief miss. Evidence: `.codex/hooks.json`, `.codex/hooks/hooks.json`, `.codex/hooks/*.py`, `.codex/product-agent-os/lifecycle-state.json`, `plugins/product-agent-os/assets/templates/hooks/hooks.json`, `plugins/product-agent-os/scripts/product_agent_os/validators.py`, `.codex/config.toml`, `.codex/evals/agent-context-contract.json` and `docs/superpowers/specs/product-agent-os-lifecycle-hooks-local-activation-summary.json`. Result: project-local hooks now use the current Codex `hooks` shape, resolve scripts from git root, and guard mutating Product-Agent OS work through `.codex/product-agent-os/lifecycle-state.json`. Normal directory creation hit the known `.codex/hooks` ACL blocker and was completed only after explicit owner approval for `New-Item -ItemType Directory -Path .codex\hooks -Force`. Codex hook trust review / new-session execution remains a follow-up boundary, not current proof.
- `B44-SLL-M07-M08-M18-M09-M10-A01`: S3 feedback/preferences evidence in `docs/superpowers/specs/batch44-self-learning-loop-feedback-preferences-summary.json`; no real session import, provider/model, target, automation, git/release/deploy/publish or auto-apply.
- `B44-SLL-M11-M12-M19-M20-M21-M22-A01`: S4 metrics/evals evidence in `docs/superpowers/specs/batch44-self-learning-loop-metrics-evals-summary.json`; no live eval/provider/model, target, automation, git/release/deploy/publish or auto-apply.
- `B44-SLL-M13-M14-A01`: S5 candidate/safety evidence in `docs/superpowers/specs/batch44-self-learning-loop-candidate-safety-summary.json`; no hook/schedule/provider/target/git/release/deploy/publish/external write or auto-apply.
- `B44-SLL-M15-M16-A01`: S6 docs/contracts/closure evidence; promotion remains `candidate_only`, `minimum_manual_successful_runs: 3`; no real session import, provider/live eval, target, automation, git/release/deploy/publish/external write or auto-apply.
- `B44-S7-SELF-LEARNING-MANUAL-PILOT-A01`: approved staged manual pilot evidence in `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; initializer, explicit `--state-file`, redacted ledgers, two candidates, 8 eval cases and 6 HALO-style recommendations are review-only. No Promptfoo/HALO/provider/browser/target/git/release/deploy/publish/automation/external write or auto-apply occurred.

## Current Product-Agent OS State

| Workstream | Status | Notes |
| --- | --- | --- |
| Track 9 / Track 10 history | Source-owned historical context. | Use detailed backlogs and registry for historical claims. |
| Task 26 Batch 35 | Closed through `T10-LIVE-M41` as `owner_closed_no_op_git_release_pr`. | No branch, stage, commit, push or PR was performed; future git writes require fresh preflight and exact approval. |
| Batch 38 S1/S2/S3/S4 | Recorded as implemented/reviewed according to source-owned history. | `B38-S2` includes `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` is preserved. |
| `B38-PILOT-NF01` | Docs-only target pilot addendum completed. | Target apply remains blocked by `source_policy_status: blocked` and missing target control-plane/source registry artifacts. |
| Batch 39 | Executed through `B39-S5-CLOSURE-A01` as local/read-only/contract evidence. | Continue with manual owner-feedback testing. Store evidence in `codex_docs`, and do not mutate `SOL 0.6`, `Neural Flow` or any target without exact approval. Runtime/browser/provider/model/vector/eval/live-database/migration/production-data/git/GitHub/release/deploy/publish/automation/external actions still require exact approval. |
| Batch 40 completion-skeptic | Closed as local manual foundation through `B40-S5`. | Promotion state remains `manual_only` and `not_promoted`. |
| Batch 41 first-run orchestration | `B41-S1..S9` recorded as local/read-only/staged CLI/contract/browser/static evidence; `B41-S9-M48..M57` carries `architecture_intelligence_design_contract_v1`, diagram workbench, graph/code surface and Neural_Flow rerun comparison. | S6 remains `closed_conditional_go_not_release_ready`; S7/S8/S9 are generated-artifact acceptance evidence only. No release readiness, target apply safety, automation promotion, installed-plugin readiness or Cosmos.gl/WebGL runtime proof is claimed. |
| Batch 42 instruction/tool-use compliance | Planning matrix added as `B42-PLANNING-A01`. | Planned-only. Execution still needs owner decision on source tree versus installed cache versus global Codex policy versus read-only audit. Do not claim Product-Agent OS auto-engagement is fixed until fresh source/cache/session, route/eval and closure evidence exist. |
| Batch 44 Self-Learning Loop | `B44-S0..S7` local/schema/fixture/docs/staged evidence; S7 adds initializer, staged state runner, eval taxonomy, Promptfoo/HALO packets and repair contract. | Continue with `B44-S8` owner review; no scheduler/hooks/automation, import, provider/HALO run, target, git/release/deploy/publish, external write or auto-apply. |
| Documentation refresh governance | G0 closed for governance scope through `documentation_refresh_G0-A01`. | Source-owned packet exists at `docs/superpowers/specs/documentation-refresh-g0-governance-summary.json`; G1-G5 remain planned, generated `site/` was not rebuilt and public/readiness/release/runtime/browser claims are not made. |
| Documentation refresh source/site parity | G1 source records are closed through `documentation_refresh_G1-A01`; the MkDocs blocker is superseded by `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`, and `DOC-M25` is deferred to final G5 after G2-G5 source updates. | Source packet: `docs/superpowers/specs/documentation-refresh-g1-source-site-parity-summary.json`. Root `site` remains stale because only `.docs-tools/reports/` smoke builds ran; final root `site`/search/sitemap freshness routes through `DOC-M25`; publication/readiness/release/runtime/browser/provider/cache/global-config/git/automation claims are not made. |
| Documentation refresh toolchain planning | G1.1 route is current through system-file sync, `DOC-M34..DOC-M41` and residual routing evidence. | Local MkDocs, Node tooling, advisory Vale, scoped lychee/gitleaks, vendored Mermaid, dependency/SBOM governance and deferred Docusaurus/Storybook/Structurizr triggers are recorded. Residuals route to future G rows and `DOC-M30`; root `site`/search/sitemap freshness is intentionally last through `DOC-M25`. Root `site`, browser Mermaid, broad enforcement/scans, raw reports, Python audit/SBOM, remediation and deferred platform readiness remain unclaimed. |
| Documentation refresh G2 | Source docs implemented through `documentation_refresh_G2-A01`. | Cockpit/artifact/graph/CLI/technical docs are synced; root `site`/search/sitemap freshness remains final `DOC-M25`. |
| Documentation refresh G3 | Source diagram docs implemented through `documentation_refresh_G3-A01`. | Source/generated trust, first-run cockpit architecture, evidence/risk, skill exposure and Architecture Intelligence diagram pages are synced; root `site`/search/sitemap freshness remains final `DOC-M25`. |
| Documentation refresh G4 | Operator-flow source docs implemented through `documentation_refresh_G4-A01`. | Instruction/tool-use compliance, operator command matrix, guided questions/answer ledger, methodology integration and source/cache/session pages are synced; root `site`/search/sitemap freshness remains final `DOC-M25`, and auto-engagement/cache/global config/fresh-session proof remains unsupported. |
| Documentation refresh G5 | Evidence-quality source docs implemented through `documentation_refresh_G5-A01`. | Generated artifact UX, graph intelligence, privacy/supply-chain/report-retention, local HTML interaction and residual follow-up/site-freshness pages are synced; root `site`/search/sitemap freshness remains final `DOC-M25`, and browser proof, broad scans, remediation and raw report retention remain approval-required. |
| Documentation refresh DOC-M25 | Root site fresh via `documentation_refresh_DOC-M25-A01`. | Former pending pages in root `site`/search/sitemap; browser/runtime/publication/release/scans/remediation/raw-retention/git unsupported. |
| Agent lifecycle/control-plane sync | Config-routed lifecycle contract implemented; project-local hooks now require `task_start_brief_v1` full field-list marker, not legacy `shown=true` marker only. | Before non-mechanical work, agents must show full visible Task Brief, record `.codex/product-agent-os/lifecycle-state.json`, run control-plane sync, and show Completion Brief. Codex may require `/hooks` trust review or a fresh session before hooks execute. |

## Control-Plane Marker Bank

Distribution map: `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `AGENTS.md`, `docs/sources/registry.md`, `docs/sources/product-agent-os-track-8-detailed-backlog.md`, `docs/sources/product-agent-os-track-9-backlog.md`, `docs/sources/product-agent-os-track-10-backlog.md`, `docs/sources/product-agent-os-batch35-approval-packet-draft.md`.

- Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix; no git stage/commit/push/PR.
- B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18`, task-matrix contract, `task-matrix-plan.md`.
- B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17`, `renderer_file_count: 195`, plugin cache remains stale until an explicit publication/cache refresh action is approved.
- B37-S3 `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`, `validate_task_matrix.py`, `task_matrix_validator_contract_present`.
- B37-S4 `T10-PLAN-M07..M09`, `T10-PLAN-M20`, `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present`, `task_matrix_planning_control_governance_present`.
- B37-S5 `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`, `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- Batch 38 S1 release gate/package metadata; M01 is owner-closed as `owner_closed_no_op_git_release_pr`; package source digest `7d5a7634d1223f72ccdd1edcd24fddeb8bbdcc38d36d73ab1d002f352b06dcbb`; M03 is owner-confirmed as `local-only/internal R&D` distribution.
- M41 post-B38 audit; historical_preflight_snapshot; fresh git status/unrelated-change preflight; B37/B38/B38-S1 did not themselves close M41.
- B38-S2, blocked_sandbox_cache_write_denied_after_backup_stage, plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage.
- B38-S3, B38-PROD-M06..M09, no_real_project_execution_performed.
- B38-S4, B38-PROD-M10..M11, reviewed_gap_recorded, rollback.
- B38-PILOT-NF01, Neural_Flow, source_policy_status blocked, read_only_pilot_executed_blocked_on_target_source_policy, usage_mode: legacy_onboarding, staged outputs validated, target_workspace_mutation false.
- B40-S4 docs/site/source-transfer run; implemented_docs_site_source_transfer.
- B40-S5 pilot/metrics/closure run; implemented_pilot_metrics_closure_manual_only; manual_only.

## Preserved Historical Markers

These markers are retained as compact discovery anchors, not as full evidence:

- B37 planning/hygiene markers: `T10-PLAN-M01..M03`, `T10-PLAN-M04..M05`, `T10-PLAN-M06`, `T10-PLAN-M07..M09`, `task_matrix_system_file_hygiene_owner_present`.
- Batch 35 live marker: `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr`.
- Batch 38 markers: `B38-S1`, `B38-S2`, `B38-S3`, `B38-S4`, `B38-PILOT-NF01`, `blocked_pending_explicit_cache_mutation_approval`, `blocked_sandbox_cache_write_denied_after_backup_stage`.
- Batch 39 markers: `B39-S1`, `B39-S2`, `B39-S3`, `B39-S4`, `B39-S5`, `B39-TEST-M01..M54`.
- Batch 40 markers: `B40-S2`, `B40-S3`, `B40-S4`, `B40-S5`, `B40-DVL-M22`, `B40-DVL-M23`, `B40-DVL-M24`, `completion_skeptic_manual_pilot_ledger`, `completion_skeptic_go_no_go_closure`, `implemented_pilot_metrics_closure_manual_only`, `manual_only`, `not_promoted`.
- Batch 41 markers: `B41-S1-M01..M05`, `B41-S2-M06..M09`, `B41-S3-M10..M16`, `B41-S4-M17..M20`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `B41-S8-M41..M47`, `B41-S9-M48..M57`, `B41-S7-M34..M35`, `B41-S7-M36..M39`, `B41-S7-M40-OWNER-APPROVAL-A01`, `B41-S7-M40-A01`, `B41-S9-HTML-MODERNIZATION-A01`, `html_redesign_after_owner_review`, `first_run_orchestrator_contract_v1`, `first_run_script_registry_v1`, `first_run_command_matrix_v1`, `first_run_evidence_summary_v1`, `first_run_resume_ledger_v1`, `first_run_project_analysis_summary_v1`, `first_run_methodology_audit_summary_v1`, `first_run_source_policy_summary_v1`, `first_run_graph_dry_run_summary_v1`, `first_run_docs_logging_summary_v1`, `first_run_dependency_readiness_summary_v1`, `first_run_runtime_browser_boundary_v1`, `first_run_artifact_cleanup_guidance_v1`, `first_run_guided_question_protocol_v1`, `first_run_answer_ledger_v1`, `first_run_ambiguous_route_intake_v1`, `first_run_cockpit_artifact_v1`, `architecture_intelligence_design_contract_v1`, `first_run_first_viewport_shell_v1`, `first_run_local_interaction_layer_v1`, `first_run_static_diagram_workbench_v1`, `first_run_schema_contract_surface_v1`, `first_run_graph_file_code_surface_v1`, `first_run_guided_tour_surface_v1`, `first_run_evidence_risk_hierarchy_v1`, `first_run_visual_accessibility_acceptance_v1`, `cosmos_gl_static_adapter_v1`, `first_run_cockpit_navigation_search_v1`, `first_run_progressive_diagnostics_v1`, `first_run_cockpit_static_visual_qa_v1`, `first_run_cockpit_safety_accessibility_v1`, `batch41_s6_synthetic_e2e_summary_v1`, `batch41_s6_closure_packet_v1`, `closed_conditional_go_not_release_ready`, `--full-dry-run`, `--stage <dir>`, `--write-analysis`, `batch41-s1-command-contract-summary.json`, `batch41-s2-script-matrix-summary.json`, `batch41-s3-project-analysis-summary.json`, `batch41-s4-html-artifact-summary.json`, `batch41-s5-guided-questions-summary.json`, `batch41-s6-closure-summary.json`, `batch41-s7-html-cockpit-analysis.txt`, `batch41-s7-m31-m33-cockpit-foundation-summary.json`, `batch41-s7-m34-m35-graph-rendering-summary.json`, `batch41-s7-m36-m39-cockpit-ux-safety-summary.json`, `batch41-s7-m40-owner-approval-packet.json`, `batch41-s7-m40-neural-flow-acceptance-summary.json`, `batch41-s9-html-modernization-summary.json`, `batch41-s9-m57-neural-flow-stage`, `playwright-runtime-proof.json`.
- Batch 42 markers: `B42-S1-M01..M03`, `B42-S2-M04..M06`, `B42-S3-M07..M08`, `B42-S4-M09..M10`, `B42-S5-M11`, `batch42_instruction_tool_use_compliance_matrix_v1`, `planned_task_matrix_added`, `self-learning-loop`, `allow_implicit_invocation`.
- Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix.
- `done_through_m40` is historical status context, not permission for new execution.

## Current Batch 39 Handoff

- Latest completed route: `B39-S5` closure/go-no-go is recorded as source-owned local evidence. Evidence refs: `docs/superpowers/specs/batch39-s5-closure-summary.json`, `docs/superpowers/specs/batch39-s5-go-no-go-decision-packet.json`, `docs/superpowers/specs/batch39-s5-no-unapproved-actions-proof.json`, `docs/superpowers/specs/batch39-s5-owner-feedback-test-plan.json`, `prod_test.md` and focused S5 tests.
- Next active route: manual owner-feedback testing, followed by any separately approved disposable runtime/browser pilot.
- Owner action: run or review the S5 owner-feedback scenarios and approve any escalation beyond local/read-only evidence.
- Codex action: continue Batch 39 attempt entries with technical/product objective, owner/Codex action split, prerequisites, evidence, result, failure/fix/retest and residual risk; keep target evidence redacted and stored under `codex_docs`.
- Approval boundary: no target write, browser automation, provider call, live server, canonical mutation, git write or external action without exact approval.

## Current Batch 41 Handoff

- Latest completed route: `B41-S7-M31..M39` cockpit foundation, graph rendering, UX and safety hardening is recorded through `B41-S7-M31-M33-A01`, `B41-S7-M34-M35-A01` and `B41-S7-M36-M39-A01`.
- Latest completed route: `B41-S7-M40` Neural_Flow acceptance pilot with owner-approved browser visual proof, runtime interaction, WCAG-oriented checks and Cosmos.gl/WebGL blocker recording.
- Latest completed route: `B41-S9-M57` read-only Neural_Flow rerun and static comparison after HTML modernization, with S9 staged artifact, comparison packet, no target mutation, and explicit unsupported-claim guards.
- Evidence refs: see `PLAN.md` Batch 41 rows for the S1-S9 packet list; current shorthand is S7 cockpit foundation/visual proof plus S9 modernization and Neural_Flow static comparison packets.
- Next active route: owner review of the S9 staged Neural_Flow HTML artifact and decision whether a future browser screenshot proof, vendored Cosmos.gl runtime/WebGL slice or target-apply safety slice is needed.
- Approval boundary: no real-target mutation, live server, browser automation, provider/API/MCP call, git write, release/deploy/publish, automation activation or external write without exact approval.

## Current Batch 42 Handoff

- Latest route: `B42-PLANNING-A01` added the planned Track 10 instruction/tool-use compliance matrix.
- Evidence refs: `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`, `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`, `docs/sources/product-agent-os-track-10-backlog.md` and `PLAN.md`.
- Next active route: owner decision on whether to execute Batch 42 as a read-only audit, source-tree implementation, installed-cache refresh path, global Codex policy/config change path or staged combination.
- Approval boundary: no global config write, installed plugin cache write, target mutation, live server, browser automation, provider/API/MCP call, git write, release/deploy/publish, automation activation or external write without exact approval.

## Current Batch 45 Handoff

- `B45-A02/A05/S6`: 6-task pilot, V3 comments/advisory validator and M24-M27 no-go promotion evidence are closed; M25 remains non-blocking and M27 keeps advisory-only, no CI/blocker promotion.
- `B45-S7`: M28-M35 source-only. M35 keeps advisory-only/no-go; no target/runtime/browser/provider/db/git/release/deploy/automation proof.

## Verification Runbook

For docs/control-plane edits, run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Strict MkDocs is required only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

## Residual Risks

- Batch 39 is closed for manual owner-feedback testing only; owner-feedback results and any runtime/browser pilot remain pending.
- `B38-PILOT-NF01` target apply remains blocked by source-policy and target-artifact gaps.
- Batch 40 completion-skeptic automation is still `manual_only` and `not_promoted`.
- Batch 41 remains non-release evidence: S6 has read-only/staged gaps, S7 records M40 static/browser Neural_Flow acceptance, S8-M41..M47 record redesign proof with owner visual acceptance and Cosmos.gl runtime/WebGL still unresolved.
- Historical detail has been intentionally moved out of root control-plane files; future broad historical claims should cite the source backlogs or registry.

<!-- product-agent-os:end runlog -->
```

### Archived TEST.md

```text
# TEST.md

<!-- product-agent-os:start test -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-06-11

## Purpose

`TEST.md` is the compact verification routing layer. It defines which checks are required for current docs, control-plane, plugin/runtime, eval and Batch 39 work. Detailed historical evidence belongs in source-owned backlogs, eval reports, `RUNLOG.md` or `prod_test.md`.

## Required Checks After Docs Or Control-Plane Changes

Run these checks after changes to root control-plane files, docs/source registry, templates or test contracts:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks.json
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
python -m unittest discover -s tests -p "test_*.py" -v
```

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

## Batch 44 S0 Self-Learning Loop Scope Checks

For `B44-S0-Discovery-And-Scope`, run:

```powershell
python -m unittest tests.product_agent_os.test_discovery -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

The scope detector must fail closed for unrelated projects, redact raw workspace
paths by default and remain a detector only. These checks do not prove any
active scheduler, Codex App automation, hidden session ingestion, provider call,
target mutation or auto-apply behavior.

## Batch 44 S1 Self-Learning Loop State And Trigger UX Checks

For `B44-S1-State-And-Trigger-UX`, run:

```powershell
python -m unittest tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_batch41_first_run_automation -v
python -m unittest tests.product_agent_os.test_first_run_analysis -v
python plugins\product-agent-os\scripts\check_self_learning_due.py . --dry-run
```

The due-check CLI must report only `due`, `not_due`, `disabled` or
`state_invalid`; it must not run analysis, write state, create a schedule,
include raw workspace paths or enable auto-apply. First-run help must disclose
the Self-Learning Loop, default `manual_only` mode, cadence choices, manual
due-check trigger and `not_created` schedule boundary. It must not expose a
`run_now` command unless the B44-S2 manual runner exists and remains
manual-only/staged-only. Invalid
`--now` input must return bounded JSON with `now:invalid_datetime` and no
traceback; `on_change` cadence must stay `not_due` until a Product-Agent OS
change trigger exists.

## Batch 44 S2 Self-Learning Loop Manual Runner And Progress Checks

For `B44-S2-Manual-Runner-And-Project-Progress`, run:

```powershell
python -m unittest tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_batch41_first_run_automation -v
python plugins\product-agent-os\scripts\run_self_learning_loop.py . --dry-run
python plugins\product-agent-os\scripts\run_self_learning_loop.py . --stage <stage-dir-outside-workspace>
```

The manual runner must start with Product-Agent OS scope detection, fail closed
for unrelated projects, and emit `self_learning_run_packet_v1` without raw
workspace paths. `--dry-run` must not write files. `--stage` may write only under
the explicit stage root and must produce `progress.jsonl`, per-run
`progress.json`, `self-learning-run-packet.json` and
`self-learning-progress.html`. The HTML artifact is generated review evidence
only; it must not contain external URLs, external scripts, raw chat, hidden
telemetry, auto-approval controls or auto-apply behavior.

## Batch 44 S3 Self-Learning Loop Feedback And Preferences Checks

For `B44-S3-Feedback-And-Preferences`, run:

```powershell
python -m unittest tests.product_agent_os.test_self_learning_state -v
```

Feedback and preference checks must cover `owner_feedback_ledger_v1`,
`codex_session_feedback_import_v1`, `self_learning_satisfaction_report_v1`
and `preference_memory_v1`. They must reject raw chat, raw transcripts,
unredacted rows, PII-like private email strings and absolute user-specific
paths. Import must remain scoped to eligible Product-Agent OS projects with
owner-provided redacted-summary consent. Satisfaction pseudo-labels must stay
low confidence and must not override explicit owner labels. Preference memory
is a compact owner-editable recall aid, not source truth or a policy override.
The manual runner may summarize `.codex/product-agent-os/owner-feedback-ledger.jsonl`
when present, but it must not perform hidden app telemetry, global session
analysis, provider/model calls, target mutation, active automation or auto-apply.

## Batch 44 S6 Self-Learning Loop Docs Contracts And Closure Checks

For `B44-S6-Docs-Contracts-And-Closure`, run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_batch44_s6_self_learning_docs_contracts_and_closure_are_synced -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

The docs closure must expose `self_learning_docs_contracts_closure_v1`, record
`B44-SLL-M15-M16-A01`, keep automation promotion as `candidate_only`, keep the
candidate packet under `.codex/automation-candidates/self-learning-automation-candidate.md`
as a proposal only and include a no active automation marker check. It must not
claim real session import, hidden telemetry, raw transcript ingestion, provider
or live eval calls, target mutation, git/release/deploy/publish, external write
or auto-apply.

## Batch 44 S7 Self-Learning Loop Manual Pilot Checks

For `B44-S7-Approved-Manual-Pilot`, run:

```powershell
python -m unittest tests.product_agent_os.test_self_learning_extensions -v
python -m unittest tests.product_agent_os.test_self_learning_state -v
python plugins\product-agent-os\scripts\init_self_learning_state.py . --stage <stage-dir-outside-workspace> --installed-at 2026-06-01T00:00:00Z
python plugins\product-agent-os\scripts\run_self_learning_loop.py . --stage <stage-dir-outside-workspace> --state-file <staged-self-learning-state.json> --metrics-ledger docs\superpowers\specs\batch44-self-learning-loop-approved-manual-pilot-metrics.jsonl --feedback-ledger docs\superpowers\specs\batch44-self-learning-loop-approved-manual-pilot-feedback.jsonl
python plugins\product-agent-os\scripts\export_self_learning_promptfoo.py . --stage <stage-dir-outside-workspace>
```

The S7 pilot must show that missing workspace state can be recovered through a
stage-only initializer, that the runner can use an explicit staged state file,
and that redacted metrics/feedback ledgers are summarized without raw session
ingestion. Promptfoo/HALO export remains `not_executed` / local-only:
provider/model/API calls, HALO service calls, browser automation, target
workspace writes, active schedules, hooks, git/release/deploy/publish, external
writes and auto-apply must remain absent.

## Batch 45 Professional Code Authoring Checks

For `B45-PILOT-MANUAL-6-CODE-TASKS-A02` owner-approved local manual pilot,
run the focused suites twice for flake replay:

```powershell
python -m unittest tests.product_agent_os.test_automation_policy -v
python -m unittest tests.product_agent_os.test_batch45_s3_professional_code_authoring -v
python -m unittest tests.product_agent_os.test_self_learning_state -v
python -m unittest tests.product_agent_os.test_automation_policy -v
python -m unittest tests.product_agent_os.test_batch45_s3_professional_code_authoring -v
python -m unittest tests.product_agent_os.test_self_learning_state -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

The pilot may record false-positive, flake, cost and reviewer-usefulness
evidence, but it must not claim hook/blocker activation, active automation,
schedule creation, provider/browser/runtime proof, target mutation, git action
or production readiness without a later exact approval.

For `B45-COMMENT-POLICY-ENFORCEMENT-A05` V3 runner comment-sufficiency
corrective work, run:

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency -v
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py .codex\product-agent-os\b45-manual-pilot\v3_reference_runner.py .codex\product-agent-os\b45-manual-pilot\v3_js_runner.mjs
python .codex\product-agent-os\b45-manual-pilot\v3_reference_runner.py --task all
node .codex\product-agent-os\b45-manual-pilot\v3_js_runner.mjs V3-ENT-JS-01
node .codex\product-agent-os\b45-manual-pilot\v3_js_runner.mjs V3-ENT-JS-02
```

The comment-sufficiency validator is advisory only: warnings are reviewer
signals, the CLI exits `0`, and no hook/blocker activation is implied.

For planned `B45-S6` advisory-validation and behavior-proof tasks, keep the
checks split by row:

```powershell
# B45-PCA-M24: broad false-positive audit
python -m unittest tests.product_agent_os.test_comment_sufficiency -v
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py <approved-corpus-paths>
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py <approved-corpus-paths> --include-tests --no-default-excludes --max-warnings-per-file -1 --max-warnings -1

# B45-PCA-M25: non-blocking advisory wiring, only after exact hook/CI approval
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks.json
python plugins\product-agent-os\scripts\validate_hooks.py .codex\hooks
python .codex\hooks\comment_sufficiency_advisory.py
python plugins\product-agent-os\scripts\product_agent_os\comment_sufficiency.py .codex\product-agent-os\b45-manual-pilot\v3_reference_runner.py .codex\product-agent-os\b45-manual-pilot\v3_js_runner.mjs

# B45-PCA-M26: real AI-agent behavior eval
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
# Approved live baseline/treatment model runs were executed for M26; reruns remain approval-required.

# B45-PCA-M27: promotion/no-go decision
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

S6 warnings stay non-blocking; M24-M27 are source-owned, M25 is reversible via `B45_COMMENT_ADVISORY_DISABLED=1`, and CI/blocker promotion, provider, browser, target, plugin-cache and git remain approval-required.

For `B45-PCA-M37-A01` local hardening/docs sync, run:

```powershell
python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python tools\check_docs.py
git diff --check
```

M37 is local advisory hardening/docs sync; `B45-PCA-M36` remains reserved; no provider/target/git/release/deploy/automation or promotion beyond no-go.

For Batch 45 retest/post-Q4 (`B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`), run:

```powershell
python -m unittest tests.product_agent_os.test_codex_runtime_runner_model_output -v
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python tools\check_docs.py
git diff --check
```

Q4 14; T01-T03 `14 -> 0`; T05 timeout; T06/T08/T12 no-go; T10 pkt; T11 src; T13 schema; T14 pkt.
No target proof.

For `B45-S5` learning-loop and automation-candidate policy, run:

```powershell
python -m unittest tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_agent_skill_metrics tests.product_agent_os.test_automation_policy tests.product_agent_os.test_infrastructure_templates -v
python -m unittest tests.product_agent_os.test_coding_standards_artifacts tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_batch45_s3_professional_code_authoring -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
.venv-docs\Scripts\mkdocs.exe build --strict --site-dir .docs-tools\reports\batch45-s5-mkdocs-strict-smoke
git diff --check
```

For `B45-S4` public docs/source cross-linking and closure-through-S4, run:

```powershell
python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v
python -m unittest tests.product_agent_os.test_batch45_coding_standards tests.product_agent_os.test_batch45_s3_professional_code_authoring -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools\reports\batch45-s4-mkdocs-strict-smoke
git diff --check
```

For `B45-S3` eval, readiness, route, HTML and hook-governance visibility, run:

```powershell
python -m unittest tests.product_agent_os.test_batch45_s3_professional_code_authoring tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_discovery tests.product_agent_os.test_status_dashboard tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_fixture_eval_runner -v
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python tools\check_docs.py
git diff --check
```

The focused B45 route must keep Professional Code Authoring as
`docs_contract_ready` / `synthetic_green` / generated-view visibility until
later approved runtime or owner-pilot evidence exists. S5 adds candidate-only
learning-loop and automation-candidate policy with
`minimum_manual_successful_runs: 3`; it does not claim root `site` freshness
for the updated page unless a root site build is approved and run. It must not
claim hook activation, active automation, schedule creation,
provider/browser/runtime proof, plugin-cache refresh, target mutation,
git/release/deploy/publish or real AI-agent behavior improvement from S0-S5.

## Control-Plane Size Budgets

`RUNLOG.md` has a `50 KB` budget, measured as `50 * 1024` UTF-8 bytes. If it exceeds that budget, run `.codex/workflows/control-plane-sync.md` as an overflow protocol: redistribute scope to `REQUIREMENTS.md`, sequencing to `PLAN.md`, verification to `TEST.md`, eval/claim ceilings to `EVALS.md`, detailed evidence to source-owned plans/specs/backlogs or `prod_test.md`, then shorten `RUNLOG.md` to current handoff and residual-risk pointers.

### MkDocs Runtime Location

`requirements.txt` declares the docs runtime:

```text
mkdocs>=1.6,<2
mkdocs-material>=9.5,<9.6
mkdocs-static-i18n>=1.2,<1.3
```

The default `python` in the current Codex App shell can be `C:\Python313\python.exe`; it does not necessarily have MkDocs installed, so plain `python -m mkdocs ...` may fail with `No module named mkdocs`.

Track 11 G1.1 `DOC-M35` installed the current project-local MkDocs runtime on 2026-06-21:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools\reports\mkdocs-strict-smoke-2026-06-21
```

The installed runtime evidence is `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`: `mkdocs==1.6.1`, `mkdocs-material==9.5.50`, `mkdocs-static-i18n==1.2.3`, and strict smoke output under `.docs-tools/reports/`. This smoke build does not refresh root `site/`; generated `site/`, search and sitemap freshness require a current build to `site/` before being claimed.

Historical strict-site builds used target-install dependencies rather than the default Python environment:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'
$env:NO_MKDOCS_2_WARNING='1'
python -m mkdocs build --strict
```

The repository also has a prior workspace-local target install at `tmp\mkdocs_deps_b40s4`; it matches older generated `site/` metadata (`mkdocs-1.6.1`, `mkdocs-material-9.5.50`) and the Batch 40 S4 source evidence. In the 2026-06-20 shell, `tmp\mkdocs_deps_b40s4` was blocked by `PermissionError`, while `C:\tmp\codex_docs_mkdocs` existed but was not usable as a runnable `python -m mkdocs` module from the active process. Treat those paths as historical fallback evidence only; use `.venv-docs\Scripts\python.exe` for current docs-runtime checks.


### Track 11 G1.1 Project-Local Docs Toolchain Checks

G1.1 prepares a repository-owned documentation toolchain. System-file preparation does not install dependencies and does not prove generated `site/` freshness.

Planned local folders:

```text
.venv-docs/
.docs-tools/node/
.docs-tools/bin/
.docs-tools/reports/
docs/assets/javascripts/vendor/  # optional vendored diagram/runtime assets
```

After an approved install slice, verify each enabled layer from project-local paths only:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict
npm.cmd --prefix .docs-tools\node run markdownlint:smoke
npm.cmd --prefix .docs-tools\node run prettier:check:readme
npm.cmd --prefix .docs-tools\node run markdownlint:version
npm.cmd --prefix .docs-tools\node run prettier:version
npm.cmd --prefix .docs-tools\node run redocly:version
.docs-tools\bin\vale.exe --version
.docs-tools\bin\vale.exe --config=.vale.ini .docs-tools\vale\fixtures\doc-m37-smoke.md
.docs-tools\bin\lychee.exe --version
.docs-tools\bin\gitleaks.exe version
.docs-tools\bin\lychee.exe --offline --no-progress .docs-tools\link-secret\fixtures\doc-m38-links.md
.docs-tools\bin\gitleaks.exe dir .docs-tools\link-secret\fixtures --config .gitleaks.toml --redact --no-banner --no-color --exit-code 1 --log-level error
powershell -NoProfile -ExecutionPolicy Bypass -File tools\docs_mermaid_install.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools\docs_mermaid_install.ps1 -Install -AllowNetwork -Force
.venv-docs\Scripts\python.exe -m mkdocs build --strict --site-dir .docs-tools\reports\mkdocs-strict-smoke-doc-m39-2026-06-21
rg -n "https://unpkg.com/mermaid|cdn.jsdelivr.net/npm/mermaid|<script[^>]+src=['""]https?://" .docs-tools\reports\mkdocs-strict-smoke-doc-m39-2026-06-21
```

`DOC-M36` installed `markdownlint-cli2==0.22.1`, `prettier==3.8.4` and `@redocly/cli==2.34.0` under `.docs-tools/node/`. Use Redocly enforcement only when an OpenAPI source contract exists. Use broad docs lint/format checks, `lychee` external-link checks, broad `gitleaks` scans, binary vendoring, Mermaid runtime vendoring, dependency audit/SBOM generation and report retention only after the slice names approval boundary, source, expected output and redaction policy.

`DOC-M37` installed local Vale `3.15.1` under `.docs-tools/bin/` with `.vale.ini`,
`.docs-tools/vale/` rules and `.docs-tools/bin/vale.sha256`. The approved smoke
scope is the local fixture only. Broad docs language scans and any failure
enforcement remain out of scope until thresholds, false-positive handling and
report retention are approved.

`DOC-M38` installed local lychee `0.24.2` and gitleaks `8.30.0` under
`.docs-tools/bin/` with `.docs-tools/bin/lychee.sha256`,
`.docs-tools/bin/gitleaks.sha256`, `.gitleaks.toml` and
`.docs-tools/link-secret/` fixtures. The approved smoke scope is offline local
link fixture checking and redacted clean secret fixture checking only. External
URL crawling, broad docs link checks, broad repository secret scans, raw finding
publication and report retention remain out of scope until a later slice names
the scope, redaction policy and retention boundary.

`DOC-M39` vendored Mermaid `10.9.6` under `docs/assets/javascripts/vendor/`
with `mermaid-10.9.6.min.js.sha256`, `mermaid-10.9.6.LICENSE.txt` and
`mermaid-10.9.6.package.json`. The approved smoke scope is strict MkDocs build
to `.docs-tools/reports/mkdocs-strict-smoke-doc-m39-2026-06-21` plus static
external Mermaid/script audit. Browser rendering, console/network cleanliness,
responsive visual quality, root `site` freshness and dependency safety remain
out of scope until later approved evidence exists.

`DOC-M40` records dependency audit and SBOM governance for the docs toolchain.
Use `tools\docs_dependency_audit.ps1` for local Python inventory, `pip check`,
Node CycloneDX SBOM generation and checksum consistency. The approved network
audit evidence is `npm.cmd --prefix .docs-tools\node audit --audit-level=high
--json`: current Node audit reports 3 moderate findings and 0 high/critical
findings. Do not run `npm audit fix`, `npm update`, dependency upgrades,
`pip-audit` installation, raw report retention or remediation without a separate
approved dependency remediation slice. Python vulnerability audit, complete
repository SBOM, standalone binary SBOM and Mermaid vulnerability audit remain
unsupported.

`DOC-M41` records deferred platform trigger governance for Docusaurus,
Storybook and Structurizr DSL. It is a source-owned decision/trigger record
only: no deferred platform install, download, scaffold, root `site` rebuild,
browser proof, render proof or publication action is approved by this evidence.
If a future requirement triggers one of these tools, first create an
owner-approved platform decision record naming trigger evidence, local install
path, rollback, verification gates and unsupported claims.

## Required Checks After Plugin Or Runtime Changes

Use focused checks first, then broaden through the relevant project route:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest discover tests -v
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
git diff --check
```

If a slice changes Product-Agent OS plugin behavior, also inspect the matching fixture/eval/transcript checks referenced by the source plan or backlog before making readiness claims.

Use `timeout_ms: 1200000` for full Product-Agent OS unittest runs.

## Batch 39 Verification Contract

- `prod_test.md` is the required attempt/failure/fix/retest ledger for `B39-TEST-M01..M54`.
- Future Batch 39 pilots should include real-project target evidence where it improves Product-Agent OS confidence. Internal `codex_docs` fixtures remain valid for deterministic contracts, but they do not replace real target discovery when the route depends on project shape, source policy, runtime signals or user workflow.
- Every Batch 39 task must record:
  - setup and prerequisites;
  - owner action and Codex action;
  - exact command/manual step;
  - observed evidence;
  - result status;
  - failure, fix and retest loop if applicable;
  - residual risk or accepted gap.
- Do not treat a planned test matrix as execution evidence.
- Do not treat generated dashboards, generated reports or project graphs as proof unless backed by source artifacts, current command evidence, current runtime evidence or an explicit accepted gap.

## Runtime And External-Action Boundaries

Runtime And External-Action Verification Boundaries

Fresh explicit approval is required before:

- target workspace mutation;
- browser automation;
- provider/API calls;
- live server or dashboard launch;
- canonical graph-source mutation;
- git branch creation/switching, stage, commit, push, tag or PR;
- publication, deployment or external automation creation.

Approval for one surface does not authorize another. Runtime launch approval does not authorize browser automation; browser approval does not authorize provider calls; provider-call approval does not authorize canonical mutation or git/release actions.

For real-project target tests, the default verification mode is read-only: inventory, route classification, source-policy status, control-plane presence, safe artifact maps, counts, digests and redacted summaries. Build/test/runtime/browser/provider/database/git/release actions require exact approval before execution.

## Current Verification State

| Area | Current evidence state | Required next check |
| --- | --- | --- |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no git writes occurred. | Fresh git preflight and exact approval before any future git write. |
| Batch 38 cache/readiness | `B38-S2` current evidence records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat as historical unless a new cache mutation is requested. |
| `B38-PILOT-NF01` | Docs-only pilot addendum; target apply blocked by `source_policy_status: blocked`. | Resolve target source policy and target control-plane artifacts before target mutation. |
| Batch 39 | `B39-S1` through `B39-S5` are current through `B39-S5-CLOSURE-A01`. S5 evidence closes source-doc sync, go/no-go and no-unapproved-actions proof as `closed_for_owner_feedback_testing_not_release_ready`: release is `no_go`, owner-feedback testing is `conditional_go`, runtime/browser pilot is `approval_required`, and promotion remains `manual_only_not_promoted`. | Run owner-feedback tests from `batch39-s5-owner-feedback-test-plan.json`; keep S4/S5 focused tests, full unittest, fixture/transcript eval, Codex compatibility, docs check and diff hygiene before any stronger readiness claim. |
| Batch 40 completion-skeptic | Local manual loop closed as `manual_only` and `not_promoted`. | Automation promotion requires manual success evidence, eval cases, owner, cadence, stop condition and rollback/disable path. |
| Batch 41 first-run orchestration | `B41-S1-M01..M05`, `B41-S2-M06..M09`, `B41-S3-M10..M16`, `B41-S4-M17..M20`, `B41-S5-M21..M23` and `B41-S6-M24..M30` are recorded as local/read-only/staged CLI/contract behavior. Owner review of the Neural_Flow artifact exposed that structurally valid first-run HTML is not product-usable; `B41-S7-M31..M40` added cockpit/static/browser evidence and conditional Neural_Flow acceptance. A later owner review still rejected the HTML as too text-file-like and missing architecture diagrams, so `B41-S8-M41..M47` is now planned for architecture-dossier redesign, diagram panels, visual shell, evidence/decision sections, graph runtime/fallback clarity, Playwright visual/a11y acceptance and regenerated Neural_Flow before/after proof. | S8 verification must include focused renderer tests, diagram render/fallback checks, Playwright desktop/mobile screenshots, interaction checks, console/network result, accessible-name/landmark checks, no-overlap visual review and completion-skeptic unsupported-claim review. Cosmos.gl/WebGL runtime execution remains blocked unless a later vendored-runtime slice is approved; no release readiness, target apply safety, provider/API call, git/release action, external write or installed-plugin readiness claim is approved. |
| Batch 42 instruction/tool-use compliance | `B42-S1-M01..M03`, `B42-S2-M04..M06`, `B42-S3-M07..M08`, `B42-S4-M09..M10` and `B42-S5-M11` are planned only in `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`. | When approved for execution, run source/cache/session inventory, official-doc source check, implicit-invocation metadata validation, runtime route tests, instruction/tool-use evals, hygiene checks, Codex compatibility, docs checks, diff hygiene and fresh-session proof if required. Do not claim Product-Agent OS auto-engagement is fixed from the planning matrix alone. |
| Batch 44 Self-Learning Loop | `B44-S0` through `B44-S7` are current local/schema/fixture/docs/staged-manual-pilot evidence. S7 adds stage-only state initializer, explicit `--state-file` runner path, redacted feedback/metrics pilot inputs, durable eval cases, Promptfoo export, HALO-style packet and staged repair worker contract. | Run focused S7 self-learning tests, manual pilot commands, docs unittest, `python tools\check_docs.py`, strict MkDocs for nav-sensitive docs and `git diff --check`. No real session import, hidden telemetry, raw transcript, live eval/provider/model call, HALO service call, Promptfoo run, target mutation, active automation, git/release/deploy/publish, external write or auto-apply evidence is provided by S7. |
| Agent lifecycle, hooks and control-plane sync | Current local agents, packaged agent templates, workflows, config templates and `agent-context-contract` require config-routed Task Brief / Completion Brief plus control-plane sync before completion. Project-local `.codex/hooks.json` is installed through `product_agent_os_LIFECYCLE-HOOKS-A01`; hook scripts and the Product-Agent OS policy mirror live under `.codex/hooks/`. `PreToolUse` blocks mutating Product-Agent OS commands when `.codex/product-agent-os/lifecycle-state.json` is missing or only has the legacy minimal marker; accepted marker schema is `task_start_brief_v1` with full `brief_fields_present`. | Rerun task lifecycle, `validate_hooks.py .codex\hooks.json`, `validate_hooks.py .codex\hooks`, infrastructure template, docs, docs-structure and diff hygiene checks after future changes to this contract. Codex hook trust review / new-session execution remains a manual runtime boundary. |
| Track 11 G1.1 docs toolchain | System files route project-local documentation tooling through `.venv-docs/`, `.docs-tools/node/`, `.docs-tools/bin/`, `.docs-tools/vale/`, `.docs-tools/link-secret/`, `.docs-tools/reports/` and `docs/assets/javascripts/vendor/`. `DOC-M35` installed the MkDocs runtime and passed a strict smoke build under `.docs-tools/reports/`; `DOC-M36` installed Node docs tooling and passed scoped README markdownlint/Prettier smoke; `DOC-M37` installed Vale and passed advisory fixture/negative wording smoke; `DOC-M38` installed lychee/gitleaks and passed scoped offline link plus redacted clean secret fixture smokes; `DOC-M39` vendored Mermaid and switched MkDocs to the local asset; `DOC-M40` records local dependency inventory, Node CycloneDX SBOM generation and current Node advisory counts; `DOC-M41` records deferred platform trigger governance for Docusaurus, Storybook and Structurizr DSL with no install or site rebuild. Root `site/`, browser Mermaid rendering, broad docs lint/format, broad Vale enforcement, broad link/secret scans, external URL crawling, report retention, Redocly enforcement, Python vulnerability audit, complete repository SBOM, dependency remediation and deferred platform runtime/readiness are not proven by that state. | Use `.venv-docs\Scripts\python.exe` for MkDocs checks, `npm.cmd --prefix .docs-tools\node run ...` for Node checks, `.docs-tools\bin\vale.exe --config=.vale.ini ...` for approved advisory Vale scopes, `.docs-tools\bin\lychee.exe --offline ...` for approved local link scopes, `.docs-tools\bin\gitleaks.exe dir ... --redact ...` for approved secret scopes, `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js` as static vendor evidence and `tools\docs_dependency_audit.ps1` for local dependency/SBOM governance. Before claiming root `site`, search or sitemap freshness, run a current build to `site/`; before claiming Python vulnerability safety or remediation, run a separately approved audit/remediation slice; before claiming browser diagram rendering or deferred platform readiness, run an approved proof slice. |
| Track 11 G2 first-run cockpit/artifact docs | Source docs and nav/test routing are implemented through `documentation_refresh_G2-A01`; the new cockpit page is intentionally in `DOC_M25_PENDING_SITE_PAGES`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g2-2026-06-21` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`. |
| Track 11 G3 diagram atlas/architecture maps | Source docs and nav/test routing are implemented through `documentation_refresh_G3-A01`; the five new diagram pages are intentionally in `DOC_M25_PENDING_SITE_PAGES`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g3-2026-06-21` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`; browser proof and Structurizr DSL evidence remain approval-required. |
| Track 11 G4 operator flows/system behavior docs | Source docs and nav/test routing are implemented through `documentation_refresh_G4-A01`; the four new Product-Agent OS pages are intentionally in `DOC_M25_PENDING_SITE_PAGES`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g4-2026-06-22` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`; auto-engagement/cache/global config/fresh-session proof remains unsupported. |
| Track 11 G5 evidence quality/final site gate docs | Source docs and nav/test routing are implemented through `documentation_refresh_G5-A01`; the five new Product-Agent OS pages are intentionally in `DOC_M25_PENDING_SITE_PAGES`, while `DOC-M25` remains `approval_required_not_run`. | Run docs unittest, `tools\check_docs.py`, strict MkDocs smoke to `.docs-tools\reports\mkdocs-strict-smoke-g5-2026-06-22` for source/nav proof and `git diff --check`; do not claim root `site`/search/sitemap freshness until final `DOC-M25`; browser proof, broad scans, dependency remediation and raw report retention remain approval-required. |
| Track 11 DOC-M25 generated site freshness | Source-owned evidence is `documentation_refresh_DOC-M25-A01`; former `DOC_M25_PENDING_SITE_PAGES` are promoted into the root site parity contract. | Run `.venv-docs\Scripts\python.exe -m mkdocs --version`, `.venv-docs\Scripts\python.exe -m mkdocs build --strict`, `powershell -NoProfile -ExecutionPolicy Bypass -File tools\fix_site_i18n_links.ps1 -SiteDir site`, `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python -B tools\check_docs.py` and `git diff --check`; this proves root `site`/search/sitemap freshness and local-file i18n link hygiene only, not browser proof, broad scans, remediation, raw report retention, publication, release, deploy or git actions. |

## Historical Evidence Owners

| Marker | Evidence owner |
| --- | --- |
| `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `blocked_pending_explicit_cache_mutation_approval`, `B38-S2` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `B39-TEST-M01..M54`, `B39-S1..B39-S5` | `PLAN.md`, `prod_test.md` |
| `B40-S2..B40-S5`, `manual_only`, `not_promoted` | `docs/sources/product-agent-os-track-10-backlog.md`, `RUNLOG.md` |
| `B41-S1-M01..M05` | `docs/superpowers/specs/batch41-s1-command-contract-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S2-M06..M09` | `docs/superpowers/specs/batch41-s2-script-matrix-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S3-M10..M16` | `docs/superpowers/specs/batch41-s3-project-analysis-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S4-M17..M20` | `docs/superpowers/specs/batch41-s4-html-artifact-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S5-M21..M23` | `docs/superpowers/specs/batch41-s5-guided-questions-summary.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S6-M24..M30` | `docs/superpowers/specs/batch41-s6-closure-summary.json`, `docs/superpowers/specs/batch41-s6-synthetic-e2e-summary.json`, `docs/superpowers/specs/batch41-s6-real-target-pilots-summary.json`, `docs/superpowers/specs/batch41-s6-usefulness-scorecard.json`, `docs/superpowers/specs/batch41-s6-verification-sweep-summary.json`, `docs/superpowers/specs/batch41-s6-plugin-cache-readiness.json`, `docs/superpowers/specs/batch41-s6-no-unapproved-actions-proof.json`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, `RUNLOG.md` |
| `B41-S7-M31..M40` | `docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json`, `docs/superpowers/specs/batch41-s7-m34-m35-graph-rendering-summary.json`, `docs/superpowers/specs/batch41-s7-m36-m39-cockpit-ux-safety-summary.json`, `docs/superpowers/specs/batch41-s7-m40-owner-approval-packet.json`, `docs/superpowers/specs/batch41-s7-m40-neural-flow-acceptance-summary.json`, `docs/superpowers/specs/batch41-s7-m40-neural-flow-stage/`, `output/playwright/b41-s7-m40/playwright-runtime-proof.json`, `docs/superpowers/specs/batch41-s7-html-cockpit-analysis.txt`, `docs/superpowers/specs/batch41-first-run-automation-matrix.json`, focused cockpit renderer tests, `RUNLOG.md` |
| `B41-S8-M41..M47` | `docs/superpowers/specs/batch41-first-run-automation-matrix.json`; `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-artifact.txt`; `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-summary.json`; `docs/superpowers/specs/batch41-s8-m42-architecture-diagram-layer-summary.json`; `docs/superpowers/specs/batch41-s8-m43-cockpit-shell-redesign-summary.json`; `output/playwright/b41-s8-m42/playwright-diagram-proof.json`; `output/playwright/b41-s8-m43/playwright-shell-proof.json`; future S8 implementation summaries, regenerated Neural_Flow stage artifact, Playwright desktop/mobile screenshots, diagram render/fallback evidence, no-overlap proof, WCAG-oriented browser checks and completion-skeptic packet |
| `B42-S1..S5` | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`; Track 10 plan Batch 42 addendum; Track 10 backlog Batch 42 planned addendum; future source/cache/session exposure packet; future official-doc source packet; future implicit-invocation validator evidence; future runtime route/eval evidence; future fresh-session proof if required |
| `B44-S0..S7` | `docs/superpowers/specs/batch44-self-learning-loop-current-gap-audit.json`; `docs/superpowers/specs/batch44-self-learning-loop-scope-detector-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-state-trigger-ux-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-manual-runner-progress-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-feedback-preferences-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-metrics-evals-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-candidate-safety-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-docs-contracts-closure-summary.json`; `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; focused state/extensions/docs tests; `RUNLOG.md` |
| `DOC-M34..DOC-M41` | `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m34-folder-contract-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-preflight-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-install-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m36-node-tooling-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m37-vale-language-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m38-link-secret-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m39-mermaid-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m40-dependency-audit-summary.json`; `docs/superpowers/specs/documentation-refresh-g1-1-doc-m41-deferred-platform-triggers-summary.json`; `.gitignore`; `.docs-tools/README.md`; `.docs-tools/node/package.json`; `.docs-tools/node/package-lock.json`; `.docs-tools/bin/vale.sha256`; `.docs-tools/bin/lychee.sha256`; `.docs-tools/bin/gitleaks.sha256`; `.gitleaks.toml`; `docs/assets/javascripts/vendor/README.txt`; `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js`; `docs/assets/javascripts/vendor/mermaid-10.9.6.min.js.sha256`; `tools/docs_install.ps1`; `tools/docs_node_install.ps1`; `tools/docs_vale_install.ps1`; `tools/docs_link_secret_install.ps1`; `tools/docs_mermaid_install.ps1`; `tools/docs_dependency_audit.ps1`; `REQUIREMENTS.md`; `PLAN.md`; `TEST.md`; `EVALS.md`; `AGENTS.md`; `RUNLOG.md` |
| Track 8 | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 | `docs/sources/product-agent-os-track-9-backlog.md` |
| Source registry | `docs/sources/registry.md` |
| Batch 35 | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Compatibility Marker Bank

- B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18`, task-matrix contract, `task-matrix-plan.md`.
- B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17`, `renderer_file_count: 195`, plugin cache remains stale until an explicit publication/cache refresh action is approved.
- B37-S3 `T10-PLAN-M06`, `T10-PLAN-M10`, `T10-PLAN-M13`, `validate_task_matrix.py`, `task_matrix_validator_contract_present`.
- B37-S4 `T10-PLAN-M07..M09`, `T10-PLAN-M20`, `task_matrix_planner_routing_contract_present`, `task_matrix_agent_handoff_contract_present`, `task_matrix_discovery_signal_contract_present`, `task_matrix_planning_control_governance_present`.
- B37-S5 `T10-PLAN-M11..M12`, `T10-PLAN-M14..M16`, `T10-PLAN-M19`, `task_matrix_docs_source_sync_present`, `task_matrix_backward_compatibility_policy_present`, `task_matrix_status_projection_deferred_present`, `task_matrix_system_file_hygiene_owner_present`, `task_matrix_lifecycle_archive_policy_present`.
- B38-S1 release gate/package metadata run; focused docs contract; Codex compatibility returned `status: compatible`; strict MkDocs was not run.
- M01 is owner-closed as no-op after historical missing release fields; M02 freezes the checked-in package source; M03 records the owner decision to keep Product-Agent OS local-only/internal R&D.
- M41 post-B38 audit; historical_preflight_snapshot; fresh git status/unrelated-change preflight; B37/B38/B38-S1 did not themselves close M41.
- B38-S2 verification/install smoke run; full unittest ran 846 tests with `OK`; fixture eval exited `0`; transcript eval exited `0` with 19 sessions and 0 failures; plugin cache inspection found stale installed cache; plugin_cache_refresh_attempt_status: blocked_sandbox_cache_write_denied_after_backup_stage; local_cache_refresh_result: REFRESH_OK; target_cache_still_stale: false.
- B38-S3 real-project pilot design run; docs contract; strict MkDocs; real project pilot execution was not run.
- B38-S4 safety and rollback run; validate_source_policy.py; validate_system_file_hygiene.py; secret_like_findings: 6; validate_codex_compatibility.py; not a security certification; No cache/global config mutation.
- B38-PILOT-NF01 `Neural_Flow` target pilot run; detect_project.py; run_methodology_audit.py; run_codex_runtime_runner.py; render_infrastructure.py --stage; scan_project_code_graph.py --stage; validate_source_policy.py; source_policy_status: blocked; false `pr_review` route; 481 nodes; Dashboard aggregation remains incomplete; staged hooks require exact approval; secret_like_findings: 0; No target mutation.
- B39 S2/S3 markers: `B39-TEST-M21-A01..A03`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`; generated first-run views remain orientation-only, read-only real-target evidence is not release readiness, and S3 is functional regression/repeatability evidence only.
- B40-S4 implements Doubt / verifier loop docs/site/source-transfer; strict MkDocs.
- B40-S5 implements Doubt / verifier loop pilot metrics and closure; completion_skeptic_manual_pilot_ledger; completion_skeptic_go_no_go_closure.
- B41-S1 implements first-run command/UX contract rows `B41-S1-M01..M05`: `first_run_orchestrator_contract_v1`, no-args help, `--full-dry-run`, external `--stage <dir>`, `--write-analysis`, stage-inside-target block, and renderer stage output support.
- B41-S2 implements help-only script-matrix rows `B41-S2-M06..M09`: `first_run_script_registry_v1`, `first_run_command_matrix_v1`, `first_run_evidence_summary_v1`, `first_run_resume_ledger_v1`, skipped approval/live boundaries and no raw stdout/stderr retention.
- B41-S3 implements project-analysis rows `B41-S3-M10..M16`: `first_run_project_analysis_summary_v1`, `first_run_methodology_audit_summary_v1`, `first_run_source_policy_summary_v1`, `first_run_graph_dry_run_summary_v1`, `first_run_docs_logging_summary_v1`, `first_run_dependency_readiness_summary_v1` and `first_run_runtime_browser_boundary_v1`.
- B41-S4 implements HTML artifact rows `B41-S4-M17..M20`: orchestrator renderer output in stage/write-analysis modes, multi-page HTML project summaries, previous-baseline comparison in CLI/HTML/manifest, and cleanup/rollback guidance as preview-only with no deletion by default.
- B41-S5 implements guided question rows `B41-S5-M21..M23`: `first_run_guided_question_protocol_v1`, `first_run_answer_ledger_v1`, `first_run_ambiguous_route_intake_v1`, top-level `first_response`, packet `question_queue`, staged `answer-ledger-template.json` and route options without blocking deterministic read-only analysis.
- B41-S6 records first-run QA/closure rows `B41-S6-M24..M30`: `batch41_s6_synthetic_e2e_summary_v1`, `batch41_s6_real_target_pilot_summary_v1`, `batch41_s6_usefulness_scorecard_v1`, `batch41_s6_verification_sweep_summary_v1`, `batch41_s6_plugin_cache_readiness_v1`, `batch41_s6_no_unapproved_actions_proof_v1` and `batch41_s6_closure_packet_v1`; release remains `no_go`, owner-feedback testing is `conditional_go`, runtime/browser and target apply are `approval_required`, M26 is `blocked_timeout`, and M29 is `blocked_expected_approval_required`.
- B41-S7 cockpit-grade HTML artifact rows `B41-S7-M31..M40` are implemented with local/static and browser evidence for `first_run_cockpit_artifact_v1`, a primary single-file cockpit shell, a bounded view-model adapter, file/source graph, Cosmos.gl static adapter payload, selected-file panel, table fallback, code-graph empty/summary states, static search/filter controls, progressive diagnostics, static visual QA and offline/privacy/accessibility contracts. `B41-S7-M40` captured Playwright screenshots and static interaction evidence for the Neural_Flow cockpit artifact; Cosmos.gl/WebGL runtime execution remains blocked by missing vendored runtime asset and script-free fallback.
- B41-S8 architecture-dossier redesign rows `B41-S8-M41..M47` are implemented after owner review rejected the M40 HTML as still too text-file-like and missing project architecture diagrams. `B41-S8-M41` is implemented as design-contract-only with evidence in `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-artifact.txt` and `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-summary.json`. `B41-S8-M42` is implemented with static architecture diagram layer evidence in `docs/superpowers/specs/batch41-s8-m42-architecture-diagram-layer-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m42/playwright-diagram-proof.json`. `B41-S8-M43` is implemented with architecture-dossier shell evidence in `docs/superpowers/specs/batch41-s8-m43-cockpit-shell-redesign-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m43/playwright-shell-proof.json`. `B41-S8-M44` is implemented with visible evidence/decision/risk/source-blueprint section evidence in `docs/superpowers/specs/batch41-s8-m44-evidence-decision-risk-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m44/playwright-evidence-decision-proof.json`. `B41-S8-M45` is implemented with Graphology/Cosmos.gl static-vs-runtime boundary evidence in `docs/superpowers/specs/batch41-s8-m45-graph-runtime-boundary-summary.json` and desktop/mobile Playwright proof in `output/playwright/b41-s8-m45/playwright-graph-runtime-proof.json`; WebGL runtime execution remains explicitly not claimed. `B41-S8-M46` is implemented with visual/interaction/accessibility-oriented Playwright evidence in `docs/superpowers/specs/batch41-s8-m46-visual-a11y-acceptance-summary.json` and `output/playwright/b41-s8-m46/playwright-visual-a11y-proof.json`; WCAG certification remains explicitly not claimed. `B41-S8-M47` is implemented with regenerated Neural_Flow before/after evidence in `docs/superpowers/specs/batch41-s8-m47-neural-flow-before-after-summary.json`, staged artifact `docs/superpowers/specs/batch41-s8-m47-neural-flow-stage/` and proof `output/playwright/b41-s8-m47/playwright-neural-flow-before-after-proof.json`; final owner acceptance remains pending screenshot review.
- B42 instruction/tool-use compliance matrix is planned only. It must later verify Product-Agent OS source/cache/session skill exposure, official OpenAI/Codex source claims, implicit invocation policy, metadata validator behavior, runtime route/eval behavior for compliance prompts and `self-learning-loop`, system-file hygiene triage and fresh-session exposure before any fixed-auto-engagement claim.

## Completion Claim Rule

Do not say that a feature works, a bug is fixed, tests pass, a release is ready, or behavior is verified unless:

- the relevant check ran in the current run; or
- the claim is explicitly scoped to earlier evidence and the evidence owner is named; or
- the missing verification is recorded as an accepted gap.

<!-- product-agent-os:end test -->
```

### Archived EVALS.md

```text
# EVALS.md

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
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
- Docs-toolchain evidence: project-local tool folders, install manifests, smoke checks, strict MkDocs, lint, terminology, link/secret hygiene and audit/SBOM outputs are separate evidence classes; planning a folder is not dependency evidence, and generated `site/` is not fresh until rebuilt in the current run.
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
- Batch 39 S4 graph-depth partial: `B39-S4-GRAPH-DEPTH-S0-S2-A01` adds current local graph-depth contract evidence, `B39-S4-GD-S0-A01` adds the ontology/parser decision artifact, `B39-S4-GD-S1-A01` adds mixed Python+TypeScript+contract/schema/docs fixture evidence, `B39-S4-GD-S3-A01` adds conservative linker/rejected-link evidence, `B39-S4-GD-S3-A02` adds framework semantics metadata evidence, `B39-S4-GD-S4-A01` adds coverage/freshness evidence, `B39-S4-GD-S6-A01` adds an agent reading packet contract, `B39-S4-GD-S6-SCORECARD-A01` adds local graph usefulness scorecard/threshold evidence, `B39-S4-GD-S10-S13-S15-A01` adds artifact/status/HTML integration evidence and `B39-S4-GRAPH-DEPTH-03-A01` adds read-only SOL real-target graph-depth comparison evidence. Evidence refs are `docs/superpowers/specs/batch39-s4-graph-depth-s0-s2-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s0-ontology-parser-decision.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s1-mixed-fixture-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s3-conservative-linker-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s3-framework-semantics-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s4-coverage-freshness-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s6-agent-reading-packet-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s6-scorecard-threshold-summary.json`, `docs/superpowers/specs/batch39-s4-graph-depth-s10-s13-s15-artifact-status-html-summary.json` and `docs/superpowers/specs/batch39-s4-graph-depth-03-real-target-retest-summary.json`. The eval value is that a stdlib-only TypeScript/JavaScript adapter can emit conservative module/function/class graph entities without adding new ontology node types or external parser dependencies, `impact` / `affected_tests` now honor reverse `max_depth`, invalid or unbounded query limits are blocked instead of silently normalized, framework terms remain metadata/static hints instead of node types, one synthetic graph can orient across backend, frontend, tests, docs, API contract, schema and stale-delta signals while exposing weak TS imports as unresolved inventory, conservative static links only connect exact normalized function/operation names while weak candidates stay in rejected-link evidence, framework hints surface React/Next/Vite/Electron/Tauri static evidence with false-positive rejection and no runtime claims, coverage/freshness surfaces make graph blind spots and stale action-claim blocking explicit, the graph query layer can return a source-first, read-only agent packet, `graph_usefulness_scorecard_v1` can record local fixture metrics and thresholds while keeping promotion gated, first-run/status/HTML generated views can surface bounded graph packet summaries without raw source, absolute paths, external refs or proof claims, and the SOL retest shows bounded real-target orientation delta with 2,830 nodes / 2,914 edges / 5,751 observations versus prior 2,539 / 2,551 / 5,090 baseline. This is bounded read-only orientation evidence only; it does not prove source-read completion, semantic correctness of every graph edge, runtime/browser/provider behavior, target apply safety, public docs/site acceptance, release readiness, promotion or automation readiness.
- Batch 39 S4 docs/offline/CLI partial: `B39-S4-M37-M39-A01` adds current local hardening evidence for `B39-TEST-M37..M39`. Evidence ref is `docs/superpowers/specs/batch39-s4-m37-m39-hardening-summary.json`. The eval value is that first-run generated pages are explicitly classified as internal/generated orientation evidence with public readiness `not_claimed`, first-run HTML has a local no-external-URL/no-script audit, and the first-run CLI matrix records `--dry-run`, `--write`, ambiguous mode rejection, `--stage` rejection and unsafe packet rejection. This is not full public docs/site acceptance, not a fresh rendered-site proof, not full offline/dependency readiness, not an all-script CLI matrix, not runtime/browser/provider proof, not target mutation safety, not release readiness, not promotion and not automation readiness.
- Batch 39 S4 full hardening packet: `B39-S4-FULL-HARDENING-A01` adds current read-only SOL 0.6 / Neural_Flow evidence for static offline/dependency readiness, all-script `--help` CLI matrix and runtime/browser harness blockers. Evidence refs are `docs/superpowers/specs/batch39-s4-all-script-cli-matrix.json`, `docs/superpowers/specs/batch39-s4-full-hardening-sol_0_6-summary.json`, `docs/superpowers/specs/batch39-s4-full-hardening-neural_flow-summary.json` and `docs/superpowers/specs/batch39-s4-full-hardening-comparison.json`. The eval value is that Product-Agent OS can now separate product manifests from dependency/generated corpora, expose and then clear script help-contract gaps across 32 top-level CLIs, preserve selected target digests before/after read-only checks and compare current target graphs with previous baselines. SOL remains partial-pass static inventory only because runtime/browser execution would mutate `.next` / `.sol_data` and can touch provider-sensitive backend surfaces; Neural_Flow remains docs/research-only with no runtime manifest. This is not runtime/browser proof, not provider/API proof, not dependency install/supply-chain audit proof, not target apply safety, not release readiness, not promotion and not automation readiness.
- Batch 39 S4 remaining gates: `B39-S4-REMAINING-GATES-A01` adds current evidence for `B39-TEST-M41..M54` plus reopened M37/M39 status. Evidence refs are `docs/superpowers/specs/batch39-s4-remaining-gates-summary.json` and `docs/superpowers/specs/batch39-s4-closure-readiness-matrix.json`. The eval value is that remaining production/mass-user gates are no longer planned-only: graph review/canonical mutation, security/privacy, templates, skills/subagents, MCP/Context7, onboarding, cross-platform, source freshness, HTML usability, LLM-as-judge, retention, incident/recovery and release governance now have explicit contract evidence or approval blockers. This still does not support release readiness: MkDocs is unavailable, runtime/browser requires a disposable approved pilot, live MCP/external surfaces require approval, and S5 keeps release/distribution at `no_go`.
- Batch 39 S4 verification sweep: full discovery exposed and then closed `B39-FIX-M40-PARTIAL-LANGUAGE-SUMMARY-001`, where graph analysis needed to separate partially supported TypeScript/JavaScript from unsupported languages. Current evidence is focused graph-analysis 2/2, S4 hardening 11/11, docs contract 81/81, fixture eval OK, transcript eval 26/26, Codex compatibility `compatible`, `check_docs.py` OK, `git diff --check` OK and full unittest discovery 983 OK / 1 skipped.
- Batch 39 S5 closure/go-no-go: `B39-S5-CLOSURE-A01` adds source-doc sync, go/no-go and no-unapproved-actions proof evidence. Evidence refs are `docs/superpowers/specs/batch39-s5-closure-summary.json`, `docs/superpowers/specs/batch39-s5-go-no-go-decision-packet.json`, `docs/superpowers/specs/batch39-s5-no-unapproved-actions-proof.json` and `docs/superpowers/specs/batch39-s5-owner-feedback-test-plan.json`. The eval value is that S4 blockers are converted into an explicit decision surface: release/distribution is `no_go`, owner-feedback testing is `conditional_go`, runtime/browser pilot is `approval_required`, and all high-impact surfaces remain not performed without exact approval.
- Batch 41 S6 first-run QA/closure: `B41-S6-CLOSURE-A01` adds current local/read-only/staged evidence for synthetic E2E, Neural_Flow expected-block pilot, usefulness scorecard, verification sweep packet, plugin-cache readiness check and no-unapproved-actions proof. Evidence refs are `docs/superpowers/specs/batch41-s6-synthetic-e2e-summary.json`, `docs/superpowers/specs/batch41-s6-real-target-pilots-summary.json`, `docs/superpowers/specs/batch41-s6-usefulness-scorecard.json`, `docs/superpowers/specs/batch41-s6-verification-sweep-summary.json`, `docs/superpowers/specs/batch41-s6-plugin-cache-readiness.json`, `docs/superpowers/specs/batch41-s6-no-unapproved-actions-proof.json` and `docs/superpowers/specs/batch41-s6-closure-summary.json`. The eval value is that first-run UX can be judged on clarity, actionability, safety, completeness and noise while unsupported claims remain separated; owner feedback is still pending, M26 app-like target evidence is `blocked_timeout`, installed plugin-cache readiness is approval-required, and release/runtime/browser/target-apply readiness is not claimed.
- Batch 41 S7 cockpit foundation: `B41-S7-M31-M33-A01` adds current local/static evidence for `first_run_cockpit_artifact_v1`, primary `index.html` cockpit shell and a bounded view-model adapter. Evidence ref is `docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json`. The eval value is that first-run artifact UX now has a testable product contract and can reject plain diagnostic white-page output, while Cosmos.gl rendering, graph interaction, visual/browser QA, Neural_Flow acceptance and release/readiness claims remain unsupported until `B41-S7-M34..M40`.
- Batch 41 S7 graph rendering: `B41-S7-M34-M35-A01` adds current local/static evidence for a Graphology-compatible file/source graph, Cosmos.gl static adapter payload, selected-file panel, status/cluster legend, bounded table fallback, omitted counts, explicit code-graph `not_available` state and code-graph summary/hotspot surface when `graph_artifact_summary` exists. Evidence ref is `docs/superpowers/specs/batch41-s7-m34-m35-graph-rendering-summary.json`. The eval value is that the cockpit now has graph-shaped orientation surfaces instead of text-only summaries. It does not prove Cosmos.gl runtime/WebGL execution, browser responsiveness, source-read completion, visual QA, Neural_Flow acceptance, release readiness or target apply safety.
- Batch 41 S7 cockpit UX and safety: `B41-S7-M36-M39-A01` adds current local/static evidence for persistent anchors, labelled offline search/filter controls, detail-panel links, progressive diagnostics, static visual QA gates, white-page regression blockers and offline/privacy/accessibility contracts. Evidence ref is `docs/superpowers/specs/batch41-s7-m36-m39-cockpit-ux-safety-summary.json`. The eval value is that the primary first-run artifact is no longer only structurally valid: it now exposes a testable usability and safety contract. It does not prove browser screenshots, runtime interaction, console/network cleanliness, WCAG conformance, Cosmos.gl runtime execution, Neural_Flow acceptance, release readiness or target apply safety.
- Batch 41 S7 M40 Neural_Flow acceptance: `B41-S7-M40-A01` records owner-approved M40 execution for the Neural_Flow cockpit artifact. Evidence refs are `docs/superpowers/specs/batch41-s7-m40-neural-flow-acceptance-summary.json`, `docs/superpowers/specs/batch41-s7-m40-neural-flow-stage/` and `output/playwright/b41-s7-m40/playwright-runtime-proof.json`. The eval value is that the cockpit is now browser-visible, navigable, labelled, offline, and captures desktop/mobile screenshots, static runtime interaction, clean console/network and WCAG-oriented browser checks. It is not a WCAG certification, and it does not prove Cosmos.gl runtime/WebGL execution because the artifact remains script-free with no vendored Cosmos.gl runtime asset and uses SVG/table fallback.
- Batch 41 S8 architecture-dossier redesign: `B41-S8-M41..M47` was opened after owner review rejected the current M40 HTML as still too text-file-like, insufficiently designed and missing project architecture diagrams. `B41-S8-M41` is implemented as design-contract-only through `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-artifact.txt` and `docs/superpowers/specs/batch41-s8-m41-html-redesign-design-summary.json`. `B41-S8-M42` adds the first static architecture diagram layer with seven diagrams, raw Mermaid fallback, source/trust labels, no Mermaid runtime dependency and desktop/mobile Playwright proof in `output/playwright/b41-s8-m42/playwright-diagram-proof.json`. `B41-S8-M43` adds the architecture-dossier shell with first-viewport artifact identity, target context, next route, architecture signal, proof strip and desktop/mobile Playwright proof in `output/playwright/b41-s8-m43/playwright-shell-proof.json`. `B41-S8-M44` adds visible supported-claim, unsupported-claim, blocker, decision, owner/Codex action, risk, future-gate, proof-ref and source-blueprint surfaces with desktop/mobile Playwright proof in `output/playwright/b41-s8-m44/playwright-evidence-decision-proof.json`. `B41-S8-M45` adds explicit Graphology/Cosmos.gl static-vs-runtime boundary labels, runtime blocker, selected-node UX and fallback explanation with desktop/mobile Playwright proof in `output/playwright/b41-s8-m45/playwright-graph-runtime-proof.json`; canvas/WebGL runtime is absent and recorded as `runtime_webgl_blocked`, not as a passed runtime. `B41-S8-M46` adds desktop/mobile visual, interaction and accessibility-oriented Playwright evidence in `output/playwright/b41-s8-m46/playwright-visual-a11y-proof.json`; this is not axe/full WCAG certification and records that gap explicitly. `B41-S8-M47` regenerates the Neural_Flow staged artifact with before/after evidence in `docs/superpowers/specs/batch41-s8-m47-neural-flow-before-after-summary.json`, stage output under `docs/superpowers/specs/batch41-s8-m47-neural-flow-stage/` and proof in `output/playwright/b41-s8-m47/playwright-neural-flow-before-after-proof.json`; target mutation is false and owner final visual acceptance remains pending screenshot review. This route still must not claim release readiness, target apply safety, Cosmos.gl runtime/WebGL execution, WCAG certification, provider/API quality, installed plugin-cache readiness or source-read semantic completeness without separate current evidence.
- Batch 42 instruction/tool-use compliance is planned only in `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`. Future eval value must come from Product-Agent OS source/cache/session exposure checks, official OpenAI/Codex source status, implicit-invocation policy validation, runtime route fixtures for instruction/tool-use compliance prompts, transcript/behavioral evals for `self-learning-loop`, system-file hygiene triage and fresh-session proof. Planning matrix presence is not eval evidence and cannot support a fixed-auto-engagement claim.
- Batch 44 Self-Learning Loop S1-S5 evidence is local/schema/fixture/staged evidence only: state/trigger UX, manual runner/progress, feedback/preferences, metrics/evals and candidate/safety packets are source-owned by their `docs/superpowers/specs/batch44-self-learning-loop-*` summaries. They do not prove active schedule, hidden session ingestion, provider calls, target mutation, git/release/deploy/publish, external writes or auto-apply.
- B44 Self-Learning Loop S6 evidence is docs/contracts/closure evidence only: `docs/superpowers/specs/batch44-self-learning-loop-docs-contracts-closure-summary.json` records `B44-SLL-M15-M16-A01`, `self_learning_docs_contracts_closure_v1`, docs/source-registry sync and candidate-only automation promotion. Eval claims remain bounded: candidate-only automation promotion requires three manual successful runs, owner approval, rollback/disable path, false-positive audit, flake replay and cost check before activation; no real session import, hidden telemetry, raw transcript, live eval/provider/model call, target mutation, active automation, git/release/deploy/publish, external write or auto-apply was performed.
- B44 Self-Learning Loop S7 evidence is approved staged manual-pilot evidence only: `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json` records `B44-S7-SELF-LEARNING-MANUAL-PILOT-A01`, staged state initializer, explicit `--state-file`, redacted feedback/metrics, review-only candidates, 8 eval cases, 9 failure classes and 6 HALO-style recommendations. Promptfoo and HALO were not run; no provider/model/API, browser, target, automation, git/release/deploy/publish, external write or auto-apply occurred.
- Batch 45 Professional Code Authoring S0-S5 is source-owned by the Batch 45 packets, especially `docs/superpowers/specs/batch45-professional-code-s5-learning-automation-summary.json`: `B45-PCA-M23` is candidate-only learning-loop evidence and `B45-PCA-M14` closes only through that source contract. No hook activation, active automation, runtime/provider/browser proof, target mutation, git/release/deploy/publish or real AI-agent behavior improvement is proven.
- Batch 45 manual pilot evidence is local code/test: `docs/superpowers/specs/batch45-manual-pilot-6-code-tasks-summary.json` + `.codex/product-agent-os/b45-manual-pilot/coding-standard-checklists.md`; 6 code tasks, no scoped false positives, promotion not_made.
- Batch 45 S6 has M24 audit/tuning, M25 local advisory wiring, M26 approved live no-go eval and M27 promotion decision evidence in `docs/superpowers/specs/batch45-comment-sufficiency-false-positive-audit.json`, `docs/superpowers/specs/batch45-comment-sufficiency-tuning-comparison.json`, `docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json`, `docs/superpowers/specs/batch45-agent-behavior-eval-results.json` and `docs/superpowers/specs/batch45-comment-policy-promotion-decision.json`. M26 result: baseline `4.22`, treatment `3.88`, 15/16 completed, warnings `29 -> 15`, reviewer `no_go`. M27 decision: `keep_advisory_only_no_go_for_blocker_or_ci`. Eval claims are `advisory_validator_implemented`, `local_advisory_wiring_runtime_enabled`, `ci_wiring_not_performed`, `blocker_enforcement_not_performed`, `real_ai_agent_behavior_improvement_unproven_after_live_eval` and `promotion_no_go_keep_advisory_only`.
- Batch 45 S7 M28-M35 is source-owned by `research/b45-real-project-scenarios/` and the `batch45-real-project-*` JSON packets. M35 keeps advisory-only/no-go after M27/M34; treatment v2 is source-only future work, runtime/browser pilot is approval-required and CI/blocker promotion is rejected. `B45-PCA-M37-A01` adds local hook/validator hardening and docs/control-plane sync without changing the no-go/advisory-only ceiling or proving target/runtime/browser/provider/database/git/release/deploy/automation behavior.
- B45 Q4+: T01-T03 `14 -> 0`; T05/T12 no-go; T14 `gpt-5.5` 16/16 +3.27%, reviewer=0; T15 no promo; T17 frozen metadata-only held-out corpus manifest; T18 eval design/strict schema, no run; T19 cost/timeout/raw-temp-only retention policy, no run; T20 exact approval packet, owner_confirmed=false and no run. Src: `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet.json`.
- Agent lifecycle and control-plane sync: current local agents and packaged Product-Agent OS templates now route Task Brief / Completion Brief through `.codex/config.toml` `[product_agent_os.lifecycle_contract]` plus `[workflows]`; the eval contract fails duplicated lifecycle prose, missing config route, missing visible briefs, or closing a state-changing task without control-plane sync.
- Project-local lifecycle hooks: `product_agent_os_LIFECYCLE-HOOKS-A01` installs active `.codex/hooks.json`, keeps scripts and the Product-Agent OS policy mirror under `.codex/hooks/`, and ties the `PreToolUse` marker guard to `.codex/product-agent-os/lifecycle-state.json`; hook output is reminder/evidence context only, not proof of completion. Codex trust review or a fresh-session hook execution remains unsupported until manually confirmed.
- Track 11 G1.1 docs-toolchain system-file sync is current through `documentation_refresh_G1_1-SYSTEM-FILES-A01`, `DOC-M34` contract-only folder policy is current through `documentation_refresh_G1_1-DOC-M34-A01`, `DOC-M35` project-local MkDocs runtime install is current through `documentation_refresh_G1_1-DOC-M35-INSTALL-A01`, `DOC-M36` project-local Node docs tooling install is current through `documentation_refresh_G1_1-DOC-M36-NODE-A01`, `DOC-M37` local Vale language-guard install is current through `documentation_refresh_G1_1-DOC-M37-VALE-A01`, `DOC-M38` local lychee/gitleaks install is current through `documentation_refresh_G1_1-DOC-M38-LINK-SECRET-A01`, `DOC-M39` local Mermaid vendor install is current through `documentation_refresh_G1_1-DOC-M39-MERMAID-A01`, `DOC-M40` dependency audit/SBOM governance is current through `documentation_refresh_G1_1-DOC-M40-AUDIT-SBOM-A01`, and `DOC-M41` deferred platform trigger governance is current through `documentation_refresh_G1_1-DOC-M41-DEFERRED-PLATFORMS-A01`: root control-plane files route `.venv-docs/`, `.docs-tools/node/`, `.docs-tools/bin/`, `.docs-tools/vale/`, `.docs-tools/link-secret/`, `.docs-tools/reports/` and `docs/assets/javascripts/vendor/` as project-local tooling targets; `.gitignore` and `.docs-tools/README.md` define ignored paths, allowed checked-in content, forbidden content and approval boundaries; `tools/docs_install.ps1 -Install -AllowNetwork` installed `mkdocs==1.6.1`, `mkdocs-material==9.5.50` and `mkdocs-static-i18n==1.2.3`; strict MkDocs smoke passed under `.docs-tools/reports/mkdocs-strict-smoke-2026-06-21`; `tools/docs_node_install.ps1 -Install -AllowNetwork` installed `markdownlint-cli2==0.22.1`, `prettier==3.8.4` and `@redocly/cli==2.34.0`; `tools/docs_vale_install.ps1 -Install -AllowNetwork` installed Vale `3.15.1` and recorded `.docs-tools/bin/vale.sha256`; `tools/docs_link_secret_install.ps1 -Install -AllowNetwork` installed lychee `0.24.2` and gitleaks `8.30.0` with checksum files; `tools/docs_mermaid_install.ps1 -Install -AllowNetwork -Force` vendored Mermaid `10.9.6` with MIT license, package metadata and checksum records; `tools/docs_dependency_audit.ps1` records local Python inventory, `pip check`, Node CycloneDX SBOM generation and local checksum consistency; approved `npm audit --audit-level=high` reports 3 moderate Node findings and 0 high/critical findings; Docusaurus, Storybook and Structurizr DSL remain deferred until concrete trigger evidence and owner approval exist. This is install, smoke, local inventory, bounded Node advisory and deferred-trigger evidence only: broad docs lint/format, broad Vale enforcement, external URL crawling, broad link/secret scans, raw report retention, browser Mermaid rendering, Redocly enforcement, Python vulnerability audit, complete repository SBOM, dependency remediation, deferred platform install/runtime proof, browser proof and root `site` freshness remain unclaimed until their matching checks run.
- Track 11 G2 first-run cockpit/artifact docs are current through `documentation_refresh_G2-A01`: source Markdown, EN counterparts, MkDocs nav, registry markers and docs tests route the new cockpit page and artifact atlas, while `DOC_M25_PENDING_SITE_PAGES` keeps root `site`/search/sitemap freshness unclaimed until final `DOC-M25`.
- Track 11 G3 diagram atlas source/nav docs are current through `documentation_refresh_G3-A01`: source Markdown, EN counterparts, MkDocs nav, registry markers and docs tests route the new source/generated, first-run cockpit, evidence/risk, skill exposure and Architecture Intelligence diagrams, while `DOC_M25_PENDING_SITE_PAGES` keeps root `site`/search/sitemap freshness unclaimed until final `DOC-M25`; browser proof remains approval_required and Structurizr DSL remains deferred.
- Track 11 G4 operator-flow source/nav docs are current through `documentation_refresh_G4-A01`: source Markdown, EN counterparts, MkDocs nav, registry markers and docs tests route instruction/tool-use compliance, operator command matrix, guided questions, methodology integration and source/cache/session state pages, while `DOC_M25_PENDING_SITE_PAGES` keeps root `site`/search/sitemap freshness unclaimed until final `DOC-M25`; auto-engagement/cache/global config/fresh-session proof remains unsupported.
- Track 11 G5 evidence-quality/source-nav docs are current through `documentation_refresh_G5-A01`: source Markdown, EN counterparts, MkDocs nav, registry markers and docs tests route generated artifact UX, graph intelligence, privacy/supply-chain/report-retention, local HTML interaction and residual follow-up/site freshness pages, while `DOC_M25_PENDING_SITE_PAGES` keeps root `site`/search/sitemap freshness unclaimed until final `DOC-M25`; browser proof, broad scans, dependency remediation and raw report retention remain approval_required.
- Track 11 DOC-M25 generated site freshness is current through `documentation_refresh_DOC-M25-A01`: root `site`, search and sitemap freshness current for the former `DOC_M25_PENDING_SITE_PAGES` set after the owner-approved MkDocs build; browser proof, visual/runtime evidence, broad scans, remediation, raw report retention, publication, release, deploy and git actions remain outside this eval result.
- Root `AGENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` are compact control-plane files. They preserve current routing and safety boundaries, not every historical batch result.
- Historical Batch 34E full-site i18n parity and Batch 35 real-testing evidence is source-owned by Track 10 backlog, source registry and dedicated source packets.

## Active Eval Routes

| Change type | Required eval route |
| --- | --- |
| Docs, source registry, control-plane or docs tests | `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`, `python tools\check_docs.py`, `git diff --check` |
| Track 11 G1.1 docs-toolchain implementation | Control-plane route checks first; then approved project-local install smoke for `.venv-docs/`, `.docs-tools/node/`, `.docs-tools/bin/`, report redaction, optional vendored diagram asset provenance, strict MkDocs and audit/SBOM checks where enabled |
| Track 11 G2 source/nav docs | Docs route plus strict MkDocs smoke to `.docs-tools/reports`; root `site` freshness remains a `DOC-M25` eval gate |
| Track 11 G3 diagram atlas source/nav docs | Docs route plus strict MkDocs smoke to `.docs-tools/reports`; root `site` freshness remains a `DOC-M25` eval gate and browser proof remains approval_required |
| Track 11 G4 operator-flow source/nav docs | Docs route plus strict MkDocs smoke to `.docs-tools/reports`; root `site` freshness remains a `DOC-M25` eval gate and auto-engagement/cache/global config/fresh-session proof remains unsupported |
| Track 11 G5 evidence-quality/source-nav docs | Docs route plus strict MkDocs smoke to `.docs-tools/reports`; root `site` freshness remains a `DOC-M25` eval gate and browser proof, broad scans, remediation and raw report retention remain approval_required |
| Track 11 DOC-M25 generated site freshness | Root `site`, search and sitemap freshness current through `documentation_refresh_DOC-M25-A01`; browser proof, broad scans, remediation, raw report retention and publication/release evidence remain separate approval gates |
| MkDocs navigation, Mermaid, localization, search/sitemap or generated `site/` evidence | Docs route plus strict MkDocs build |
| Plugin scripts, templates, lifecycle skills, runtime behavior or CLI contracts | Focused tests, full unittest, fixture eval, transcript eval, Codex compatibility, docs check and diff hygiene as routed by `TEST.md` |
| Self-Learning Loop state, manual pilot, Promptfoo/HALO export or repair contract | `python -m unittest tests.product_agent_os.test_self_learning_extensions -v`, `python -m unittest tests.product_agent_os.test_self_learning_state -v`, staged initializer/runner/export commands, docs checks and diff hygiene |
| Product-Agent OS pilot runner, result collector, dashboard rollup or Batch 39 pilot/hardening matrix | `prod_test.md` attempt/failure/fix/retest ledger review, focused schema/collector/dashboard/route tests, redaction and no-mutation proof, CLI contract checks, graph extension gates, security/privacy/compliance/supply-chain checks, template/workflow and skill/subagent contract checks, fixture eval, transcript eval, docs check and diff hygiene; full plugin verification when runtime/scripts/templates change |
| Batch 45 Professional Code Authoring | Focused B45, behavioral, discovery/status/dashboard/template/fixture, self-learning, automation-policy, docs/source-link, manual-pilot ledger, docs check, strict MkDocs smoke for nav-sensitive changes and diff hygiene; generated views/candidates stay orientation-only/candidate-only until approved runtime or activation evidence exists |
| Batch 45 review remediation local hook/validator hardening and docs/control-plane sync | `python -m unittest tests.product_agent_os.test_comment_sufficiency tests.product_agent_os.test_lifecycle_hooks -v`, `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`, `python tools\check_docs.py`, scoped `git diff --check`; no runtime/browser/provider/target/git/release/deploy/automation claims |
| Batch 45 repeat quality/refactor retest Q0-Q4/post-Q4 | Focused coding-standards, comment-sufficiency/lifecycle, docs check and diff hygiene; protocol/static replay/planning only, no behavior/runtime/provider/target/CI/release/automation proof |
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
- G1.1 planned folders, package manifests, Vale rules, lychee/gitleaks fixture smokes, Mermaid vendor files, DOC-M40 inventory/SBOM governance, DOC-M41 deferred platform trigger records or tool names as proof that dependencies are vulnerability-free, fully remediated, broadly enforced, secret-free, externally link-healthy, browser-rendered, platform-ready or that `site/` was rebuilt.
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
```
