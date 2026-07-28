# Agent Task Packet

Use this as the fresh-context handoff for any subagent or parallel worker. The packet must be complete enough for the worker to act without raw conversation history.

For Codex subagents, pair this task packet with a Subagent Context Packet before launch and a Subagent Result Packet after completion. The Agent Handoff / Context Packet must name role, `fork_turns`, prompt, allowed files, files actually read, and outputs.

## Task

- Goal:
- Lifecycle state:
- Usage mode:
- Task row id:
- Owner:
- Recommended role:
- Dependency status:

## Full Context

- Source/context used:
- Complete task context:
- Source constraints:
- Allowed sources:
- Inputs used:
- Requirements:
- Acceptance criteria:
- Architecture boundary:
- Files already reviewed:
- Assumptions:

## Ownership

- Owned files:
- Files out of scope:
- Forbidden files:
- Owned/forbidden files:
- Shared resources:
- Cross-agent file ownership:
- Conflict notes:
- Shared ownership ambiguity:
- Worktree required for shared generated files, contracts, migrations, public APIs, schemas, release files, or rollback-sensitive work:
- Read-only research exception:

## Execution Contract

- Allowed actions:
- Subagent Context Packet before launch:
- Subagent Result Packet after completion:
- Agent Handoff / Context Packet:
- Role:
- `fork_turns`:
- Prompt:
- Allowed files:
- Files actually read:
- Outputs:
- Approval requirements:
- Commands to run:
- Expected evidence:
- Accepted gaps:
- Documentation impact:
- Docs update path assigned:
- Rollback notes:
- Handoff output schema:

## Professional Code Authoring Contract

Use this section for non-mechanical code authoring, refactoring, defect fixes, dependency changes, generated-code edits, or AI-agent handoffs that can create technical debt. For docs-only, read-only, formatting-only, or tiny mechanical edits, record `not_applicable` with the reason and reduced evidence path.

- Coding standards workflow: `.codex/workflows/coding-standards.md`
- Coding standard checklist: `.codex/artifact-templates/coding-standard-checklist.md`
- Task classification:
- `not_applicable` reason:
- `enterprise_leverage_check`:
- `existing_capability_scan`:
- Local source/patterns inspected:
- Standard library or language construct option:
- Framework/platform API option:
- Current dependency option:
- Project helper or existing abstraction:
- `one_line_candidate`:
- Selected leverage path: `delete | configure | stdlib | language_construct | framework_api | platform_api | current_dependency | project_helper | tiny_adapter | small_custom_code | new_dependency | not_applicable`
- Rejected options and reasons:
- `negative_dependency_rule`:
- New dependency count:
- Dependency approval requirement:
- `deep_module_check`:
- Public API or runtime contract touched:
- `legacy_seam_check`:
- Characterization test or existing regression evidence:
- Refactoring behavior proof:
- Comment policy:
- `cleverness_budget`:
- Tests/evals tied to code-quality claim:
- Unsupported code-quality claims:
- Accepted gap:
- Raw research body or raw conversation history included: forbidden.

## Planning Control Governance

Hard gates live in validator/tests/skills. Hooks are reminder-only unless approved, and closure cannot claim readiness from hook reminders alone.

- Planning control governance:
- File/subsystem boundaries:
- No hook activation:
- No automation activation:
- No MCP activation:
- No Agents SDK runner:
- No external writes:

## Runtime Methodology Packet

Carry only the compact runtime methodology packet. Do not include raw conversation history; no raw conversation history belongs in this handoff.

- Runtime methodology packet:
- `methodology_packet`:
- Owner domain:
- Consumer domains:
- `finish_options`:
- Safe next action:
- Approval requirements:
- Evidence gaps:
- Stop conditions:

## AI/RAG Handoff Compatibility

- Legacy alias: `agent-handoff-contract.md` maps to this agent task packet.
- Handoff owner:
- Inputs:
- Output schema:
- Trace evidence:
- Stop condition:

## Stop Conditions

- Owned files are unclear.
- Required context is missing.
- Source constraints are missing.
- Handoff output schema is missing.
- Missing handoff schema.
- Expected evidence is missing.
- Shared ownership ambiguity exists.
- Cross-agent file ownership exists.
- Approval is required and not present.
- Verification command cannot run and no accepted gap exists.
- Non-mechanical code work is requested without `enterprise_leverage_check`.
- New custom code or dependency is proposed without `existing_capability_scan`.
- A new dependency is proposed without `negative_dependency_rule` and approval path.
- Shared modules, APIs, data models, generated code, or runtime contracts are touched without `deep_module_check`.
- Legacy or fragile code is refactored without `legacy_seam_check` and characterization or accepted gap.
- Code-quality claims are requested without tests/evals, current evidence, or accepted gap.
- Secret-bearing or customer data is needed.
- Parallel work is requested without this agent task packet.
- Auto subagent dispatch is requested.
- Overlapping ownership parallelism is unresolved.
- Raw chat history is needed.
- Do not advance to parallel work until the packet is complete.

## Sequential Fallback

- Sequential fallback:
- Reason parallel work is unsafe:
- Coordination needed before retrying parallel work:

## Scenario Handoff

Keep the handoff concise enough for the next role to act without reading raw conversation history.

- Sources/context used:
- Assumptions:
- Files touched:
- Files proposed:
- Commands run:
- Verification evidence:
- Unsupported claims:
- Open risks:
- Recommended next role:
- Stop reason:
- Next agent task:
