# Control-Plane Sync

Project: {project_name}
Profile: {profile_name}

## Purpose

Assess documentation impact before closing every Product-Agent OS task. Only changed owned information requires a write; small or read-only tasks may record a concise no-change reason.

This is not an active hook or automation. It is a mandatory agent checklist inside the parent task before the applicable completion response; it does not require a full Completion Ledger for every task.

## Control-Plane Files

- `REQUIREMENTS.md`: current scope, users, constraints, acceptance criteria, assumptions, and non-goals.
- `PLAN.md`: current sequencing, queue, dependencies, rollback, and planning pointers.
- `TEST.md`: current verification commands, escalation rules, and latest maintenance evidence.
- `EVALS.md`: current eval rubrics, thresholds, subjective gates, unsupported-claim policy, and accepted-gap policy.
- `RUNLOG.md`: current-cycle decisions, latest completed slice, evidence summary, residual risks, and handoff state.
- `prod_test.md`: optional project-specific production-test ledger; update it only when the current task explicitly changes that evidence family.

## Process

1. Run this check after implementation and verification, before the Completion Ledger.
2. For each control-plane file, decide `update_required`, `not_applicable`, `handoff_required`, or `overflow_refactor_required`.
3. Update the file directly when the current task changed its owned information class and the file is in the task write scope.
4. Use `handoff_required` only when the file is relevant but belongs to another owner or is outside the current write scope. Do not use `handoff_required` merely because the file is near a size limit.
5. Use `overflow_refactor_required` when a required update would bloat a compact root file. First move cold history, detailed evidence, row banks, long matrices, or old cycle decisions to the owning source artifact, then shorten the root file to current pointers and apply the required update in the same slice when the file is in scope.
6. Preserve compactness: root files record current state, routing, gates, and pointers only; detailed history belongs in source-owned docs, specs, backlogs, product docs, generated artifacts, or the project ledger.
7. Treat `40 KB` as exactly `40 000 UTF-8 bytes` for active control-plane and navigation documents; warn at `32 000` bytes. A stricter project limit wins. Legacy character/50KiB budgets are superseded. A budget crossing is a compaction trigger requiring a lossless proposal, not permission to skip the update.
   Detailed task matrices under `docs/planning/` (including subfolders) are exempt from the default size trigger: preserve full cards/tables and do not split solely because of size. This is active detail, not history. Index/README and control-plane files keep their budgets; explicit per-file project limits and all content/link/security checks still apply.
8. Before shortening `RUNLOG.md` or any root control-plane file, route scope and constraints to requirements docs, sequencing and next actions to plan docs, verification commands and ownership to test docs, eval thresholds and claim ceilings to eval docs, detailed evidence to source-owned plans/specs/backlogs or the project ledger, and only current handoff/residual risk pointers to the root runlog.
9. Never treat generated dashboards, stale logs, or previous runs as current evidence.
   Before shortening, review exact-byte moves, source/destination hashes, retention reasons and recovery journal. Authorized apply must reject concurrent changes and verify preservation, links and sizes. Never summarize away original evidence. Recheck changed documents after the next update; this manual checklist creates no automation.
10. Do not activate hooks, automations, external writes, git actions, provider calls, browser automation, live servers, cache mutation, or target workspace mutation through this workflow.

## Update Triggers

- `REQUIREMENTS.md`: user goal, scope, acceptance criteria, assumptions, constraints, or non-goals changed.
- `PLAN.md`: task order, active batch status, dependency, rollback route, or next planned action changed.
- `TEST.md`: verification command, required check, escalation rule, or test ownership changed.
- `EVALS.md`: eval rubric, threshold, failure class, accepted-gap policy, or evidence standard changed.
- `RUNLOG.md`: current-cycle handoff, latest completed slice, residual risk, or next route changed.
- `prod_test.md`: the current task explicitly changed the project-specific production-test evidence ledger.

## Outputs

