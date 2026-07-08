# PLAN.md

<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Purpose

`PLAN.md` is the compact sequencing and rollback layer for current Product-Agent OS work. It points to source-owned plans, backlogs, evidence packets and [current control-plane state](docs/product-agent-os/control-plane-current-state.md) for detailed history.

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
| Batch 35 / Batch 38 | `T10-LIVE-M41` is closed as `owner_closed_no_op_git_release_pr`; `B38-S2` cache refresh evidence is current and historical `blocked_pending_explicit_cache_mutation_approval` remains preserved in source history. | Future git writes need fresh preflight and exact approval; no remaining B38 cache refresh action is planned. |
| Batch 39 | Closed for manual owner-feedback testing only; release/distribution is `no_go`, owner feedback is `conditional_go`, runtime/browser pilot is `approval_required`. | Use `prod_test.md` and B39 S5 packets; do not claim release/runtime/browser readiness. |
| Batch 41 | First-run cockpit S9 modernization and Neural_Flow staged comparison are source-owned generated-artifact evidence. | Next decision is owner review or a separately approved browser/Cosmos.gl/WebGL/target-apply proof slice. |
| Batch 42 | Instruction/tool-use compliance matrix is planned-only. | Owner must choose read-only audit, source implementation, cache/global policy path or staged combination before execution. |
| Batch 44 | Self-Learning Loop S0-S7 are local/staged/manual evidence. | Continue with `B44-S8` closure/promotion decision only after owner review; no active automation or auto-apply. |
| Batch 45 | Professional Code Authoring remains advisory-only/no-go. T14 `gpt-5.5` rerun is a positive current-quality signal only: 16/16, `+3.27%`, reviewer `0`, below `>=20%`, not same-model comparable. T18 now defines the same-model promotion-grade comparison, strict schema, quarantine, scoring/reviewer rubric and result contract, but no run occurred. | Next route is `B45-S8` design-first: T19 cost/timeout/raw-temp-only retention, then exact approval before any baseline/treatment run. |
| Track 11 DOC-M25 | Root `site`, search and sitemap freshness are source-owned by the DOC-M25 packet. | Browser proof, broad scans, remediation, raw retention, publication, release/deploy and git actions remain separate. |
| Lifecycle/control-plane sync | Task Brief, lifecycle marker, control-plane sync and Completion Brief are config-routed. | Before closing state-changing Product-Agent OS work, update root files or record `not_applicable`, `handoff_required` or `overflow_refactor_required`. |

## Next Implementation Queue

| Slice | Next decision | Approval boundary | Source pointer |
| --- | --- | --- | --- |
| `B39-owner-feedback` | Run/review manual owner-feedback scenarios. | Runtime/browser pilot remains separate approval. | `prod_test.md`; `docs/superpowers/specs/batch39-s5-owner-feedback-test-plan.json`. |
| `B44-S8` | Review S7 manual pilot and decide promotion/no-go. | No scheduler, hooks, provider/model, target mutation, git/release/deploy/publish, external write or auto-apply. | `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`. |
| `B45-S8` | Implement the promotion-grade eval task group before any future run; T18 eval design and strict schema are now source-owned. | No provider/model/reviewer call, runtime/browser, target, CI/blocker, git, release/deploy or automation without exact approval. | `docs/superpowers/specs/batch45-postq4-t16-t22-promotion-grade-eval-task-group.json`; `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json`; `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json`. |
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
- Track 11/B44/B45 anchors: `DOC-M25`, `B44-S0` through `B44-S8`, `B45-PCA-M24..M27`, `B45-PCA-M37-A01`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`.

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
