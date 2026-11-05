# PLAN.md

## Current ordinary route integration — 2026-11-05

`PAOS-ORD-01-06-2026-11-05`: implemented_locally_verified; final integrated verification passed. Scope is only PAOS-ORD-01 through PAOS-ORD-06 in [the owning plan](research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md). The opt-in task context connects existing T26/T27 selectors to the public contract CLI, scoped infrastructure proposals and compact authoring. T23-T29 are reused unchanged; PAOS-GAP and T30-T34 remain unstarted. No publication, target apply, hook/cache activation or provider calls. Rollback only the ORD-owned changes against the recorded pre-slice baseline; preserve earlier docs/site work.

## Current documentation refresh — 2026-11-05

`PAOS-SITE-DOCS-REFRESH-2026-11-05`: user-authorized docs/site maintenance from F01-F18 audit. Scope: bilingual guides, registry, archive labels and local site rebuild/links/Mermaid checks; no implementation or publication. Plan: `.docs-tools/reports/site-docs-refresh-plan-2026-11-05.md`; evidence: `docs/superpowers/specs/site-docs-refresh-2026-11-05.json`. Completed: docs_static_verified. One writer; 100 docs tests, strict build, 220 routes, links/anchors/search and 93 Mermaid renders passed. No implementation changes or publication.


<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Current lifecycle repair — 2026-11-03

`PAOS-LIFECYCLE-REPAIR-2026-11-03`: **implemented_locally_verified / verified_local_runtime**. The six repair findings are resolved; activation_pending=false, activation_status=verified_local_runtime for the tested desktop routes. Future definition changes require exact-hash trust review and a fresh negative probe.

Evidence: [task group](docs/superpowers/specs/gpt6-documentation-refresh-task-group.json), `lifecycle_parity.repair`; [plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md). The earlier failed activation below is historical, superseded by this bounded retest.

## Historical lifecycle activation check — 2026-11-03

`PAOS-LIFECYCLE-ACTIVATION-2026-11-03`: verification completed with findings; **activation_failed**. Next: diagnose ACT-F1 host trust/matcher/response handling without bypass; reconcile ACT-F2 ledger format and ACT-F3..F6 source contradictions; then repeat the fresh large/ordinary and safe negative scenarios. Fixes require their own authorized slice; this task changed evidence only.

Evidence: [task group](docs/superpowers/specs/gpt6-documentation-refresh-task-group.json), `lifecycle_parity.activation_check`; [detailed plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md). No trust/permissions/models/provider/Git changes.

## Historical lifecycle parity — 2026-11-03

`PAOS-TRADE-LIFECYCLE-PARITY-2026-11-03`: `implemented_locally_verified / activation_failed`. Sequence: read-only Trade baseline -> RED/GREEN regressions -> active/staged contracts -> integrated checks -> status sync. Detailed task and rollback live in the existing November plan pair; fresh-session trust/activation is a separate gate.

Evidence owner: [task group](docs/superpowers/specs/gpt6-documentation-refresh-task-group.json), `lifecycle_parity`; detail: [plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md).

## Current contract alignment — 2026-11-03

`PAOS-CONTRACT-MODEL-ALIGNMENT-2026-11-03`: `implemented_locally_verified / behavioral_promotion_pending`. Parent permissions and MCP inheritance aligned; 23 active/staged profiles pinned to GPT-6.1 Sol/Terra with preserved effort; inherited skills moved to parent; validators and renderer reject unsupported contracts; lifecycle validator follows the explicit current plan.

Current verification: Ran 1247 tests in 611.387s; OK (skipped=1); fixture/transcript eval, compatibility, 15 active agents, both hook validators, RU/EN task matrices, state consistency, docs checker and diff check exit 0. Detailed evidence, source receipts and rollback: [plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md) and [task group](docs/superpowers/specs/gpt6-documentation-refresh-task-group.json).

Fresh-session effective permissions/MCP/model availability and quality/cost/latency comparison remain unverified. No provider calls, browser, hook activation, target mutation, Git publication or root site update.

Local PERM/MCP/BASELINE repair is complete. MODEL pins are switched, promotion pending. OPEN-RUNTIME remains separately scoped; Batch 45 T30 remains next in its existing queue.

