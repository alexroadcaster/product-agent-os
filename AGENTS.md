# AGENTS.md

## Project Identity And Mission

This repository is the implementation, verification and evidence workspace for
Product-Agent OS: a local, governed engineering operating system for Codex App,
CLI and IDE extension. It is not merely a documentation collection.

Product-Agent OS audits a target workspace and the relevant Codex control
surfaces available in scope, determines project state and risk, stages the
required control plane, agents, skills, workflows and engineering artifacts,
selects applicable methodologies, and routes work from idea or defect through
requirements, planning, implementation, verification, review, release evidence
and learning.

The intended outcome is that a user ranging from a vibe-coder to an AI Engineer
receives reviewable specifications, bounded implementation slices, reproducible
bug fixes, verification evidence and explicit next actions instead of relying on
an unstructured chat history. Codex performs the engineering work; Product-Agent
OS controls order, evidence, ownership, approvals and claim boundaries.

The Russian Codex knowledge base, source registry and operator documentation are
supporting product surfaces: they explain, source and verify the system, but do
not define the repository as documentation-only.

## System Responsibilities

- Discover the target project's stack, structure, existing instructions, Codex
  assets, source boundaries, risks and missing evidence without mutating it by
  default.
- Establish or stage a durable project control plane: `AGENTS.md`,
  `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md`.
- Route greenfield ideas, existing features, bugs, legacy onboarding, AI/RAG,
  frontend, backend, API, data, security, release and maintenance work through
  only the methodologies and evidence gates that apply.
- Define agent ownership, skill use, handoffs, stop conditions, model/reasoning
  policy and approval boundaries before concurrent or high-risk implementation.
- Produce staged infrastructure, specifications, implementation plans, tests,
  evals, review packets, rollback evidence and safe merge proposals; apply local
  changes only through an authorized route that preserves user-authored files.
- Keep generated graphs, cockpits, dashboards and reports as orientation
  evidence; source files, current checks and owner decisions remain authoritative.

## Current Implementation And Claim Ceiling

| Surface | Current repository status | Claim ceiling |
| --- | --- | --- |
| Core plugin | Checked-in local plugin package with deterministic Python tooling, lifecycle skills, workflow and artifact templates, validators and eval fixtures. | Implemented local package; not an autonomous hosted delivery platform. |
| Workspace discovery and Architecture Intelligence | Read-only discovery, project graph, first-run analysis, cockpit/status/dashboard and evidence routing are implemented as local or staged surfaces. | Generated views help orientation and do not prove source truth, runtime behavior or readiness. |
| Project infrastructure | Dry-run/staging, manifest, approval-aware merge planning/apply, rollback and user-file preservation contracts are implemented. | Target mutation still requires the applicable explicit authority, preview and verification. |
| Product delivery routes | Requirements, architecture, implementation, bug rescue, test/eval, review, release-packet and learning routes exist with local contract and fixture evidence. | Every target project still needs current source reads, project-specific checks and owner decisions. |
| Agents and skills | Project-maintenance agents and packaged lifecycle skills cover discovery, product, architecture, implementation, verification, security, docs, release and learning responsibilities. | Role presence does not prove correct routing or task success; use current task evidence. |
| Self-learning and automation | Manual learning-loop and candidate-only automation governance are implemented. | `manual_only` / candidate-only until promotion gates and explicit owner approval are satisfied. |
| Product release and production use | The system can guide work toward production evidence and release readiness. | Broad Product-Agent OS release-readiness, autonomous production delivery and mass-project usefulness are not currently proven or promoted. |

## Control-Plane Role

`AGENTS.md` is the durable project instruction layer. It should stay compact and must not store full historical implementation ledgers, command logs or batch marker banks.

| Information class | Owning file |
| --- | --- |
| Durable project identity, rules, safety boundaries and claim ceiling | `AGENTS.md` |
| Current scope, acceptance and constraints | `REQUIREMENTS.md` |
| Current sequencing, queue, rollback and planning pointers | `PLAN.md` |
| Current verification commands, escalation rules and latest maintenance evidence | `TEST.md` |
| Current eval rubrics, thresholds and long-horizon quality gates | `EVALS.md` |
| Current-cycle handoff, latest completed slice and residual risks | `RUNLOG.md` |
| Batch 39 production test attempt, failure, fix and retest ledger | `prod_test.md` |
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
- Project-local documentation tooling belongs under `.venv-docs/`, `.docs-tools/node/`, `.docs-tools/bin/`, `.docs-tools/reports/` and, when approved, `docs/assets/javascripts/vendor/`; do not rely on global installs for docs freshness claims.

## Diagram Atlas Rules

