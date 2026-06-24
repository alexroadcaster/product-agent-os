# Task Plan Lifecycle

Source status: `codex-plugin-template`

Project: {project_name}
Profile: {profile_name}

## Purpose

Use this workflow before and after execution when Product-Agent OS work needs a concrete task-plan file instead of a loose chat plan.

The source of truth is the config-routed lifecycle workflow contract in `.codex/config.toml`: `[product_agent_os.lifecycle_contract]` points to this workflow, `control_plane_sync`, and `agent_context_contract`. Agent profiles should reference that config route instead of duplicating field-level lifecycle rules.

Project-local lifecycle hooks are configured in `.codex/hooks.json`; scripts and the Product-Agent OS policy mirror live under `.codex/hooks/`. They may enforce the lightweight marker before mutating commands, but remain guardrails and reminders, not a substitute for the visible chat brief. New or changed non-managed hooks may require Codex `/hooks` trust review or a fresh session before they execute.

This workflow also defines the user-visible contract:

- Show the Task Brief in chat before execution starts.
- Show the Completion Brief in chat after execution or handoff.
- Do not hide the brief only in a file, `prod_test.md` row, runlog, or generated artifact.

## Before Execution

0. Show the Task Brief to the user before editing or running non-read-only execution commands.
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

0. Show the Completion Brief to the user after execution, verification, or a blocked handoff.
1. Update the same task block, not only a summary table.
2. Change status to `implemented` only when current evidence exists or an accepted gap is recorded.
3. Replace `pending_execution_timestamp` with actual `DD-MM-YYYY HH:mm` time in `Europe/Moscow`.
4. Fill the Completion Report: what was done, files touched / work locations, technical value delivered, product value delivered, verification evidence, residual risks, and follow-up.
5. Validate the plan file again.

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

A legacy marker with only `task_start_brief_shown`, `task_id`, `scope`, `updated_at`, and `approval_boundary` is not sufficient for non-mechanical execution.

## Completion Brief Fields

- Task ID:
- Result status:
- What was done:
- Files / artifacts changed:
- Verification evidence:
- Residual risks / accepted gaps:
- Follow-up:

## Stop Conditions

- The work is small and mechanical and a lightweight exception is explicitly recorded.
- A required Task Brief or Completion Brief would be missing from the user-visible conversation.
- A mutating or non-read-only tool command is about to run while `.codex/product-agent-os/lifecycle-state.json` is missing or does not record `task_start_brief_shown: true`.
- Exact files, verification gates, evidence owner, or approval boundaries are unknown.
- Current evidence is missing for an `implemented`, `fixed`, `verified`, `ready`, or `release-ready` claim.
- The task would require external writes, provider calls, browser automation, git mutation, deployment, hooks, automation, or permission changes without approval.