- Control-plane sync decision:
- Overflow/refactor decision:
- Files updated:
- Files marked `not_applicable`:
- Handoffs required:
- Evidence refs:
- Residual risks:

## Stop Conditions

- A required control-plane update is missing.
- The task would close with only code/artifact changes while scope, plan, tests, evals, runlog, or project ledger state changed.
- A needed update is skipped because a root control-plane file is near or over budget.
- `overflow_refactor_required` is needed but no redistribution decision names the owning files or source artifacts that received the detailed information.
- Ownership is unclear and no handoff is recorded.
- Verification evidence is missing for a completion, fixed, verified, ready, or release-ready claim.

## Per-task documentation synchronization

Assess documentation impact after every task, including small fixes and read-only outcomes. Assessment does not require rewriting a file or creating a report. Reuse the task Completion Report/evidence artifact. Record changed fact, source path/revision, canonical owner/path/section, decision (`updated`, `no_change_needed`, `handoff_required`), reason and evidence. Map the earlier checklist's `not_applicable` to `no_change_needed`; pending `update_required` becomes `updated` only after verified apply. Unresolved overflow or ownership stays `handoff_required`.

Use `sync_task_documents.py` for an approved section update or coordinated task completion: `assess` reads an existing packet; `preview` returns exact section diffs/recovery bytes; `apply --approved-digest` uses the reviewed proposal. For completion the packet includes `completion.matrix_path` and the existing TaskCompletion report fields. The task card and matching PLAN revision pin update through the same existing recovery journal. Other source pins and bytes outside the selected sections are preserved. A required unresolved handoff prevents implemented closure; report partial status instead. `create_task_plan.py complete --legacy-card-only` is compatibility-only and does not establish synchronized closure.

The `documentation_sync_v1` contract is implemented in `product_agent_os/documentation_sync.py`. `impact` has schema_version 1, task_id and bounded facts. Each fact has id, event, changed_fact, reason, decision and source path/revision references; a changed owner additionally has target path/revision, role, owner and section anchor. A no-change decision for a changed contract needs existing_coverage explaining that exact section. `patches` contains one fact_id/replacement per updated fact. Missing/new owners route to review or formation staging; this writer updates existing sections only. Explicit review inputs are not machine proof that all semantic changes were found.

Events route independently: requirements -> REQUIREMENTS; sequencing -> PLAN; verification_command -> TEST; eval_policy -> EVALS; handoff -> RUNLOG; architecture/decision/api/schema/operations -> their canonical domain documents. Evidence details stay in the owning task/evidence artifact. TEST stores commands and a short evidence pointer; RUNLOG stores the current handoff, not full command output. Reuse docs/adr, docs/runbooks or docs/ops, docs/testing and docs/archive when they are canonical. Unknown/ambiguous owners need a handoff, not a guessed second file.

Examples: an internal bugfix with unchanged contract records no_change_needed; an API/schema change updates only the affected contract; a test rerun records its outcome in the existing evidence owner and does not rewrite unchanged commands; a new documentation domain goes through formation preview; a repeated identical task update performs zero writes; out-of-scope ownership records handoff_required. A linked brief summary or explicitly reviewed current mirror may be retained. Exact cross-document copies/conflicting task states require disposition; semantic duplication remains a review question, never automatic deletion.

Event-scoped sync, size-triggered lossless compaction and periodic hygiene are separate. Active/navigation files warn at 32 000 and stop above 40 000 UTF-8 bytes unless a stricter limit applies; detailed docs/planning matrices retain the existing exception. Do not split the current research matrix or delete/summarize original evidence automatically. Recovery journals retain before-images and refuse later user edits. Exclude external writers; this is recoverable multi-file coordination, not ACID or an authorization grant. Weekly/monthly hygiene remains read-only, schedule_status=not_created. These instructions and local checks do not prove fresh-session activation, semantic completeness or owner acceptance.