## Purpose

`PLAN.md` is the compact sequencing and rollback layer for current Product-Agent OS work. It points to source-owned plans, backlogs, evidence packets and [current control-plane state](docs/product-agent-os/control-plane-current-state.md) for detailed history.

## Documentation refresh queue — 2026-11-03

`PAOS-DOCS-REFRESH-2026-11-03`: documentation_implemented_locally_verified (20/20). The [detailed RU/EN plan](docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md) owns all 20 task blocks; [task-group JSON](docs/superpowers/specs/gpt6-documentation-refresh-task-group.json) owns machine status. Completed E0 baseline -> E1 controls/instructions -> E2 models -> E3 migration/evals -> E4 API/runtime/hooks -> E5 parity/navigation -> E6 checks and status. No model/runtime promotion. The subsequent authorized contract-alignment task owns PERM/MCP/MODEL/BASELINE repair; runtime activation and new API paths remain separate. Batch 45 T30 remains the next implementation dependency; this documentation queue does not execute T30-T34. Rollback only this documentation slice, preserving historical evidence and unrelated dirty changes.

## Current Planning Contract

- Work in focused slices with explicit scope, acceptance criteria, risks, rollback and verification gates.
- Use Product-Agent OS skills for requirements, implementation planning, test/eval design, docs maintenance, risk review and completion-skeptic loops when the task matches them.
- Keep historical batch matrices in source-owned files, not in this root plan.
- Use `overflow_refactor_required` when a root control-plane file is near budget: move cold detail to the owning docs/spec/backlog first, then update the compact root pointer.
- Do not create/switch branches, stage, commit, push, open PRs, mutate target workspaces, run browser automation, call providers/live APIs, publish, deploy or create automations without exact approval for that action.
- Preserve unrelated dirty work and record only the evidence needed for current handoff.

## Current State

| Workstream | State | Planning impact |
| --- | --- | --- |
| Product identity and agent contract | Root `AGENTS.md` now defines this repository as the implementation, verification and evidence workspace for Product-Agent OS, separates the Russian knowledge base as a supporting surface, records the current local/manual claim ceiling, and distinguishes active `.codex/agents` roles from target-workspace agent templates. | Keep volatile route and batch evidence in the owning plans, packets and `RUNLOG.md`; do not turn product mission into a broad production-readiness claim. |
| Batch 35 / Batch 38 | `T10-LIVE-M41` is closed as `owner_closed_no_op_git_release_pr`; `B38-S2` cache refresh evidence is current and historical `blocked_pending_explicit_cache_mutation_approval` remains preserved in source history. | Future git writes need fresh preflight and exact approval; no remaining B38 cache refresh action is planned. |
| Batch 39 | Closed for manual owner-feedback testing only; release/distribution is `no_go`, owner feedback is `conditional_go`, runtime/browser pilot is `approval_required`. | Use `prod_test.md` and B39 S5 packets; do not claim release/runtime/browser readiness. |
| Batch 41 | First-run cockpit S9 modernization and Neural_Flow staged comparison are source-owned generated-artifact evidence. | Next decision is owner review or a separately approved browser/Cosmos.gl/WebGL/target-apply proof slice. |
| Batch 42 | Instruction/tool-use compliance matrix is planned-only. | Owner must choose read-only audit, source implementation, cache/global policy path or staged combination before execution. |
| Batch 44 | Self-Learning Loop S0-S7 are local/staged/manual evidence. | Continue with `B44-S8` closure/promotion decision only after owner review; no active automation or auto-apply. |
| Batch 45 | Professional Code Authoring remains advisory-only/no-go. T21 aborted on strict schema validation with `valid_pair_count=0`, `invalid_pair_count=8`, reviewer `0` and repo raw retention `0`; `B45-POSTQ4-T22-A02` remains no-go. A04 locally implements/focused-verifies T23/T24; `B45-CQRR-A05` locally implements/focused-verifies T25-T27: compact contract, project-native `present_unverified` stack/tool selector and risk-selected quality strategy; final T25-T27 combined route is 54 OK with independent local reviewer and completion-skeptic `GO_local_code_gate`. | A06 subsequently completed T28/T29 locally; current next dependency is T30. T30-T34 remain unstarted; T34 is exact-approval-only. The earlier A04/A05 evidence is historical. A04/A05 are no CLI/live/provider/external-reviewer/promotion proof and do not reverse T22 no-go. |
| Track 11 DOC-M25 | Root `site`, search and sitemap freshness are source-owned by the DOC-M25 packet. | Browser proof, broad scans, remediation, raw retention, publication, release/deploy and git actions remain separate. |
| GPT-5.6 system-file remediation | `GPT56-R1-R6-REMEDIATION-2026-08-05` is locally implemented and verified: active/generated config use one `workspace-write` permission model, generic defaults are Terra/medium, skill write authority and Docs MCP routing are explicit, semantic validation is active, and durable prompts are compact/phase-neutral. Plan: `docs/superpowers/plans/2026-08-05-gpt56-r1-r6-remediation.md`; audit: `research/2026-07-23-codex-gpt-5p6-system-files-audit.md`. | Fresh-session MCP/`SessionStart` activation and same-effort/one-lower-effort behavioral comparison remain separate gates before any quality, cost, latency or promotion claim. |
| Lifecycle/control-plane sync | `B45-S9-H01` locally hardens the config-routed lifecycle: read-only `PreToolUse` takes a no-workspace fast path, comment advisory inspects current patch paths, hook timeouts are bounded to 5 seconds, and `Completion Brief` is a terminal-final contract after checks/sync with one bounded `Stop` correction only when the lifecycle marker is ready. | Before closing state-changing work, finish checks and control-plane sync, set `ready_for_completion_brief`, then emit one terminal `Completion Brief` with no later tool call. Hook hash trust review and fresh-session activation proof remain separate user actions. |

