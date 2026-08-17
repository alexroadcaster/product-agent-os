# Task Plan Lifecycle

Source status: project-local system workflow.

## Purpose

Use this workflow before and after execution when Product-Agent OS work needs a concrete task-plan file instead of a loose chat plan.

The source of truth is the config-routed lifecycle workflow contract in `.codex/config.toml`: `[product_agent_os.lifecycle_contract]` points to this workflow, `control_plane_sync`, and `agent_context_contract`. Agent profiles should reference that config route instead of duplicating field-level lifecycle rules.

Project-local lifecycle hooks are configured in `.codex/hooks.json`; scripts and the Product-Agent OS policy mirror live under `.codex/hooks/`. They may enforce the lightweight marker before mutating commands, but remain guardrails and reminders, not a substitute for the visible chat brief. New or changed non-managed hooks may require Codex `/hooks` trust review or a fresh session before they execute.

This workflow also defines the user-visible contract:

- Show the Task Brief in chat before execution starts.
- Show the Completion Brief once, as the terminal `final` response, after execution or handoff and after every write and verification command.
- Do not hide the brief only in a file, `prod_test.md` row, runlog, or generated artifact.

The lifecycle is root-owned. A delegated agent reads this workflow only for constraints: it must not create or update the lifecycle marker, show a nested Task Brief or Completion Brief, or run the shared Control-Plane Sync. It returns one compact Subagent Result Packet to the root agent.

## State Ownership

- Source-owned task-group JSON owns machine task status and dependencies.
- The concrete task-matrix plan owns task detail, acceptance and completion report.
- `.codex/product-agent-os/lifecycle-state.json` owns only the current root run; it is not durable task history.
- `RUNLOG.md` owns current execution evidence and handoff.
- `TEST.md` owns verification routes and the evidence ceiling.
- Projection conflict is a stop condition: repair the owning source first, then update projections once.

## Before Execution

0. The root agent shows the Task Brief to the user before editing or running non-read-only execution commands. Delegated agents do not repeat it.
1. Create a detailed task block with `task_matrix_plan_v1`.
2. Keep status `planned`.
3. Use `pending_execution_timestamp` for date and time of task implementation.
4. Name product value, technical value, scope, non-goals, expected result, acceptance criteria, verification gates, risks, agents, skills, output artifacts, complexity, estimated execution time, and next step.
5. Record the lifecycle marker at `.codex/product-agent-os/lifecycle-state.json` after the user-visible full field-list Task Brief is shown. The marker must include `task_start_brief_shown: true`, `task_id`, `scope`, `updated_at`, `approval_boundary`, `brief_schema_version: task_start_brief_v1`, `brief_format: field_list`, `brief_digest`, and `brief_fields_present` containing every required Task Brief field below. Do not store raw chat, secrets, private source bodies, or private customer data in this marker.
6. Validate the plan file before execution:

```powershell
python plugins\product-agent-os\scripts\validate_task_matrix.py <plan-file>
```

Optional generator:

```powershell
python plugins\product-agent-os\scripts\create_task_plan.py new --output <plan-file> --task-id <id> --task <id> --plan-trigger <trigger> --source <source> --short-description <text> --technical-value <text> --product-value <text> --scope <text> --non-goals <text> --expected-result <text> --acceptance-criteria <text> --verification-gates <command-or-gap> --risks-approval-gates <text> --complexity <low-medium-high> --estimated-execution-time <time> --agents <roles> --skills <skills> --output-artifacts <paths> --next-step <text>
```

## After Execution

