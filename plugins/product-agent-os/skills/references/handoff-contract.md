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

- Complete task context
- Source constraints
- Allowed sources
- Inputs used
- Owned files
- Forbidden files
- Expected evidence
- Handoff output schema
- Stop conditions
- Sequential fallback
- `complete_task_context`
- `source_constraints`
- `allowed_sources`
- `inputs_used`
- `owned_files`
- `forbidden_files`
- `expected_evidence`
- `handoff_output_schema`
- `stop_conditions`
- `sequential_fallback`

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

Rules:

- `goal`, `constraints`, and `verification_evidence` must not be empty when a skill claims readiness.
- At least one of `files_touched` or `files_proposed` must be non-empty.
- `unsupported_claims` must be explicit when sources or runtime checks are missing.
- `commands_run` records command strings, not invented outcomes.
- `verification_evidence` records observed results from the current run.
- `stop_reason` is required when the skill cannot advance the lifecycle.
- Reject handoffs that claim readiness without evidence, hide unsupported claims, omit stop conditions, or blur touched files with proposed files.
- Fresh-context handoff is required before any subagent or parallel worker starts.
- `complete_task_context` must be enough to work without raw conversation history.
- `source_constraints`, `allowed_sources`, and `inputs_used` must be explicit.
- `owned_files`, `forbidden_files`, and expected evidence must be explicit per worker.
- The handoff output schema must say what the worker returns: files touched, files proposed, commands run, verification evidence, unsupported claims, risks, and stop reason.
- Use sequential fallback when shared ownership ambiguity, missing handoff schema, cross-agent file ownership, missing expected evidence, or unresolved stop conditions remain.
- Require worktrees or explicit ownership for shared generated files, contracts, migrations, public APIs, schemas, release files, or rollback-sensitive work.
- Read-only research can proceed without a worktree when no writes, external actions, MCP activation, hooks, or automation are requested.
- Do not advance to parallel work when a missing handoff schema or missing expected evidence remains.
- Do not advance live/provider/mutation work when audit evidence is missing, security/privacy negative cases are unverified, degraded graph-only mode is hidden, ownership or verification evidence is missing, or `provider_call_allowed` / `external_call_performed` would be true without explicit approval.
