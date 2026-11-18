# AGENTS.md

## Project Map

Product-Agent OS is a local engineering workspace for Codex App, CLI and IDE
extension. Web/Desktop and the local service handle projects, tasks, sessions and
evidence. The Python plugin in `plugins/product-agent-os/` owns discovery,
lifecycle, staged infrastructure and verification. The RU/EN knowledge base
documents both surfaces.

- Start at `docs/product/index.md` for components, contracts and documentation owners.
- Use `PLAN.md` and `docs/planning/index.md` to find the current task owner and
  dependencies. Use `REQUIREMENTS.md` for scope and acceptance, `TEST.md` for
  verification, `EVALS.md` for eval thresholds and `RUNLOG.md` for the current handoff.
- Keep historical plans, approvals and receipts with their owning sources. Treat
  generated views as orientation. Ground claims in source, checks and owner decisions.
- Separate local or synthetic verification, actual runtime, human acceptance and
  release readiness. A role, template or configured pin alone establishes its
  presence in source. Record fresh-session evidence when claiming activation.

## Documentation And Sources

- Use Russian for user-facing docs and canonical OpenAI terms on first mention.
  Include `Source status:` on non-index pages except source registries.
- Use current official OpenAI sources for product claims and keep
  `docs/sources/registry.md` and `docs/sources/registry.en.md` in sync. Keep community
  reports under `docs/insights/` with `trust_level` and `verification_status`. Promote
  them to core guidance after verification or label them `community` or `experiment`.
  Use memory and chat for recall. Keep sensitive data out of docs and artifacts.
- Use the documentation owners in `docs/product/index.md` and the implementation
  atlas at `docs/diagrams/index.md`. Keep atlas navigation discoverable in `mkdocs.yml`.
  Each diagram page needs Mermaid, usage, related artifacts and failure modes.
  Check atlas, navigation and `tools/check_docs.py` impact when adding a workflow.
- Keep operating guidance in `docs/product-agent/`, runtime guidance in
  `docs/runtime/`, and reusable artifacts in `docs/artifact-templates/`.
  Use `docs/codex/use-cases-deep-analysis.md` for use-case extraction and
  `docs/playbooks/use-case-to-plugin.md` with `docs/artifact-templates/plugin-blueprint.md`
  for repeated workflows. Document inputs, outputs, checks, risks and the next artifact.
- Reuse project-local docs tooling under `.venv-docs/` and `.docs-tools/`.
  Approved vendored docs assets belong in `docs/assets/javascripts/vendor/`.
  Installation, vendoring and docs hook/automation activation require explicit
  authority. Claim `site/` freshness only after an authorized project-local build.

## Product-Agent Operating Model

- Read the lifecycle and workflow routes in `.codex/config.toml` when applicable.
  Use the linked Task Start Brief and Completion Ledger for large, high-risk or
  financially material implementation, release/readiness closure, or an explicit
  packet request. For ordinary, read-only, partial or blocked work, report the
  result, evidence and limits concisely. Stop is advisory.
- State what counts as done, the checks a reviewer should be able to observe, and
  the approved scope. For cross-boundary changes, record impact in the existing
  task or plan. For handoffs, link to the owning source and its revision.
- Before closure, apply `.codex/workflows/control-plane-sync.md`. Update only the
  owners of changed facts in scope, or record `no_change_needed` or `handoff_required`.
- Delegate independent work with explicit ownership, verification, handoff and
  stop conditions when authorized. Use `.codex/workflows/worktree-ownership.md`
  to bound overlapping edits. Branches and worktrees require explicit requests.
- Use task-matching skills. Promote working procedures through the existing
  playbook, skill, plugin and automation routes. Keep automation candidate-only
  until its promotion checks and explicit owner approval are satisfied.
- Use `python-design-patterns` and `python-code-style` for Python work as advisory
  guidance. For model or instruction changes, compare the same tasks against the
  recorded baseline, isolate one behavior change, and use `EVALS.md` for thresholds.

## Approvals And Acceptance

- Reuse authorization from the current request or the standing scope below.
  Require exact approval for actions outside that scope, including target
  mutation, live servers, browser automation, provider/model calls, canonical
  graph mutation, Git writes, installation, publication and external automation.
  The sandbox, managed policy and tool approvals still apply.
- Standing owner authorization for implementation, fixes and verification in this
  repository covers bounded synthetic acceptance with temporary loopback services,
  browser automation, native launcher checks and independently owned subagent work.
  Use disposable profiles and synthetic workspace roots. Perform fixture setup,
  pairing, checks, evidence capture and cleanup within that scope. Keep pairing
  and session material in memory. Exclude real credentials, existing OS credential
  entries, provider/model calls, public exposure, installation, system-policy
  changes, Git/publication and forced termination of apps containing user work.
- Real target workspaces are read-only until explicit approval identifies the
  action, target, owner, rollback and verification. Bind material release,
  publication or reviewed apply approval to the exact digest, revision or staged
  artifact. Reconfirm if the relevant reviewed content or authorized scope changes.
- Preserve failed and rejected receipts. For material manual acceptance, record
  the tested revision or build ID, observer, observed result and owner decision
  in the existing acceptance evidence. Report outstanding acceptance with the
  exact entry point, action, expected result and what to capture on failure.

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

- Inspect targets read-only. Use `python plugins/product-agent-os/scripts/render_infrastructure.py <workspace> --dry-run`
  before staging. Stage outside the target. Apply only through reviewed merge
  and verification with the required authority.
- Preserve user-authored files outside managed sections. Stage unmarked
  `AGENTS.md`, config, hooks, workflows and automations as companion proposals.
  Keep examples, templates and fixtures synthetic and free of user-specific paths.
- Packaged hooks are staged assets. The lifecycle `PreToolUse` hook may block
  mutating Product-Agent OS commands until the applicable brief or concise scope
  note is followed by the SessionStart-selected session marker. The unsuffixed
  `.codex/product-agent-os/lifecycle-state.json` is legacy-only. Preserve independent
  command, path, secret, approval and sandbox protections. Hook activation and
  scheduling require explicit approval and observed evidence in the target host.

## Verification

- Follow `TEST.md` for scoped commands, working directories, applicable gates and
  evidence reuse. Rerun checks affected by the change. Identify a reused receipt
  by original provenance and verify it still applies to the relevant inputs.
- Start with focused regressions and affected integrations. Broaden for
  cross-cutting risk, unknown impact, release qualification or an explicit request.
  Full discovery includes fixture/transcript evals. Keep the relevant authorization,
  secret/path, user-file preservation, migration and recovery checks.
- Compare the final diff with approved scope and file ownership. Inspect
  unexpected paths and preserve independent changes. Report what was checked,
  what failed or stayed unverified, and the boundary of each completion claim.

## Rollback

- Revert only files touched by the current maintenance slice.
- Preserve user-authored files and unrelated dirty changes.
- Do not use destructive git operations without explicit approval.