1. Update the same task block, not only a summary table.
2. Change status to `implemented` only when current evidence exists or an accepted gap is recorded.
3. Replace `pending_execution_timestamp` with actual `DD-MM-YYYY HH:mm` time in `Europe/Moscow`.
4. Fill the Completion Report: what was done, files touched / work locations, technical value delivered, product value delivered, verification evidence, residual risks, and follow-up.
5. Validate the plan file again and run the configured Control-Plane Sync plus every required final check.
6. Before the user-visible brief, update the lifecycle marker with `completion_ready: true` and terminal `status: ready_for_completion_brief`, `blocked`, or `stopped_repair_required`; include the final result status, compact completion summary, verification summary and next action. Keep `completion_brief_shown: false` or omit it; a file marker cannot prove that chat content was displayed.
7. Re-read the request, inspect the final diff and prepare exact artifact references. Complete all tool calls at this step.
8. Show the Completion Brief once as the terminal `final` response after execution, verification, or a blocked handoff. No tool calls are allowed after the Completion Brief. Its delivery is chat/transcript evidence, not a post-response file mutation.

Optional generator:

```powershell
python plugins\product-agent-os\scripts\create_task_plan.py complete --path <plan-file> --task-id <id> --timestamp <DD-MM-YYYY HH:mm> --what-was-done <text> --files-touched <paths> --technical-value-delivered <text> --product-value-delivered <text> --verification-evidence <command-evidence> --residual-risks <text> --follow-up <text>
```

## Outputs

- User-visible Task Brief:
- Pre-execution detailed task block:
- User-visible Completion Brief:
- Post-execution Completion Report:
- Validation command:
- Evidence ref:
- Handoff target:

## Task Brief Fields

- Task ID:
- Product value:
- Technical value:
- Source / trigger:
- Scope:
- Non-goals:
- Agents and skills:
- Files / artifacts expected:
- Verification gate:
- Approval boundary / risks:
- Complexity:
- Estimated execution time:
- Next action:

## Lifecycle Marker Fields

- `task_start_brief_shown`: `true` only after the full Task Brief is visible in chat.
- `task_id`: the current task or slice ID.
- `scope`: concise scope boundary.
- `updated_at`: current timestamp with timezone.
- `approval_boundary`: concise forbidden/approval-required surfaces.
- `brief_schema_version`: `task_start_brief_v1`.
- `brief_format`: `field_list`.
- `brief_digest`: `sha256:<hex>` digest or stable short digest for the visible brief content.
- `brief_fields_present`: list containing every field from `Task Brief Fields`.
- `completion_ready`: `true` only after implementation or handoff, task-plan update, control-plane sync, final verification and exact artifact references are complete.
- `status`: `in_progress` while mutations are allowed; `ready_for_completion_brief`, `blocked`, or `stopped_repair_required` immediately before the terminal Completion Brief. Every terminal status and legacy `completed` deny further mutations.
- `completion_brief_shown`: legacy compatibility field only. It cannot prove chat delivery and must not require a post-Brief write.

A legacy marker with only `task_start_brief_shown`, `task_id`, `scope`, `updated_at`, and `approval_boundary` is not sufficient for non-mechanical execution.

## Completion Brief Fields

- Task ID:
- Result status:
- What was done:
- Files / artifacts changed:
- Verification evidence:
- Residual risks / accepted gaps:
- Follow-up:

The headings above are the Stop-hook validation contract. Put them in the terminal `final` response; do not emit a block titled `Completion Brief` in intermediate commentary.

## Stop Conditions

- The work is small and mechanical and a lightweight exception is explicitly recorded.
- A required Task Brief or Completion Brief would be missing from the user-visible conversation.
- A mutating or non-read-only tool command is about to run while `.codex/product-agent-os/lifecycle-state.json` is missing or does not record `task_start_brief_shown: true`.
- Exact files, verification gates, evidence owner, or approval boundaries are unknown.
- Current evidence is missing for an `implemented`, `fixed`, `verified`, `ready`, or `release-ready` claim.
- The task would require external writes, provider calls, browser automation, git mutation, deployment, hooks, automation, or permission changes without approval.
- A tool call, file update, validation command, reference lookup, or lifecycle-marker write remains after the Completion Brief.
- A delegated agent attempts to own the root lifecycle, user-facing briefs, or shared Control-Plane Sync.
- Machine state, task-plan detail, lifecycle state, RUNLOG evidence or TEST evidence ceiling contradict their owning source.
