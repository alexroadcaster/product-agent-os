# Product-Agent OS Handoff Contract

Use this reference when a skill hands work to the next lifecycle role or reports a stop condition.

Required fields:

- `lifecycle_state`
- `goal`
- `constraints`
- `allowed_sources`
- `inputs_used`
- `verified_claims`
- `unsupported_claims`
- `files_touched`
- `files_proposed`
- `commands_run`
- `verification_evidence`
- `risks`
- `next_agent_task`
- `stop_reason`

Fresh-context handoff fields for any subagent or parallel worker:

- Task row id
- Complete task context
- Source constraints
- Allowed sources
- Inputs used
- Owned files
- Forbidden files
- Owned/forbidden files
- Dependency status
- Expected evidence
- Handoff output schema
- Stop conditions
- Sequential fallback
- `task_row_id`
- `complete_task_context`
- `source_constraints`
- `allowed_sources`
- `inputs_used`
- `owned_files`
- `forbidden_files`
- `owned_forbidden_files`
- `dependency_status`
- `expected_evidence`
- `handoff_output_schema`
- `stop_conditions`
- `sequential_fallback`

Subagent transparency packet fields:

- Subagent Context Packet
- Subagent Result Packet
- Agent Handoff / Context Packet
- role
- `fork_turns`
- prompt
- allowed files
- files actually read
- outputs
- before launch
- after completion

Planning control governance fields:

- `planning_control_governance`
- `hard_gates_location`
- `hook_reminder_only`
- `docs_update_path_assigned`
- `no_hook_activation`
- `no_automation_activation`
- `no_mcp_activation`
- `no_agents_sdk_runner`
- `no_external_writes`

Compatibility and plan lifecycle fields:

- `compatibility_policy`
- `old_matrices_remain_historical_evidence`
- `task_matrix_plan_v1_scope`
- `historical_summary_table_validator_target`
- `plan_lifecycle_policy`
- `active_concrete_task_file_status`
- `runlog_evidence_destination`
- `source_backlog_history_destination`
- `source_registry_claim_destination`
- `no_automatic_deletion`
- `no_destructive_cleanup`

Live/provider/mutation handoff fields for Batch 31-style routing:

- `project_graph_live_audit_log`
- `project_graph_live_security_privacy_tests`
- `project_graph_runtime_observability`
- `project_graph_agent_skill_handoff_routing`
- `ownership_required`
- `verification_evidence_required`
- `fresh_context_required`
- `provider_call_allowed`
- `external_call_performed`
- `degraded_graph_only_mode_visible`

Scenario handoff aliases used in workflow templates:

- Sources/context used -> `allowed_sources` and `inputs_used`
- Assumptions -> `unsupported_claims` when unverified, or `verified_claims` when evidence-backed
- Files touched -> `files_touched`
- Files proposed -> `files_proposed`
- Verification evidence -> `verification_evidence`
- Open risks -> `risks`
- Recommended next role -> `next_agent_task`
- Stop reason -> `stop_reason`

Doubt verification handoff mapping:

- `doubt_verification_packet` remains the detailed companion artifact for completion-skeptic evidence.
- `claim_ledger` supported entries map to `verified_claims`.
- `claim_ledger` unsupported, contradicted, stale, missing, or assumption entries map to `unsupported_claims`.
- `evidence_ledger` command and source records map to `commands_run` and `verification_evidence`.
- `requirement_ledger` missing, partial, approval-required, or accepted-gap entries map to `risks` until resolved or explicitly accepted.
- `approval_boundary` hits map to `stop_reason` and `next_agent_task` when the next safe action is approval, owner review, or a different lifecycle role.
- `accepted_gap` entries must preserve owner, reason, residual risk, and follow-up; they do not become supported claims.
- Generated dashboards are not completion proof; generated status, site, report, or graph views can be orientation evidence only.
- The completion skeptic owns the completion-claim gate; `risk-reviewer`, `test-eval-designer`, and `docs-maintainer` consume confirmed gaps through this mapping rather than re-litigating the whole packet.

Rules:

- `goal`, `constraints`, and `verification_evidence` must not be empty when a skill claims readiness.
- At least one of `files_touched` or `files_proposed` must be non-empty.
- `unsupported_claims` must be explicit when sources or runtime checks are missing.
- `commands_run` records command strings, not invented outcomes.
- `verification_evidence` records observed results from the current run.
- `stop_reason` is required when the skill cannot advance the lifecycle.
- Reject handoffs that claim readiness without evidence, hide unsupported claims, omit stop conditions, or blur touched files with proposed files.
- Fresh-context handoff is required before any subagent or parallel worker starts.
- Task rows from `task-matrix-plan.md` must map to fresh-context packets by task row id.
- `complete_task_context` must be enough to work without raw conversation history.
- Do not use raw chat history or raw conversation history as worker context.
- `source_constraints`, `allowed_sources`, and `inputs_used` must be explicit.
- `owned_files`, `forbidden_files`, owned/forbidden files summary, dependency status, and expected evidence must be explicit per worker.
- The handoff output schema must say what the worker returns: files touched, files proposed, commands run, verification evidence, unsupported claims, risks, and stop reason.
- Do not auto-dispatch subagents from a handoff packet; return staged packets until the user or approved runner starts work.
- Do not allow overlapping ownership parallelism; use sequential fallback when workers need the same file, subsystem, public contract, generated artifact, or release surface.
- Use sequential fallback when shared ownership ambiguity, missing handoff schema, cross-agent file ownership, missing expected evidence, or unresolved stop conditions remain.
- Require worktrees or explicit ownership for shared generated files, contracts, migrations, public APIs, schemas, release files, or rollback-sensitive work.
- Read-only research can proceed without a worktree when no writes, external actions, MCP activation, hooks, or automation are requested.
- Do not advance to parallel work when a missing handoff schema or missing expected evidence remains.
- Do not advance live/provider/mutation work when audit evidence is missing, security/privacy negative cases are unverified, degraded graph-only mode is hidden, ownership or verification evidence is missing, or `provider_call_allowed` / `external_call_performed` would be true without explicit approval.
- Planning control governance: hard gates live in validator/tests/skills, hooks are reminder-only unless approved, agents own file/subsystem boundaries, docs update path assigned, and closure cannot claim readiness from hook reminders alone.
- Record no hook activation, no automation activation, no MCP activation, no Agents SDK runner, and no external writes unless an explicit approval packet changes the boundary.
- Compatibility policy: old matrices remain historical evidence. task_matrix_plan_v1 applies to new concrete task-plan files and optional backfilled rows only. Validator should not retroactively fail historical summary tables unless explicitly targeted.
- Plan lifecycle policy: active concrete task files remain active while they drive current execution, unresolved acceptance criteria, open verification gates or owner handoff decisions. Evidence moves to RUNLOG.md; history moves to docs/sources/*backlog*.md; source-backed claims enter docs/sources/registry*.md. No secrets, raw chat, customer data, credentials, tokens or private keys belong in handoff packets, task rows or examples. Avoid root PLAN.md bloat by keeping detailed history in the owning evidence artifact. No automatic deletion of task files, evidence rows or historical records. No destructive cleanup without explicit owner approval and rollback notes.
