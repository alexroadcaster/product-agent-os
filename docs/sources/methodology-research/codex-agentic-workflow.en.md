---
title: "Archive - Codex / Agentic Workflow Methodology Research"
---

# Archive - Codex / Agentic Workflow Methodology Research {#codex-agentic-workflow-methodology-research}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official OpenAI + verified methodology + local implementation evidence + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/codex-agentic-workflow.md](../../methodologies/codex-agentic-workflow.md)

Target Product-Agent OS behavior: operate Codex as an engineering system, not as a chat transcript. Durable rules, task state, handoffs, evidence, approvals and promotion decisions must live in repository artifacts. Chat remains a working surface; checked-in or staged artifacts remain the source of truth.

## Scope

This dossier covers Codex App, CLI, IDE extension, `AGENTS.md`, skills, subagents, MCP, hooks, plugins, memories, sandbox, approvals, automations, Codex workflows/use cases, Agents SDK orchestration concepts, model/reasoning routing, context management, evidence-before-completion and Product-Agent OS lifecycle routing.

It does not create active hooks, MCP servers, automations, schedules, GitHub Actions or external writes. It does not replace official OpenAI documentation, and it does not treat community reports or memories as durable project rules.

## Supported facts

- OpenAI Codex documentation describes customization as complementary layers: `AGENTS.md` for persistent project guidance, memories for useful local recall, skills for reusable workflows, MCP for external tools/context and subagents for delegated specialized work.
- `AGENTS.md` is loaded before work starts and can be layered from global and project scopes. Files closer to the working directory override earlier guidance in the prompt chain.
- Codex best practices recommend task prompts that include goal, context, constraints and done condition; complex work should plan before implementation.
- Codex best practices describe `AGENTS.md` as the place to encode repo layout, commands, conventions, constraints and verification expectations.
- Codex skills package instructions, resources and optional scripts. Skills use progressive disclosure: metadata is visible for discovery, while full instructions are loaded only when selected.
- Codex plugins are the installable distribution unit. A plugin has `.codex-plugin/plugin.json` and can bundle skills, MCP configuration, hooks, apps/connectors and assets.
- Codex MCP connects Codex to external tools and context providers through `config.toml` and supports stdio and streamable HTTP servers.
- Codex hooks run deterministic lifecycle scripts and must be reviewed/trusted before non-managed command hooks execute.
- Codex subagents can run specialized agents in parallel when explicitly requested. Subagents inherit sandbox and approval controls from the parent workflow, and parallel workflows consume more tokens than comparable single-agent runs.
- Codex approval and sandbox guidance treats sandbox mode and approval policy as key autonomy controls. Default workspace-write behavior can read/edit workspace files while requiring approval for writes outside the workspace or network access.
- Codex memories can carry useful context across threads, but required team guidance belongs in `AGENTS.md` or checked-in documentation. Memories are a recall layer, not a rule source.
- Codex automations schedule recurring tasks. Official guidance says to test automation prompts manually first, review early outputs and use skills to define maintainable recurring workflows.
- Codex best practices summarize the promotion split: skills define the method, automations define the schedule.
- Codex use cases show repeated patterns: structured inputs, constraints, verification, audit output, and promotion into skills or automation only after the manual workflow is stable.
- Agents SDK guidance defines code-first agent applications where the application owns orchestration, tool execution, approvals and state. This is a different runtime layer from Codex App/CLI/IDE work, but it provides useful vocabulary for handoffs, tools, guardrails, sessions, tracing and evals.
- Agents SDK orchestration guidance distinguishes handoffs, where a specialist owns the next response, from agents-as-tools, where a manager keeps ownership.
- Agents SDK guardrails and human review guidance treats automatic validation and human approval as mechanisms that decide whether a run continues, pauses or stops.
- OpenAI agent eval guidance recommends moving from traces to repeatable datasets and eval runs once "good" behavior is defined.
- The local Product-Agent OS implementation already uses lifecycle skills, staged infrastructure rendering, candidate-only automations, fresh-context handoff artifacts, approval records, source-policy validation and evidence-before-completion checks.

## Assumptions

