# Model And Reasoning Policy

Source status: project policy template grounded in current repository contracts and official OpenAI model guidance checked 2026-07-23.

## Owner

- Owner:
- Review date:
- Decision status: `draft | active_config | behavioral_promotion_pending | promoted | rolled_back`

## Active GPT-5.6 Role Policy

| Work class | Default model | Baseline effort | Escalation trigger | Downgrade trigger |
| --- | --- | --- | --- | --- |
| Architecture, lifecycle orchestration, review, security/privacy, release, completion judging, complex product/research decisions | `gpt-5.6-sol` | preserve current role value | irreversible decision, ambiguous multi-step reasoning, high-risk verification | only after same-task quality gate passes at lower effort or on Terra |
| Focused implementation, docs maintenance, graph/cockpit work, plugin construction, bounded exploration | `gpt-5.6-terra` | preserve current role value | repeated uncertainty, cross-system design, security/release consequence | mechanical and deterministic work with stable checks |
| High-volume repeatable processing | `gpt-5.6-luna` candidate only | define per eval | quality failure or ambiguous inputs | use only after explicit availability, quality, and cost validation |

Use the explicit `gpt-5.6-sol` or `gpt-5.6-terra` pin for durable roles. Treat the `gpt-5.6` alias as Sol routing, not as an independent quality tier.

## Migration And Promotion Gate

1. Preserve the previous reasoning-effort baseline on the first GPT-5.6 run.
2. Compare the same task at the preserved effort and at one lower supported effort.
3. Hold task input, tools, skill set, sandbox, approvals, output rubric, and verification commands constant.
4. Run in a fresh session so stale model/config/hook state cannot masquerade as activation proof.
5. Record correctness, instruction following, tool completion, unsupported claims, latency, tokens, and cost.
6. Promote only when quality is non-inferior at the selected threshold and cost/latency stay inside the declared budget.
7. Roll back the pin or effort independently; do not rewrite the prompt and change the model in the same comparison.

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

Approval is required before external writes, MCP activation, hook activation outside the already authorized local configuration, automation activation, GitHub Action changes, production data access, provider/API calls, or Agents SDK app orchestration.

## Verification

- Current evidence:
- Eval or command:
- Reviewer:
- Closure ceiling without behavioral comparison: `active_config_behavioral_promotion_pending`

## Rollback

- Previous model/effort:
- Disable or revert path:
- Owner:

## No Secrets

Do not store secrets, tokens, private keys, private customer data, raw private chat logs, or raw provider payloads.