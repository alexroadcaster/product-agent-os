# Subagents, skills and AGENTS.md

Source status: `official + experiment`

Sources: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Skills](https://learn.chatgpt.com/docs/build-skills), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Product-Agent OS](../product-agent-os/index.md).

## Choosing a mechanism

| Mechanism | Use | Example |
| --- | --- | --- |
| AGENTS.md | Durable project rule | Test commands, documentation and source policy |
| Skill | Repeatable bounded method | Gather source, write card, verify claims |
| Subagent | Independent authorized work | Separate source research and review |
| Plugin | Distribute skills/tools/agents | A shared documented workflow package |

## Subagents

Local Codex can delegate on an explicit user request or applicable AGENTS/skill instructions. ChatGPT Work Ultra can delegate proactively. Stricter project policy remains separate: this project requires independent ownership and applicable authorization; tool availability alone is insufficient.

A bounded prompt names each source family, owned files, forbidden actions and expected output: sources, verified claims, uncertainty and proposed updates. The primary agent waits for results and consolidates findings without copying raw logs. Security, correctness, concurrency or test review can be separate responsibilities when the task justifies them; do not require a fixed number of agents.

## Fresh-context handoff contract

Generated `agent-skill-handoff.json` helps routing but does not replace a task packet.

| Field | Required content |
| --- | --- |
| Ownership | Owned files/subsystems, forbidden files, expected artifact |
| Fresh context | Current request, applicable rules, current sources and assumptions |
| Verification | Required commands, evals or an explicit evidence gap |
| Stop conditions | Approval boundary, missing source, conflicting ownership, failed check, stale context |
| Return packet | Sources, touched/proposed files, observed results, risks and next role |

Use sequential work when ownership overlaps or evidence cannot be obtained. Community claims remain intake material until trust level and verification status are explicit.

## Skills and promotion

A skill should have one job, clear inputs/outputs and verification. Keep SKILL.md focused; load references on demand; use scripts for deterministic work or external tooling, with authority checked separately.

`completion-skeptic` follows manual -> playbook -> skill -> plugin -> automation candidate. Owner review, rollback notes, failure log, eval cases and candidate-only status are required. Generated handoff/dashboard output is not promotion proof. Documentation/scorecard promotion includes owner review; it does not mean every routine authorized edit needs another approval.

Automation blockers remain explicit: active hooks, schedules, MCP servers, Agents SDK runners, provider calls and external writes need the applicable manual evidence and separate approval packet.

## Skill design rubric

| Criterion | Check |
| --- | --- |
| One job | One repeated workflow |
| Trigger | Description covers when to use and when not to use |
| Inputs / outputs | Required input and result contract are explicit |
| Progressive disclosure | References/scripts/assets loaded only when needed |
| Determinism | Scripts have a justified deterministic/tooling role |
| Evals | Trigger and non-trigger cases exist |

Candidate methods include source-card-writer, claim-verifier, insight-intake, docs-refresh, product-spec-writer, implementation-planner, test-gap-finder, release-note-writer, eval-loop-runner and ui-visual-reviewer. Naming a candidate does not install or activate it.

`agents/openai.yaml` can describe display metadata, invocation policy and tool dependencies. Explicit invocation may be a project choice for source-sensitive transfer; it is not a universal requirement for every skill.

## AGENTS.md

Keep durable applicable rules here, not task history: documentation language, official-source policy, community trust labels and required checks. Use the project-local docs runtime for strict builds. For discovery/override/size limits see [context engineering](../prompting/context-engineering.md); writing a file alone does not prove it was loaded.

## Custom-agent inheritance and activation

Checked 2026-11-03: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). A custom agent file defines `name`, `description`, `developer_instructions`, supported model/effort choices and capability restrictions. Permissions, approvals, provider and MCP inherit from the parent; agent-local `sandbox_mode`, `approval_policy`, `model_provider`, `mcp_servers` do not override them. A read-only role is a behavioral obligation until technical isolation is separately demonstrated.

Explicit spawn model/effort precede defaults; defaults/parent then resolve according to the official rules. Changing model without effort can select the new model default; custom-file overrides have their own ordering. Verify resolved model/effort rather than inferring them from a role name.

Skill `allow_implicit_invocation: false` disables implicit selection, not explicit invocation. Dependency metadata grants no permissions and does not prove MCP availability. Effective parent configuration and current tool evidence are needed; this refresh activates no MCP.

## Inputs

Current goal, applicable instructions, source context, ownership boundaries and required evidence.

## Outputs

A bounded work packet, source-backed result and explicit handoff with unresolved risks.

## Verification

Check applicability, authority, ownership and observed evidence before accepting a result.

## Risks

Overlapping writes, stale context and treating a proposed capability as activated behavior.

## When an installed skill is not used

Checked 2026-11-05: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Plugins](https://learn.chatgpt.com/docs/plugins).

1. Check a supported skill location and valid `SKILL.md`.
2. Check discovery and the initial list: its budget is limited; large catalogs can shorten descriptions and omit skills.
3. Use a short, distinct description and concrete trigger. Codex reads the full skill body after selecting it.
4. Compare explicit invocation with implicit routing. `allow_implicit_invocation: false` disables automatic selection but retains explicit invocation.
5. Start a new chat/session after plugin installation; check MCP authentication and tool availability separately.
6. Verify the result on a representative task: source presence, exposure and invocation are different evidence.

Start with an instructions-only skill. Scripts are for testable deterministic operations, not another agent loop. Agent roles, skills and plugins are separate components. Custom agents inherit parent permissions/MCP; a read-only role description does not create a sandbox.

At most intelligence levels delegation is requested explicitly; supported Ultra can delegate proactively. Check client/account and active instructions. Available subagents do not make a team mandatory: independent ownership, a budget and result reconciliation are still needed.