## Next Implementation Queue

| Slice | Next decision | Approval boundary | Source pointer |
| --- | --- | --- | --- |
| `B39-owner-feedback` | Run/review manual owner-feedback scenarios. | Runtime/browser pilot remains separate approval. | `prod_test.md`; `docs/superpowers/specs/batch39-s5-owner-feedback-test-plan.json`. |
| `B44-S8` | Review S7 manual pilot and decide promotion/no-go. | No scheduler, hooks, provider/model, target mutation, git/release/deploy/publish, external write or auto-apply. | `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`. |
| `B45-S8` | Promotion-grade eval task group is source-owned through strict-schema abort evidence: T18 eval design/strict schema, T19 cost/timeout/raw-temp-only retention, T20 A03 consumed cost-waived approval, T21 invalid-schema result and T22 A02 blocked/no-go decision. | No provider/model/reviewer call, runtime/browser, target, CI/blocker, git, release/deploy or automation unless strict output/schema handling is fixed or normalized and a new exact approval authorizes a rerun; T21 must produce a valid result before T22 reviewer gate can run. | `docs/superpowers/specs/batch45-postq4-t16-t22-promotion-grade-eval-task-group.json`; `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json`; `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json`; `docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json`; `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet.json`; `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json`; `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-cost-waived.json`; `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json`; `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json`; `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-cost-unknown.json`; `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-results.json`; `docs/superpowers/specs/batch45-postq4-t22-promotion-grade-decision-packet.json`. |
| `B45-S9` | A04-A06 locally implement/focused-verify T23-T29. T28 repair replaced the unaccepted 196-record manifest/legacy T18-T22 block with semantic cases (families 34, exceptions 3, combined test LOC 5658); T29 adds deterministic promotion evidence with self-score diagnostic-only. Next dependency is T30. | Keep single-writer/two-repair budgets. T30-T33 remain local gates; T34 is exact-approval-required. No provider/model/reviewer, runtime/browser, target, Git, release/deploy or automation action is authorized. | `docs/superpowers/plans/2026-08-17-product-agent-os-loop-remediation.md`; `docs/superpowers/plans/2026-08-14-batch45-s9-c-test-metric-repair.md`; `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. |
| `Track11-after-DOC-M25` | Maintain source docs and generated-site boundary. | Browser proof, broad scans, dependency remediation, publication and release remain separate. | `docs/superpowers/specs/documentation-refresh-doc-m25-site-freshness-summary.json`. |
| `control-plane-overflow` | Keep `PLAN.md`, `RUNLOG.md`, `TEST.md`, `EVALS.md` under compact budgets after each task. | Size pressure is not permission to skip updates. | `docs/product-agent-os/control-plane-current-state.md`; `.codex/workflows/control-plane-sync.md`. |

## Batch 39 Ledger Rule

- `prod_test.md` is the required attempt/failure/fix/retest ledger for Batch 39.
- Real-project target evidence defaults to `read_only_target_discovery`; any target write, browser automation, provider/API, database, git, release, external write or target mutation action requires separate exact approval.
- Generated dashboards, reports and project graphs are orientation evidence unless backed by source artifacts, current command/runtime evidence or explicit accepted gaps.

## Source Planning Artifacts

| Artifact | Role |
| --- | --- |
| `REQUIREMENTS.md` | Current scope, acceptance and constraints. |
| `TEST.md` | Current verification commands and escalation rules. |
| `EVALS.md` | Current eval rubrics, thresholds and subjective gates. |
| `RUNLOG.md` | Current-cycle handoff and residual risks. |
| `AGENTS.md` | Durable operating rules and current operating status. |
| `docs/product-agent-os/control-plane-current-state.md` | Site-facing current state, source matrix and root-file compaction owner artifact. |
| `docs/sources/product-agent-os-track-8-detailed-backlog.md` | Track 8 detailed scenario/methodology history. |
| `docs/sources/product-agent-os-track-9-backlog.md` | Source-owned Track 9 methodology and verification history. |
| `docs/sources/product-agent-os-track-10-backlog.md` | Source-owned Track 10, Batch 35, Batch 38, Batch 39, Batch 40, Batch 41 and Batch 42 history. |
| `docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md` | Active Track 11 docs architecture, Batch 44 and Batch 45 matrices. |
| `docs/sources/registry.md` and `docs/sources/registry.en.md` | Claim/source registry. |
| `docs/sources/product-agent-os-batch35-approval-packet-draft.md` | Batch 35 approval and execution packet. |
| `docs/superpowers/specs/*.json` | Source-owned evidence packets for current batch details. |
| `prod_test.md` | Batch 39 production test ledger. |
| `.codex/workflows/control-plane-sync.md` | Mandatory before-completion control-plane sync checklist. |

Evidence ownership stays source-routed; `git diff --check` remains part of docs/control-plane verification.

## Compatibility Anchors

These compact anchors support discovery and tests; they are not execution evidence by themselves:

- B37 task-matrix anchors: `B37-S1`, `B37-S2`, `B37-S3`, `B37-S4`, `B37-S5`, `T10-PLAN-M01..M03`, `T10-PLAN-M04..M05`, `T10-PLAN-M18`, `task-matrix contract`, `task-matrix-plan.md`.
- Batch 35/38 anchors: `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr`, `B38-S1`, `B38-S2`, `B38-S3`, `B38-S4`, `B38-PILOT-NF01`, `blocked_pending_explicit_cache_mutation_approval`.
- Batch 39 anchors: `B39-S1`, `B39-S2`, `B39-S3`, `B39-S4`, `B39-S5`, `B39-TEST-M21-A01..A03`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`, `B39-S4 hardening`.
- Batch 40/41/42 anchors: `B40-S5`, `manual_only`, `not_promoted`, `B41-S1..S9`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `B41-S8-M41..M47`, `B42-S1..S5`, `planned_task_matrix_added`.
- Track 11/B44/B45 anchors: `DOC-M25`, `B44-S0` through `B44-S8`, `B45-PCA-M24..M27`, `B45-PCA-M37-A01`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`, `B45-CQRR-A01`, `B45-CQRR-A02`, `B45-CQRR-A03`, `B45-CQRR-T23..T34`.

## Rollback

- Revert only files touched by the current slice.
- Preserve unrelated dirty changes.
- Do not use destructive git operations without explicit approval.
- For target-workspace pilots, rollback must be defined before mutation and must name owner, files, commands and stop condition.

## Verification

For docs/control-plane changes, run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Run strict MkDocs only when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

<!-- product-agent-os:end plan -->
