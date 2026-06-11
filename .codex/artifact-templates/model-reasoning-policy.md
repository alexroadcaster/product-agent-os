# Model And Reasoning Policy

Source status: project policy artifact for `codex_agentic_workflow`.

## Owner

- Owner:
- Review date:

## Evidence

- `codex_agentic_workflow` gate set: `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, `agentic_evidence_before_completion`.
- Runtime routing: Codex App, CLI, IDE extension, `codex exec`, GitHub Action, MCP, Agents SDK, automation.
- Model policy by role:
- Reasoning policy by risk:
- Escalation rule:
- Downgrade rule:
- Cost/latency budget:
- Codex-native subagents vs Agents SDK decision:
- Unsupported claim check:

## Accepted Gap

- Status: `present_unverified | explicit_gap_accepted | approval_required`
- Reason:
- Follow-up condition:

## Residual Risk

- Memory as recall only:
- No silent activation:
- Risk:

## Approval Boundary

- Approval required before external writes, MCP activation, hook activation, automation activation, GitHub Action changes, production data access or Agents SDK app orchestration.

## Verification

- Current evidence:
- Eval or command:
- Reviewer:

## Rollback

- Disable path:
- Owner:

## No Secrets

- Do not store secrets, tokens, private keys, private customer data or raw private chat logs.