- Product-Agent OS should treat Codex App/CLI/IDE extension as human-in-the-loop engineering surfaces and Agents SDK as a programmable app-orchestration layer.
- Large project work should start with read-only discovery unless the requested task is trivial and already scoped.
- The default promotion path should be: manual thread -> playbook -> skill -> plugin -> automation.
- Subagents should be used only when work is independent enough to split by files, subsystem or evidence output.
- Parallel agents need fresh task packets, file ownership, forbidden files, expected evidence, stop conditions and handoff output schema.
- MCP, hooks, plugins and automations should be capability surfaces with explicit permission, trust and rollback/disable boundaries.
- Reasoning effort should be selected by task risk: lower for bounded read-only or mechanical work, stronger for architecture, debugging, security, eval judging, migrations and ambiguous multi-step work.
- Memories can reduce repeated context, but the project should never depend on them for mandatory rules, source policy, secrets policy or completion criteria.

## Unsupported claims not adopted

- "More agents are always better." Subagents add token cost and coordination risk.
- "Memory can replace documentation." Required team/project guidance belongs in `AGENTS.md` or checked-in docs.
- "A repeated idea is ready for automation." Automation needs manual success evidence, stable inputs/outputs, owner, verification and disable path.
- "MCP access means the agent may write external systems." MCP tools must follow source, approval, permission and side-effect boundaries.
- "Hooks are harmless because they are local scripts." Hooks run inside lifecycle events and require trust review, provenance and failure handling.
- "A plugin is just a folder of prompts." Plugins are installable packages with manifests, components, permissions, assets and update ownership.
- "Agents SDK should replace Codex App/CLI for every workflow." Agents SDK is useful for code-owned agent apps; Codex App/CLI/IDE remain the product-agent work surfaces.
- "Passing inspection proves completion." Completion claims need current evidence or explicit gaps.
- "Subagents can share raw chat context instead of task packets." Fresh-context handoff should carry only the task contract, source constraints, ownership and expected evidence.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Agentic delivery loop | Any non-trivial engineering/product work | Read-only discovery, smallest useful plan, focused slice, verification, risk review, handoff or release evidence. |
| Control-plane docs-as-state | Long-running or production work | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` hold state instead of relying on chat memory. |
| `AGENTS.md` durable rules | Team/project conventions recur | Encode repo layout, commands, standards, constraints, source policy and done criteria near the code they govern. |
| Progressive disclosure skills | Workflow repeats with stable triggers | Create `SKILL.md` with trigger, inputs, outputs, steps, scripts/references, verification and failure modes. |
| Plugin packaging lifecycle | Workflow must be shared or bundled | Package stable skills, MCP config, hooks/apps/assets and marketplace metadata with owner/update loop and evals. |
| Fresh-context handoff | Specialist or subagent work is useful | Use task packet with sources, assumptions, files, forbidden areas, expected evidence, output schema and stop conditions. |
| Ownership-bound parallelism | Work can split safely | Assign non-overlapping files/subsystems, require merge evidence and fall back to sequential work when ownership overlaps. |
| Approval-bound capability governance | External tools, side effects or privileged commands appear | Define sandbox, approval, MCP, hook, CI, publish, production and external-write boundaries before action. |
| Evidence-before-completion | Any claim that work is done/works/passes | Cite commands, artifacts, runtime output, traces/screenshots/evals or state the missing evidence explicitly. |
| Memory hygiene | Context repeats across threads | Use memory as local recall only; keep secrets out; promote durable rules into checked-in docs. |
| Automation promotion | Recurring work becomes predictable | Manual success -> skill/playbook -> candidate automation -> reviewed early runs -> active schedule. |
| Agent eval loop | Agent behavior quality matters | Baseline, one focused change, rerun eval, inspect traces/artifacts, log result, stop at threshold. |
| Runtime routing | Work can run in App, IDE, CLI, exec, GitHub, MCP, Agents SDK or automation | Choose the least complex runtime that satisfies ambiguity, permissions, evidence and repeatability needs. |
| Model/reasoning policy | Cost/latency/quality tradeoff matters | Define default model/reasoning, escalation, downgrade and budget by role or workflow. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| `AGENTS.md` | Durable project rules, source policy, commands, conventions, done criteria. | Codex project guidance |
| `REQUIREMENTS.md` | Users, goals, non-goals, constraints, acceptance criteria, source constraints. | Product-Agent OS control plane |
| `PLAN.md` | Smallest useful plan, file ownership, gates, rollback and verification. | Product-Agent OS implementation planner |
| `TEST.md` | Unit/integration/runtime/manual/eval checks and commands. | Test/eval designer |
| `EVALS.md` | Subjective or long-horizon quality thresholds, datasets and judge criteria. | AI/eval workflow |
| `RUNLOG.md` | Decisions, command evidence, failures, residual risks, next action. | Learning loop |
| `agent-task-packet.md` | Fresh-context packet for any subagent or parallel worker. | Agent team designer |
| `handoff-contract.md` | Handoff output schema, evidence fields and stop conditions. | Agent team designer |
| `worktree-ownership.md` | Parallel ownership map and merge boundaries. | Codex App worktrees / Git worktrees |
| `skill-candidate.md` | Manual workflow evidence before skill creation. | Skill lifecycle |
| `skill-failure-log.md` | Trigger misses, missing inputs, unsafe actions and verification failures. | Skill hardening |
| `plugin-blueprint.md` | Plugin users, bundled skills, MCP/hooks/apps, permissions, evals, owner. | Plugin packaging |
| `mcp-permission-review.md` | MCP tools/resources/prompts, trust level, side effects and approval policy. | MCP governance |
| `hook-activation-record.md` | Hook source, event, command, trust decision, failure behavior. | Hooks governance |
| `approval-record.md` | External write or privilege escalation approval, scope and rollback. | Sandbox/approvals |
| `automation-candidate.md` | Manual stability evidence, cadence, prompt, environment, verification, disable path. | Codex automations |
| `model-reasoning-policy.md` | Role/workflow defaults, escalation/downgrade rules and budget. | Codex/Agents configuration |
| `context-memory-policy.md` | What belongs in chat, RUNLOG, `AGENTS.md`, memory and source docs. | Memory hygiene |
| `agent-eval-case.md` | Input, expected behavior, trace/evidence, grader, threshold and failure label. | Agents evals |
| `release-packet.md` | Final evidence, risks, approvals and next action for merge/release. | PR/release operator |

## Project application instructions

1. Classify the task before starting: docs, web/front-end, backend, database, API, native/mobile, desktop, AI/eval, security, delivery/release, automation, plugin/skill, PR/review or long-running goal.
2. Start read-only unless the task is trivial, already scoped and low-risk. Read `AGENTS.md`, relevant docs, target files, existing patterns, commands and sandbox/approval constraints.
3. Write or update control-plane artifacts for long-running/product work. Use `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` when the task spans multiple slices or has ambiguous acceptance criteria.
4. Keep chat as an interaction surface, not the source of truth. Durable requirements, constraints, decisions and evidence must be written to project artifacts.
5. Use `AGENTS.md` for stable project rules only. Do not put one-off instructions, private data, secrets, raw chat logs or speculative community tricks there.
6. When a mistake repeats, add a concise durable rule or routing hint only after the failure is understood.
7. Use skills when a workflow has a clear trigger, repeatable inputs, expected outputs, verification and failure modes.
8. Create a skill from a proven manual workflow, not from an abstract idea. Log at least one successful run and one known failure/risk before treating it as reusable.
9. Package a plugin only when the workflow must be shared, installed, bundled with MCP/hooks/apps/assets or maintained with a clear owner/update loop.
10. Treat MCP as an external capability boundary. Document which tools/resources/prompts are exposed, what can mutate state, what needs approval and what data must not leave the workspace.
11. Treat hooks as executable policy. Stage hook definitions, document event/matcher/command/failure behavior and require trust review before activation.
12. Use subagents only for independent or specialist work. Every subagent needs a fresh task packet with sources, assumptions, owned files, forbidden files, expected evidence and stop condition.
13. Avoid overlapping edits across subagents. If file ownership overlaps or the merge risk is high, use sequential execution with review checkpoints.
14. Use worktrees or explicit ownership for parallel implementation. Do not let background work modify the same local checkout without a merge/rollback plan.
15. Keep sandbox and approvals tight by default. External writes, CI/GitHub changes, publishing, production data, network-heavy actions, MCP side effects and hook activation need explicit approval.
16. Select runtime by job: Codex App/IDE for ambiguity and steering, CLI for local engineering, `codex exec` for stable non-interactive jobs, GitHub Action for PR/CI, MCP for external tools, Agents SDK for code-owned agent apps, automation for stable recurring workflows.
17. Set model/reasoning policy by risk. Use stronger reasoning for architecture, review, debugging, security, eval judging, migrations and ambiguous multi-step work; lower reasoning for bounded read-only collection or mechanical edits.
18. Use memory only as recall. Required rules, source policy, acceptance criteria, secrets policy and verification commands must live in checked-in docs or current task artifacts.
19. Require evidence-before-completion. A final claim must cite current commands, checks, artifacts, runtime output, traces/screenshots/evals or explicitly state what was not verified.
20. Promote recurring workflows in order: manual thread -> playbook -> skill -> plugin -> automation. Automation is blocked until manual stability, owner, reviewable output, verification and disable/rollback path exist.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `.codex/`, `.codex/agents/`, `.codex/workflows/`, `.codex/artifact-templates/`, `.agents/skills/`, `.agents/plugins/`, `plugins/`, `skills/`, `subagents/`, `docs/playbooks/`, `docs/artifact-templates/`, `docs/product-agent/`, `docs/runtime/`, `docs/insights/`
- Files: `AGENTS.md`, `AGENTS.override.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `SKILL.md`, `.codex-plugin/plugin.json`, `.mcp.json`, `hooks.json`, `config.toml`, `automation.toml`, `agent-task-packet.md`, `handoff-contract.md`, `worktree-ownership.md`, `plugin-blueprint.md`, `automation-candidate.md`
- Terms: Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP, Agents SDK, hooks, plugin, automation, worktree, runlog, eval, handoff, task packet, source of truth, approval boundary, evidence
- Risk signals: external write, network access, production data, secrets, token, customer data, GitHub Action, publish, deploy, release, CI, hook activation, MCP side effect, automation schedule, overlapping edits, long-running goal

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `agentic_scope_classified` | Any Codex/product-agent workflow | Use-case archetype, runtime surface or task type is unknown. |
| `source_of_truth_present` | Long-running or production work | Durable artifacts are missing and chat would become the source of truth. |
| `control_plane_present` | Multi-slice work | `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` or `RUNLOG.md` are needed but absent. |
| `read_only_discovery_complete` | Non-trivial repo work | Relevant files, docs, commands, patterns and sandbox/approval context were not inspected. |
| `approval_boundary_present` | External write, privileged action, MCP side effect, hook, CI, release, production data | Approval scope, risk, rollback/disable path or owner is missing. |
| `fresh_context_handoff_present` | Any subagent, parallel worker or specialist handoff | Task packet lacks sources, assumptions, owned files, forbidden files, expected evidence, output schema or stop condition. |
| `ownership_split_present` | Parallel implementation or review | File/subsystem ownership overlaps or merge path is unclear. |
| `subagent_parallelism_safe` | User asks for subagents or parallel agents | Work is not independent, evidence outputs conflict or token/coordination cost is unjustified. |
| `skill_promotion_evidence_present` | New or changed skill | Manual success evidence, trigger, inputs, outputs, verification and failure modes are missing. |
| `plugin_boundary_present` | Plugin packaging or distribution | Manifest, bundled components, permissions, owner/update loop or eval cases are missing. |
| `mcp_permission_review_present` | MCP server/tool/resource/prompt added or used for side effects | Tool capability, trust level, data boundary, approval policy or secret handling is missing. |
| `hook_activation_approval_present` | Hook created, changed or enabled | Event/matcher/command/trust decision/failure behavior is missing or unapproved. |
| `automation_manual_stability_present` | Automation creation/update | Manual test evidence, durable prompt, cadence, environment, owner, verification or disable path is missing. |
| `model_reasoning_policy_present` | Durable agent/workflow role | Default model/reasoning, escalation/downgrade rules or budget are missing. |
| `memory_policy_present` | Memory or repeated context is used | Required rules live only in memory, or secrets/private context might be stored. |
| `agent_eval_workflow_present` | AI/agent behavior quality matters | Baseline, dataset/eval cases, threshold, rerun command or failure labels are missing. |
| `agentic_evidence_before_completion` | Any completion/readiness claim | Current verification evidence is missing or not tied to the claim. |

