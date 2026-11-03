# Model And Reasoning Policy

Source status: project policy grounded in official OpenAI guidance checked 2026-11-03.

## Owner

- Owner:
- Review date:
- Decision status: `draft | active_config | behavioral_promotion_pending | promoted | rolled_back`

## Active GPT-6 Role Policy

| Work class | Default model | Baseline effort | Escalation trigger | Downgrade trigger |
| --- | --- | --- | --- | --- |
| Engineering, planning, architecture, implementation, plugin/graph work, review, security, release and research | `gpt-6.1-sol` | preserve current role value | unresolved complexity; evaluate Astra separately | measured non-inferiority at lower effort |
| Docs maintenance and bounded exploration | `gpt-6.1-terra` | preserve current role value | engineering or ambiguous multi-step decisions route to Sol | measured narrow-task benefit before Luna |
| Highest-complexity or high-volume candidates | `gpt-6-astra` / `gpt-6-luna` candidate only | define separately | explicit measured need | no default activation |

Generic subagents use Sol with medium effort. Custom profiles pin both model and effort; these override resolved spawn/default/parent values. Account access remains unverified until an authorized fresh session. Current local CLI compatibility alone does not prove App availability. No silent fallback to older models.

## Migration And Promotion Gate

1. Preserve the previous effective reasoning effort for the first comparison.
2. Hold task inputs, tools, skills, parent permissions, approvals, output rubric and verification commands constant. Compare the same effort before trying one lower supported effort.
3. Configuration-contract repair changes the control surface; record it separately from model quality. Do not attribute combined effects to a model-only change.
4. Run an authorized fresh session and record effective model, effort, parent permissions and inherited MCP. Prompt restrictions do not create a separate sandbox.
5. Record correctness, instruction following, tool completion, unsupported claims, latency, tokens and cost.
6. Promote only after quality is non-inferior at the declared threshold and cost/latency stay within budget.
7. Restore the recorded prior model/effort independently. Never restore unsupported agent-local permission or MCP fields as a model rollback.

## Evidence

- `codex_agentic_workflow` gate set: `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, `agentic_evidence_before_completion`.

- Runtime routing: Codex App, CLI, IDE extension, `codex exec`, GitHub Action, MCP, Agents SDK, automation.
- Model policy by role:
- Reasoning policy by risk:
- Fixed comparison inputs/settings:
- Same-effort result:
- One-lower-effort result:
- Quality threshold and actual:
- Cost/latency/token budget and actual:
- Fresh-session activation evidence:
- Unsupported claim check:

## Accepted Gap

- Status: `present_unverified | explicit_gap_accepted | approval_required`
- Reason:
- Follow-up condition:

## Residual Risk

- Memory as recall only:
- No silent activation:
- Model availability or alias drift:
- Risk:

## Approval Boundary

Provider/API calls, external writes, hook/automation activation, target mutation, Git publication and production access require their own authority. Staged configuration does not activate a target workspace.

## Verification

- Current evidence:
- Eval or command:
- Reviewer:
- Closure ceiling without behavioral comparison: `active_config_behavioral_promotion_pending`

## Rollback

- Previous model/effort:
- Disable or revert path:
- Owner:

## Sources

- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/models
- https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart

## No Secrets

Do not store secrets, tokens, private keys, private customer data, raw private chat logs or raw provider payloads.
