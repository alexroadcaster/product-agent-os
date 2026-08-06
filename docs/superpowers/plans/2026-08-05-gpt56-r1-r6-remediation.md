# GPT-5.6 R1-R6 Remediation Plan

Source status: `current project task plan`.

### Task `GPT56-R1-R6-REMEDIATION-2026-08-05`

- Task: Apply the approved R1-R6 remediation to project configuration, agent and skill contracts, semantic validation, and context hygiene.
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User requested implementation of findings R1-R6 from the GPT-5.6 configuration audit.
- Validator target: detailed task blocks
- Date and time of task implementation: 06-08-2026 03:46
- Depends on: Source-backed GPT-5.6 audit and current official Codex configuration, subagent, skill, and permissions documentation.
- Blocks: Honest project-local GPT-5.6 configuration and future behavioral promotion evaluation.
- Source: User request, research/2026-07-23-codex-gpt-5p6-system-files-audit.md, current repository files, and official OpenAI documentation checked during this task.
- Short description: Remove the ineffective permission-profile composition, set generic subagent defaults, align agent and skill write authority, add required MCP routing, strengthen semantic validation, and reduce durable prompt drift.
- Technical value: Makes active configuration and role contracts machine-checkable and internally consistent.
- Product value: Reduces ambiguous approvals, excessive context, missing source tools, and accidental use of expensive generic subagents.
- Scope: Project-local .codex config and agents, six Product-Agent OS skills, validator and tests/eval contract, root instruction compaction, stale references, and control-plane synchronization.
- Non-goals: Global Codex config changes, plugin installation, MCP activation proof, provider or model calls, browser/runtime checks, Git operations, release, deployment, publication, and external automation.
- Expected result: R1-R6 are implemented in local source files with deterministic contract checks and explicit remaining behavioral gaps.
- Acceptance criteria: Strict config loads; all agent profiles validate; write-authority conflicts are rejected; source roles have the official docs MCP route; generic subagents default to Terra medium; root and agent prompts meet size and phase-neutrality budgets; stale references are removed.
- Verification gates: Focused validator and contract tests, Product-Agent OS docs tests, documentation structure check, strict Codex doctor, and git diff hygiene.
- Risks / approval gates: Prompt compaction may remove necessary role nuance; external, global, provider, browser, hook activation, Git, release, deployment, and publication actions remain forbidden or approval-required.
- Complexity: high
- Estimated execution time: 60-90 minutes
- Agents: Primary Codex agent; no delegated subagents authorized.
- Skills: openai-docs, executing-plans, python-design-patterns, python-code-style, verification-before-completion.
- Output artifacts: .codex/config.toml, .codex/agents, Product-Agent OS skills, validator/tests/eval contract, AGENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md, and this task plan.
- Next step: Restart Codex for fresh MCP/SessionStart activation proof, then run same-effort and one-lower-effort behavioral comparisons before any promotion claim.

#### Completion Report

- status: implemented
- what was done: R1-R6 aligned active and generated config on native workspace-write, added Terra/medium generic defaults, explicit skill write authority, Docs MCP routing, semantic validator coverage, phase-neutral prompt compaction, stale-path fixes, and synchronized control-plane/source artifacts.
- files touched / work locations: .codex/config.toml, .codex/agents, .codex/evals, plugins/product-agent-os assets/skills/validators, tests/product_agent_os, AGENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md, docs/sources registries/inventory, and the GPT-5.6 audit/plan.
- technical value delivered: Configuration, agent, skill, source-tool, prompt-budget, phase-neutrality, and staged-path invariants are machine-checked without restoring volatile batch routing.
- product value delivered: Generic work defaults to Terra/medium, source roles have an official Docs MCP route, explicitly authorized local edits are no longer contradicted by skill prose, and durable context is smaller and less phase-biased.
- actual implementation date and time: 06-08-2026 03:46
- verification evidence: Agent validator 15/15 with zero config errors; focused contract tests 184 OK; docs tests 100 OK; hook tests 19 OK; hook validators OK; strict doctor 0 fail; fixture eval exit 0; transcript eval 26/26; Codex compatibility compatible; full discovery 1195 OK with 1 skip; documentation structure check OK.
- residual risks: Fresh-session Docs MCP/SessionStart activation, optional doctor MCP env warning attribution, and same-effort/one-lower-effort behavioral quality, latency, token, and cost evidence remain outside this local-only slice.
- follow-up: Keep R1-R6 as the static local baseline; obtain fresh runtime and comparative eval evidence before any quality, cost, latency, or promotion claim.
