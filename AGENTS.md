# AGENTS.md

## Project Purpose

This repository is a Russian knowledge base for researching OpenAI Codex, advanced agentic workflows, multi-agent systems, memory, skills, subagents, prompt/context engineering, Codex runtime automation and product-agent workflows.

## Control-Plane Role

`AGENTS.md` is the durable project instruction layer. It should stay compact and must not store full historical implementation ledgers, command logs or batch marker banks.

| Information class | Owning file |
| --- | --- |
| Durable project rules, safety boundaries and current operating status | `AGENTS.md` |
| Current scope, acceptance and constraints | `REQUIREMENTS.md` |
| Current sequencing, queue, rollback and planning pointers | `PLAN.md` |
| Current verification commands, escalation rules and latest maintenance evidence | `TEST.md` |
| Current eval rubrics, thresholds and long-horizon quality gates | `EVALS.md` |
| Current-cycle handoff, latest completed slice and residual risks | `RUNLOG.md` |
| Source-backed historical registry | `docs/sources/registry.md` |
| Track 8 detailed scenario and methodology history | `docs/sources/product-agent-os-track-8-detailed-backlog.md` |
| Track 9 detailed methodology and verification history | `docs/sources/product-agent-os-track-9-backlog.md` |
| Track 10 detailed execution and verification history | `docs/sources/product-agent-os-track-10-backlog.md` |
| Batch 35 approval and execution evidence | `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |

## Documentation Rules

- Write user-facing docs in Russian.
- Keep official OpenAI terms in English on first mention: Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP and Agents SDK.
- Treat official OpenAI documentation as source of truth.
- Keep community tricks and user reports under `docs/insights/` with `trust_level` and `verification_status`.
- Do not move community claims into core guides unless they are verified or explicitly marked as `community` or `experiment`.
- Update `docs/sources/registry.md` and `docs/sources/registry.en.md` when adding or changing source-backed claims.
- Use `Source status:` on every non-index documentation page except source registry pages.
- Treat `docs/diagrams/` as the project implementation atlas and keep it near the top of MkDocs navigation.
- Keep product-agent operating guidance under `docs/product-agent/`, runtime execution guidance under `docs/runtime/` and reusable artifact templates under `docs/artifact-templates/`.
- Treat `docs/codex/use-cases-deep-analysis.md` as the official use-case extraction map.
- Use `docs/playbooks/use-case-to-plugin.md` and `docs/artifact-templates/plugin-blueprint.md` when turning a repeated workflow into a distributable plugin.
- Prefer behavior-level documentation over tool hype: every workflow should name inputs, outputs, verification, risks and the next artifact it produces.

## Diagram Atlas Rules

- Keep `docs/diagrams/index.md` as the entry point for end-to-end project implementation.
- Maintain separate Mermaid pages for project delivery, agent teams and skills, runtime choices, skill lifecycle and context/memory/verification.
- Every diagram page must include `Source status:`, a Mermaid diagram, usage guidance, related artifacts or playbooks and common failure modes.
- When adding a product-agent workflow, check whether one of the diagram pages, `mkdocs.yml` or `tools/check_docs.py` must change.
- Diagrams must answer a practical project question and point to the next action or artifact.

## Product-Agent Operating Model

- Use `AGENTS.md` for durable rules only. Use `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` for active long-running product work.
- Do not create or switch to a branch or worktree unless the user explicitly asks for it.
- Do not stage, commit, push, open a PR, launch live servers, run browser automation, call providers/live external model/API endpoints, mutate canonical graph sources or create external automations without exact approval for that action.
- Use skills when the task matches a repeatable method. Promote project knowledge in this order: manual workflow, playbook, skill, plugin, automation, durable rule.
- Use subagents or parallel work only when ownership is independent and file/subsystem boundaries are explicit.
- Design agent teams around ownership, handoff artifacts, verification and stop conditions.
- Give durable project agents an explicit model/reasoning policy: default model, reasoning effort, escalation rules, downgrade rules and cost/latency budget.
- Use stronger reasoning for planning, architecture, review, debugging, eval judging, security and ambiguous multi-step work; use lower reasoning for bounded collection, mechanical edits and deterministic checks.
- For Python implementation work, use `python-design-patterns` and `python-code-style` as advisory guidance while preserving existing project patterns.
- Use eval-driven loops for subjective or long-horizon tasks: baseline, one focused change, rerun eval, inspect artifacts and stop only at threshold.
- Current Product-Agent OS status: Tracks 1-8, Track 9 and Track 10 history is source-owned by the detailed backlogs and registry. Task 26 Batch 35 is complete through `done_through_m40`; `T10-LIVE-M41` remains `blocked_pending_explicit_git_release_fields`. B38-S1 records package-source freeze and metadata-audit evidence without closing M41: M01 blocked, M02 implemented, M03 accepted as a local-only metadata gap. M41 Batch 35 git preflight counts are historical evidence only; rerun fresh preflight before any git write.
- Current M41 missing fields: release branch or push target, commit message, PR base branch, PR title and intent, plus explicit branch creation/current-branch push policy.

## Windows Codex Shell Guard

In Codex App Windows PowerShell sessions, the inherited process environment may contain both `PATH` and `Path`. This can break PowerShell/.NET environment enumeration and `Start-Process` when redirecting stdout or stderr with `An item with the same key has already been added`.

Before running PowerShell commands that use `Get-ChildItem Env:`, `[System.Environment]::GetEnvironmentVariables()`, `Start-Process` with `-RedirectStandardOutput` or `-RedirectStandardError`, long-running background helpers or dashboard/dev-server launches, normalize `PATH`/`Path` in the same PowerShell invocation.

Use this as a process-local workaround only. Do not edit Windows registry `Path`, user environment variables or machine environment variables unless the user explicitly asks for a system-level change.

```powershell
$pathValue = [System.Environment]::GetEnvironmentVariable('Path', 'Process')
if ([string]::IsNullOrEmpty($pathValue)) {
    $pathValue = [System.Environment]::GetEnvironmentVariable('PATH', 'Process')
}
if (-not [string]::IsNullOrEmpty($pathValue)) {
    [System.Environment]::SetEnvironmentVariable('Path', $null, 'Process')
    [System.Environment]::SetEnvironmentVariable('PATH', $null, 'Process')
    [System.Environment]::SetEnvironmentVariable('Path', $pathValue, 'Process')
}
# command that enumerates env or uses Start-Process redirect follows here
```

## Product-Agent OS Plugin Rules

- Treat `plugins/product-agent-os/` as the implementation package for the local Product-Agent OS plugin.
- Treat `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md` as the active Track 9 implementation plan.
- Treat `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md` as the staged Track 10 implementation plan.
- Track 9 methodology intelligence work is section-by-section: read only the relevant task block, audit the matching `docs/methodologies/` source file, update the plan/backlog if the audit finds unrepresented concepts, then implement the focused slice with tests/evals/docs sync.
- Track 3 infrastructure generation is staged-first. Use `python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run` before staging infrastructure for a project.
- Use `--stage <output-dir>` only with an output directory outside the target workspace unless a later approved merge workflow proves a safe write path.
- Preserve user-authored files outside managed sections. Existing unmarked `AGENTS.md`, `.codex/config.toml`, hooks, workflows and automation files are user content and must be staged as companion proposals rather than overwritten.
- Packaged hooks are examples and staged target-project assets. Do not add plugin-root hook activation or enable target-project hooks without explicit approval.
- Automation artifacts under `assets/templates/automations/` are candidate-only. Do not create schedules, recurring jobs, GitHub Actions, Codex App automations or external workflows from Track 3 templates.
- Template files, fixtures and generated examples must remain synthetic and must not contain secrets, private customer data, raw private chat logs or absolute user-specific paths.

## Source And Insight Policy

- `docs/sources/registry.md` is the claim/source index; update it together with source-backed documentation changes.
- Store unverified observations under `docs/insights/`, not in core guides.
- Memory and chat history are recall layers, not source of truth.
- Generated dashboards, graph outputs and `site/` builds are orientation evidence unless an owning source document says otherwise.
- Do not store secrets, tokens, private keys, credentials, customer data or raw private chat logs in prompts, docs, memory, insights, examples, fixtures or templates.

## Verification

- For docs, source-registry, control-plane or test-contract edits, run:
  - `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
  - `python tools\check_docs.py`
  - `git diff --check`
- Run strict MkDocs when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.
- For plugin/runtime changes, run focused tests first, then route through `TEST.md` for full unittest, fixture eval, transcript eval and Codex compatibility checks.
- Do not claim a feature works or a maintenance slice is verified unless the relevant checks ran in the current run and their results are recorded.

## Rollback

- Revert only files touched by the current maintenance slice.
- Preserve user-authored files and unrelated dirty changes.
- Do not use destructive git operations without explicit approval.