- Keep `docs/diagrams/index.md` as the entry point for end-to-end project implementation.
- Maintain separate Mermaid pages for project delivery, agent teams and skills, runtime choices, skill lifecycle and context/memory/verification.
- Every diagram page must include `Source status:`, a Mermaid diagram, usage guidance, related artifacts or playbooks and common failure modes.
- When adding a product-agent workflow, check whether one of the diagram pages, `mkdocs.yml` or `tools/check_docs.py` must change.
- Diagrams must answer a practical project question and point to the next action or artifact.

## Product-Agent Operating Model

- Use `AGENTS.md` for durable rules only. Use `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` for active long-running product work.
- Before closing any non-mechanical Product-Agent OS task, run the local `.codex/workflows/control-plane-sync.md` checklist: update owned control-plane files when scope, sequencing, verification, evals, handoff state or an explicitly in-scope historical evidence ledger changed, or record `not_applicable` / `handoff_required`.
- Task Start Brief / Completion Ledger lifecycle is config-routed: load `.codex/config.toml` `[product_agent_os.lifecycle_contract]` and `[workflows]`. The linked templates own the nine start fields and thirteen ledger items. Full packets apply to large/high-risk or financially material implementation, release/readiness closure, or an explicit packet request; ordinary fixes and read-only/partial/blocked work use concise results, evidence and gaps unless that scope applies. Do not invent metrics, review context or completion. Stop is an advisory reminder, not automatic chat validation.
- Do not create or switch to a branch or worktree unless the user explicitly asks for it.
- Do not stage, commit, push, open a PR, launch live servers, run browser automation, call providers/live external model/API endpoints, mutate canonical graph sources or create external automations without exact approval for that action.
- Do not install documentation dependencies, vendor binaries/minified assets, activate documentation hooks/automation or claim generated `site/` freshness unless the current slice has explicit approval and records project-local smoke/build evidence.
- Use skills when the task matches a repeatable method. Promote project knowledge in this order: manual workflow, playbook, skill, plugin, automation, durable rule.
- Use subagents or parallel work only when ownership is independent and file/subsystem boundaries are explicit.
- Design agent teams around ownership, handoff artifacts, verification and stop conditions.
- Give durable project agents an explicit model/reasoning policy: default model, reasoning effort, escalation rules, downgrade rules and cost/latency budget.
- Use stronger reasoning for planning, architecture, review, debugging, eval judging, security and ambiguous multi-step work; use lower reasoning for bounded collection, mechanical edits and deterministic checks.
- For Python implementation work, use `python-design-patterns` and `python-code-style` as advisory guidance while preserving existing project patterns.
- Use eval-driven loops for subjective or long-horizon tasks: baseline, one focused change, rerun eval, inspect artifacts and stop only at threshold.
- Current Product-Agent OS execution status and historical batch evidence are source-owned by `PLAN.md`, `RUNLOG.md`, `prod_test.md`, the detailed backlogs, and the source registry; `AGENTS.md` does not carry batch ledgers.
- Real-project target evidence remains read-only unless an exact approval names the mutation, runtime, browser, provider, Git, or external surface, owner, rollback, and verification evidence.

## Agent File Contract

- Treat `.codex/agents/*.toml` as the active role profiles for maintaining this
  repository and executing approved Product-Agent OS slices. Treat
  `plugins/product-agent-os/assets/templates/agents/*.toml` as staged proposals
  for target workspaces; they are not the active team for this repository.
- Keep agent profiles role-based and phase-neutral. Store current task routing,
  batch state and completion evidence in `PLAN.md`, `RUNLOG.md` and their owning
  artifacts instead of durable `developer_instructions`.
- Route discovery and independent assurance through read-only roles such as
  `explorer`, `research-source-analyst`, `reviewer`,
  `security-privacy-supply-chain-reviewer`, `completion-skeptic` and
  `release-operator` unless a separately authorized task requires writes.
- Route approved workspace edits through ownership-specific roles such as
  `product-manager`, `architect`, `builder`, `plugin-runtime-builder`,
  `graph-cockpit-engineer`, `tester`, `docs-maintainer`,
  `learning-loop-engineer` and `lifecycle-orchestrator`.
- A writable agent may edit only its assigned files and responsibility slice.
  It must preserve unrelated dirty work, current control-plane authority and the
  approval boundary for target, provider, browser, Git, release or external actions.
- Validate active and generated agent profiles after changes. Model, reasoning
  effort and behavioral ownership must match the responsibility. Permissions,
  approvals, provider and MCP are inherited from the parent session; a read-only
  role does not create a separate sandbox. Custom profiles may only reduce
  supported capabilities. Do not imply runtime activation or production proof.

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
- Packaged hooks are staged target-project assets. The lifecycle `PreToolUse` hook may block mutating Product-Agent OS commands until the applicable full brief or concise scope note is followed by `.codex/product-agent-os/lifecycle-state.json`; command, path, secret, approval and sandbox protections remain separate. Do not add plugin-root hook activation or enable target-project hooks without explicit approval. A changed file does not prove fresh-session loading or trust.
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
