# Task Plan Lifecycle

Source status: project-local system workflow.

## Purpose

The config-routed lifecycle workflow contract in `.codex/config.toml` routes the root to `task_start_brief`, `completion_ledger`, this workflow, `control_plane_sync`, and `agent_context_contract`. The two packet templates own their fields; do not duplicate the field lists in role prompts. Chat is Russian; stored artifacts follow project language policy. Never persist private raw chat.

## Applicability

Use the full Task Start Brief and Completion Ledger for large/high-risk or financially material implementation, release/readiness closure, or an explicit packet request. Ordinary fixes and read-only/partial/blocked work use concise results, evidence and gaps unless the full scope applies. Do not force a plan row or duplicate packet artifact for a small fix. A read-only request authorizes inspection and reporting, not implementation or marker writes.

First read applicable instructions, the packet template and enough source to identify scope. Show the applicable start packet before broad exploration or edits. Uncertain values must be marked inferred; unavailable metrics need a concrete trace limitation. A heading or merged progress paragraph is not a full packet.

## State Ownership

- The root owns, within its chat, the visible Task Start Brief, session-bound lifecycle marker, terminal Completion Ledger or concise result, and Control-Plane Sync. Independent chats do not share a current-task marker; coordinate only overlapping file ownership.
- Delegated agents return a Subagent Result Packet; never start or close a nested lifecycle or update the root marker.
- Source-owned task-group JSON owns machine status; the concrete task-matrix plan owns task detail; RUNLOG.md owns a compact current-cycle handoff; TEST.md owns verification routes and ceiling.
- Reuse the owning detailed evidence artifact. Do not create a separate script/report/state file per command or persist a duplicate of the visible packet by default.
- Required partial, blocked or unreviewed children prevent parent completion. Update only the owning task status.

## Before Execution

1. Classify request type, scope, risk, financial materiality, release/readiness and explicit packet request. This is a declared workflow decision, not a security permission grant.
2. Show the Task Start Brief when full packets apply; for ordinary authorized mutations show a concise scope/evidence/limits note. A separate full packet is not required for an ordinary fix.
3. Inspect relevant source, ownership, worktree, existing tests and rollback. For complex work use task_matrix_plan_v1 with planned status and pending_execution_timestamp; otherwise reuse the current plan with a concrete lightweight-exception reason.
4. Before authorized non-mechanical mutations, record the minimal lifecycle marker below. Preserve user work. Read-only tasks need no marker mutation.
5. Validate a new or changed concrete plan with `python plugins/product-agent-os/scripts/validate_task_matrix.py <plan-file>`.

## Session Isolation

Use the marker path displayed by SessionStart. With host `session_id`, it is
`.codex/product-agent-os/lifecycle-state.<sha256(session_id)>.json`, where the hash
uses UTF-8 and lowercase hexadecimal. Record the matching `session_id` in the
marker. PreToolUse, SessionStart and Stop select the same path from the top-level
host envelope; tool-input fields cannot select a different session. Subagents
use the parent session and do not own separate root lifecycle transitions.

The unsuffixed `.codex/product-agent-os/lifecycle-state.json` is legacy-only for
callers without session identity. Never fall back to it when session_id exists,
and never wait for or reset another chat's marker. A missing own marker requires
the applicable brief and new own marker, not permission from another chat.
For a new user-authorized task in the same chat, preserve the prior closure and
start the new scope; terminal state does not grant additional old-task writes.

Bootstrap supports one exact Add/Update patch to the selected marker, or one
literal Set-Content write to that path. A body mention, foreign marker, move/delete
or mixed patch is not bootstrap. Dynamic shell/code writes are not an authorization
interface. Existing sandbox/approvals and path/secret restrictions still apply.
Reporting metadata is not a filesystem lock or proof of user approval; concurrent
edits to the same source still need explicit ownership coordination.

## Lifecycle Marker Fields

Common fields: `task_id`, `plan_path` when a concrete owning plan exists, `scope`, timezone-aware `updated_at`, `approval_boundary`, `status: in_progress`, `completion_ready: false`, `brief_digest: sha256:<64 lowercase hex characters>`, `brief_schema_version`, `brief_format`, `brief_fields_present`. Do not store raw chat or secrets. Marker freshness and terminal-state checks remain mandatory.

New mutation scopes declare `lifecycle_scope`: `work_type` (`implementation` or `fix`), `size` (`bounded` or `large`), `risk` (`low`, `medium`, `high`), boolean `financially_material`, `release_or_readiness`, `explicit_packet_request`, and a nonempty `reason`. A full packet is required when any trigger applies. Review/research/planning classifications cannot authorize mutation through this marker.

