# Hook Governance

Source status: project policy artifact for `codex_agentic_workflow`.

## Owner

- Owner:
- Review date:

## Evidence

- `codex_agentic_workflow` gate set: `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, `agentic_evidence_before_completion`.
- Runtime routing context: Codex App, CLI, IDE extension, `codex exec`, GitHub Action, MCP, Agents SDK, automation.
- Hook event:
- Matcher:
- Command:
- Read-only validation hook:
- Blocking or side-effecting hook:
- Failure behavior:
- Two-stage review required:

## Accepted Gap

- Status: `present_unverified | explicit_gap_accepted | approval_required`
- Reason:
- Follow-up condition:

## Residual Risk

- Hook files can execute automatically when activated.
- Memory as recall only:
- No silent activation:

## Approval Boundary

- Approval required before hook activation, command changes, blocking behavior, external writes, production data or permission changes.

## Verification

- Dry run:
- Reviewer:
- Result:

## Rollback

- Disable path:
- Owner:

## No Secrets

- Do not store secrets, tokens, private keys, private customer data or raw private chat logs.