## Candidate eval fields

- The workflow starts from a classified use-case archetype and selected runtime surface.
- The plan names source-of-truth artifacts and avoids relying on chat memory.
- Read-only discovery includes current project docs, target files, commands and sandbox/approval context.
- Subagent or specialist work includes fresh-context task packet, ownership, forbidden files, output schema and stop conditions.
- Parallel work has explicit ownership or falls back to sequential execution.
- Skills are promoted only from proven manual workflows with verification and failure modes.
- Plugins include manifest, bundled component list, permissions, owner/update loop and eval cases.
- MCP additions include capability, trust, data, secret and approval review.
- Hook additions remain staged until trust review and failure behavior are documented.
- Automations remain candidate-only until manual stability evidence exists.
- Model/reasoning policy is explicit for durable agents or workflows.
- Memory is used as recall only and never as mandatory source of truth.
- Final claims cite current evidence or state gaps.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Work surface | Codex App, CLI, IDE extension | Choose by ambiguity, local command needs, editor context and steering requirements. |
| Durable rules | `AGENTS.md`, nested `AGENTS.md`, checked-in docs | Keep concise and practical; add rules after repeated friction. |
| Runtime automation | `codex exec`, GitHub Action, Codex automations | Use only for stable, non-interactive or recurring work. |
| Reusable methods | Skills with `SKILL.md`, scripts, references, assets | Method layer before schedule layer. |
| Distribution | Codex plugins with `.codex-plugin/plugin.json` | Package stable skills, MCP/hooks/apps/assets with owner/update loop. |
| External systems | MCP servers | Pair with skills and approval policy; avoid secret leakage. |
| Lifecycle controls | Hooks | Stage and trust-review before activation. |
| Parallel work | Subagents, custom agents, worktrees | Split by ownership and evidence output. |
| Programmable orchestration | Agents SDK | Use for application-owned agent workflows, not as default replacement for Codex App/CLI/IDE. |
| Evidence | Tests, builds, logs, screenshots, traces, evals, run logs | Evidence must match the claim being made. |

