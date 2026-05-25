# Skill Promotion Record

Source status: project policy artifact for `codex_agentic_workflow`.

## Owner

- Owner:
- Review date:

## Evidence

- `codex_agentic_workflow` gate set: `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, `agentic_evidence_before_completion`.
- Runtime routing context: Codex App, CLI, IDE extension, `codex exec`, GitHub Action, MCP, Agents SDK, automation.
- Manual thread evidence:
- Playbook evidence:
- Trigger tests:
- Negative trigger tests:
- Missing-input behavior:
- Verification failure behavior:
- Failure log:
- Plugin boundary:
- Automation manual stability threshold:

## Accepted Gap

- Status: `present_unverified | explicit_gap_accepted | approval_required`
- Reason:
- Follow-up condition:

## Residual Risk

- Promotion can happen before repeatability and failure modes are known.
- Memory as recall only:
- No silent activation:

## Approval Boundary

- Approval required before plugin packaging, automation activation, external writes, hook activation, MCP activation or GitHub Action changes.

## Verification

- Manual run count:
- Current command:
- Reviewer:

## Rollback

- Disable path:
- Owner:

## No Secrets

- Do not store secrets, tokens, private keys, private customer data or raw private chat logs.