- Full route: `brief_schema_version: task_start_brief_v2`, `brief_format: bold_fields`, all nine template labels in `brief_fields_present`, and `task_start_brief_shown: true` after the visible packet.
- Ordinary route: `brief_schema_version: task_scope_note_v1`, `brief_format: concise`, `brief_fields_present: [Scope, Evidence, Limits]`, `scope_note_shown: true`; do not claim a full Task Start Brief was shown.
- Compatibility: existing `task_start_brief_v1` field-list markers remain valid for already-started legacy sessions. Preserve historical task matrices and receipts. New tasks use the scoped contract.
- `plan_path` must be workspace-relative and stay inside the workspace. New concrete tasks name their owning plan; legacy markers may use the historical fallback.

## After Execution

1. Update the same task block and source-owned status. Use an actual Europe/Moscow DD-MM-YYYY HH:mm timestamp and current evidence; do not invent acceptance or review.
2. Run directly affected tests during changes and the required integrated gate on the combined final state. Repeat only for changed inputs, failures or unresolved material risk; retain original provenance for reused evidence.
3. Complete Control-Plane Sync and record Docs impact as updated, no_change_needed with reason, or accepted_gap with affected document, owner, risk and next step. An accepted docs gap cannot close a parent that requires the document.
4. Prepare the applicable Completion Ledger with all thirteen list items and `closure_contract: product-agent-os-completion-ledger-v2`, or a concise result/evidence/limits response. Review context must be self_review, separate_reused_context, separate_fresh_context or fresh_blind_review as actually observed. Unavailable counters use not_available with a reason; do not create raw transcripts or scripts only to fill them.
5. After all writes and checks, set `completion_ready: true` and status `ready_for_completion_ledger` (full route), `ready_for_completion_brief` (legacy or concise route), `blocked` or `stopped_repair_required`. Terminal states deny further mutations. Leave completion_brief_shown false or absent: file state cannot prove delivery.
6. Show the Completion Ledger or concise result once as the terminal final response. No tool calls are allowed after the Completion Ledger or concise terminal result. All follow-up work belongs to a later task.

## Verification And Hook Boundary

Use `validate_lifecycle_packet_text` for explicit local format checks and regression tests. It checks shape and explicit closure contradictions, not source truth, child evidence, review independence, metrics accuracy or product acceptance. Do not save a packet only to run this check unless the task needs that artifact.

PreToolUse retains command/path/secret restrictions plus scoped marker checks; reporting scope never expands sandbox or approvals. Stop is advisory only: no automatic chat validation, format-based rejection or corrective continuation. A missing literal heading must not cause the final answer to repeat. SessionStart points to the current templates and applicability. Changed hook definitions may require exact-hash trust review in `/hooks` and a fresh session. Never bypass trust or infer activation from local tests.

## Optional Pinned Report Authority

A research/review/planning task remains read-only by default. A separately approved
hook command may supply `--report-authority <workspace-relative-json>` followed by
`--report-authority-sha256 <64-lowercase-hex>` for one exact new Markdown report.
The grant has exactly `schema_version: 1`, `task_id`, `previous_task_id`,
`workspace_sha256`, `marker_sha256`, `output_path`, `issued_at`, `expires_at`.
Hash the resolved workspace with platform `normcase` and UTF-8; hash the exact
current marker bytes. The fresh nonterminal read-only marker must explicitly
name the prior task and a different current task. Expiry cannot exceed 24 hours.

Prepare and review the grant, exact command and source hashes before asking for
hook trust/activation approval. Never derive authority from tool payload fields,
reset a terminal marker automatically, or install a command/pin silently. Existing
sandbox, command/path/secret guards and host approvals remain authoritative.

The supported write is one literal `apply_patch` Add File, either direct or a
single `await tools.apply_patch(JSON-string)` call inside `functions.exec`
(optional `text(...)`). Dynamic wrappers, multiple calls, existing output,
neighboring paths, config/hooks/control-plane files, traversal and symlinks fail
closed. Shell writes are not supported. In pinned mode only literal
`Get-Content`/`Get-ChildItem -LiteralPath 'path'` with `login: false` are accepted
as shell reads; other commands need separate review. The default command without
report flags preserves the previous lifecycle route. This is a preflight check,
not an atomic write transaction or host activation receipt. Local fixtures do
not close the separate fresh-host positive/negative gate.

## Stop Conditions

- Required scope, ownership, verification or approval is missing.
- A required child, document or relevant gate is blocked, partial or unreviewed.
- A completion/readiness claim exceeds current evidence.
- A delegated agent tries to own root lifecycle or a terminal response has already been sent.
- A request would cross target, provider, external, Git, permission, publication or hook-trust boundaries without applicable authority.

Task plan generation updates durable task detail and Completion Report only. It does not manufacture a user-visible Task Start Brief or Completion Ledger, review verdict or metrics. Existing historical packet sections remain unchanged.

## Task Matrix Commands

Inspect required arguments with `python plugins/product-agent-os/scripts/create_task_plan.py new --help` and `python plugins/product-agent-os/scripts/create_task_plan.py complete --help`. The `new` command writes planned task detail; `complete` updates the selected task and Completion Report with supplied evidence. Neither command proves that a chat packet was shown. Validate the result with `validate_task_matrix.py`.