## Failure modes

- Chat contains the real requirements while project artifacts remain stale.
- `AGENTS.md` accumulates vague preferences, obsolete rules or one-off instructions.
- Subagents are spawned for overlapping edits without file ownership.
- Handoffs omit source constraints, assumptions, expected evidence or stop conditions.
- Skills are created from ideas without successful manual runs.
- Plugins are packaged before permissions, evals and owner/update loop exist.
- MCP tools are treated as safe because they are "just docs" even when they expose actions.
- Hooks are enabled without trust review or failure-mode documentation.
- Automations are scheduled before the prompt and tools are stable.
- Memory stores context that should have been checked into docs, or contains private/secrets material.
- Completion is claimed from inspection-only evidence.
- Agents SDK concepts are copied into Codex runtime docs without distinguishing runtime layers.

## Open questions for deeper research

- Should Product-Agent OS generate a dedicated `agentic-workflow-readiness.md` artifact or distribute these fields across `PLAN.md`, `RUNLOG.md` and `agent-task-packet.md`?
- Which readiness gates should become hard blocks in the plugin, and which should stay warning-level?
- Should MCP permission review be a standalone artifact or a section in `plugin-blueprint.md` and `approval-record.md`?
- Should hook activation always require a two-stage review, even for read-only validation hooks?
- How many successful manual runs are enough before a workflow can become a skill or automation?
- Should memory policy be part of `AGENTS.md`, `RUNLOG.md`, or a generated `context-memory-policy.md` template?
- How should Product-Agent OS compare Codex-native subagents with Agents SDK orchestration when both are available?
- Should model/reasoning policy be generated per role, per workflow, or both?

## Sources

- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [Codex customization](https://developers.openai.com/codex/concepts/customization)
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Agent Skills](https://developers.openai.com/codex/skills)
- [Subagents](https://developers.openai.com/codex/subagents)
- [Model Context Protocol](https://developers.openai.com/codex/mcp)
- [Hooks](https://developers.openai.com/codex/hooks)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [Memories](https://developers.openai.com/codex/memories)
- [Codex workflows](https://developers.openai.com/codex/workflows)
- [Codex automations](https://developers.openai.com/codex/app/automations)
- [Save workflows as skills](https://developers.openai.com/codex/use-cases/reusable-codex-skills)
- [Run verified operations](https://developers.openai.com/codex/use-cases/verified-operations-workflows)
- [Follow a goal](https://developers.openai.com/codex/use-cases/follow-goals)
- [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)
- [Agents SDK orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration)
- [Agents SDK guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)
- [Context7 research](../context7-research.md)
