# PLAN.md

<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-06-07

## Purpose

`PLAN.md` is the compact sequencing and rollback layer for the current Product-Agent OS work. It should not store the full historical implementation ledger.

Evidence ownership is distributed as follows:

| PLAN information class | Owning file now |
| --- | --- |
| Current scope, acceptance and constraints | `REQUIREMENTS.md` |
| Current verification commands and escalation rules | `TEST.md` |
| Current eval rubrics, thresholds and subjective gates | `EVALS.md` |
| Current-cycle handoff and residual risks | `RUNLOG.md` |
| Durable operating rules and current operating status | `AGENTS.md` |
| Track 8 detailed scenario/methodology history | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 detailed methodology and verification history | `docs/sources/product-agent-os-track-9-backlog.md` |
| Track 10 detailed execution and verification history | `docs/sources/product-agent-os-track-10-backlog.md` |
| Source-backed claim registry | `docs/sources/registry.md` |
| Batch 35 approval and execution packet | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Current State

- Track 9 methodology intelligence, Track 10 Task 23, Task 24, Task 25 and Task 26 through `done_through_m40` are implemented or closed as recorded in the source registry and Track 9/10 backlogs.
- Task 26 Batch 35 is complete through `T10-LIVE-M40` under `batch35_approval_bound_real_testing_execution`.
- `T10-LIVE-M41` reached `explicit_git_release_pr_action` preflight and remains `blocked_pending_explicit_git_release_fields`.
- Separately approved maintenance: B37-S1 implements `T10-PLAN-M01..M03` and `T10-PLAN-M18` for the Product-Agent OS task-matrix contract, lifecycle/timestamp policy, `task-matrix-plan.md` placement policy and lightweight exception rule. B37-S2 implements `T10-PLAN-M04..M05` and `T10-PLAN-M17` for the checked-in `task-matrix-plan.md` template, renderer registration and packaging-surface evidence with `renderer_file_count: 195`.
- Root `AGENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` follow the compact-control-plane model: current routing and safety boundaries stay in root files, detailed history stays in source-owned backlogs and registry entries.
- Existing dirty `README.md` is unrelated to this planning maintenance unless the owner explicitly scopes it in.

## Current Planning Contract

- Next executable product action: none until the owner supplies the missing `T10-LIVE-M41` git release/PR fields or explicitly defers M41. The approved B37-S1/B37-S2 planning maintenance is not a live/runtime/git action and does not close M41.
- Required fields for M41: release branch or push target, commit message, PR base branch, PR title and intent, and explicit branch creation/current-branch push policy.
- Do not create or switch branches, stage files, commit, push or open a PR without explicit approval.
- Do not start Task 27/28 planning from Batch 35 while M41 is unresolved or explicitly deferred.
- Do not launch live servers, run browser automation, call providers/live external model/API endpoints or mutate canonical graph sources without the exact approved action packet.
- B37-S1 task-matrix contract boundaries: `planned` uses `pending_execution_timestamp`; `implemented` requires actual `DD-MM-YYYY HH:mm`, touched files/work locations and current verification evidence; detailed task blocks are the future validator target and summary tables are indexes only; lightweight exceptions require `reason`, `reduced_evidence_path` and `residual_risk`.
- B37-S2 template/renderer boundaries: checked-in source is `plugins/product-agent-os/assets/templates/artifact-templates/task-matrix-plan.md`; staged target is `.codex/artifact-templates/task-matrix-plan.md`; renderer key is `artifact-task-matrix-plan`; plugin cache remains stale until an explicit publication/cache refresh action is approved; no plugin publication, `.codex-plugin/plugin.json` mutation, live automation, provider/live external model/API call or git stage/commit/push/PR is authorized.

## Next Implementation Queue

| Order | Item | Status | Owner action required |
| --- | --- | --- | --- |
| 1 | B37-S1 `T10-PLAN-M01..M03`, `T10-PLAN-M18` task-matrix contract | implemented in current maintenance slice | No owner action. |
| 2 | B37-S2 `T10-PLAN-M04..M05`, `T10-PLAN-M17` template, renderer and packaging surface | implemented in current maintenance slice | No owner action unless the owner wants B37-S3 validator/eval work. |
| 3 | `T10-LIVE-M41` explicit git release/PR action | `blocked_pending_explicit_git_release_fields` | Provide release branch or push target, commit message, PR base/title/body intent and explicit write approval. |
| 4 | Batch 35 closure decision | blocked by M41 | Either approve M41 details or explicitly defer M41 with residual risk. |
| 5 | Future Task 27/28 planning | not started | Start only after Batch 35 is closed or deliberately deferred. |

## Source Planning Artifacts

- Track 9 design: `docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md`.
- Track 9 implementation plan: `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Track 10 implementation plan: `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
- Track 9 backlog: `docs/sources/product-agent-os-track-9-backlog.md`.
- Track 10 backlog: `docs/sources/product-agent-os-track-10-backlog.md`.
- Batch 35 approval packet: `docs/sources/product-agent-os-batch35-approval-packet-draft.md`.

## Architecture Boundary

- Plugin implementation package: `plugins/product-agent-os/`.
- Operator and product docs: `docs/product-agent-os/`, `docs/product-agent/`, `docs/runtime/`, `docs/agent-systems/`, `docs/playbooks/`.
- Evidence and registry docs: `docs/sources/`.
- Generated site output: `site/`, not source of truth.
- Root control-plane files: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`.

## Planning Rules

- Keep `PLAN.md` focused on active sequencing, ownership boundaries, source pointers and rollback.
- Put completed-slice, implementation-status and historical verification history in Track 8/9/10 backlogs and the source registry, not in root control-plane files.
- If a future docs contract starts requiring every historical marker in `PLAN.md`, update the contract and owning source docs together instead of growing `PLAN.md`.
- Preserve user-authored files and unrelated dirty changes.

## Verification For This Planning Maintenance

- Focused docs contract: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`.
- Documentation structure: `python tools\check_docs.py`.
- Diff hygiene: `git diff --check`.

## Rollback

- Revert only files touched by the current maintenance slice.
- Preserve evidence ownership notes in the Track 10 backlog and source registry.
- Do not use destructive git operations without explicit approval.
<!-- product-agent-os:end plan -->
