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

## Professional Code Authoring Reminder Plan

- Reminder target: `professional_code_authoring_evidence_present`
- Candidate hook events: `PreToolUse` for mutating code edits; `Stop` for missing evidence reminder.
- Candidate-only status: hook templates may be staged, but no hook activation follows from this artifact.
- Reminder text must ask for `.codex/workflows/coding-standards.md` and `.codex/artifact-templates/coding-standard-checklist.md`, existing-capability scan, one-line candidate, selected leverage path, rejected alternatives, dependency decision, and `not_applicable` reason when skipped.
- Hard-stop boundary: block only when an explicitly approved project hook policy says non-mechanical code mutation requires lifecycle marker plus coding-standard evidence.
- Soft-reminder boundary: allowed as generated guidance only; it is not proof and must not claim verification.
- Automatic mode: AI agents apply the standard through skills/workflows/agent task packets first; hooks are deterministic reminders/guards after explicit activation.
- Methodology link: `quality_testing_evals` owns evidence; `codex_agentic_workflow` carries it through agents, subagents, skills, handoff and runtime route packets.

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
- Approval required before turning a professional-code reminder into an active blocking hook.

## Verification

- Dry run:
- Reviewer:
- Result:

## Rollback

- Disable path:
- Owner:

## No Secrets

- Do not store secrets, tokens, private keys, private customer data or raw private chat logs.
