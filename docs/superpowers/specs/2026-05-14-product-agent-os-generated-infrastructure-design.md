---
title: "Архив — Product-Agent OS Generated Infrastructure Design"
---

# Архив — Product-Agent OS Generated Infrastructure Design {#product-agent-os-generated-infrastructure-design}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + experiment`

Sources: [Codex build plugins](https://developers.openai.com/codex/plugins/build), [Codex hooks](https://developers.openai.com/codex/hooks), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md).

This design defines Track 3 for the [Product-Agent OS plugin spec](../../product-agent/product-agent-os-plugin-spec.md). It builds on the completed [Track 1 core plan](../plans/2026-05-14-product-agent-os-plugin-core.md) and [Track 2 lifecycle skills design](2026-05-14-product-agent-os-lifecycle-skills-design.md).

## Goal

Track 3 turns `product-agent-os` from a lifecycle guide into a project infrastructure generator. The plugin gains templates and scripts that can produce a staged infrastructure package for a user's workspace: control-plane files, project-scoped Codex assets, hooks, workflow packets, eval skeletons, and release packet templates.

The core rule is staged-first. Track 3 does not silently mutate a user's project. It renders a reviewable plan and staged artifacts, validates them, and leaves actual project writes behind explicit approval and merge-safe behavior.

## Design Choice

Use a staged infrastructure generator.

The plugin package owns reusable templates and rendering code. When applied to a project, it reads a workspace audit, lifecycle packets, and a complexity profile, then renders proposed artifacts into an output directory or dry-run JSON. A later approved write step may merge managed sections into project files, but hidden writes are not part of the default path.

Rejected approaches:

- Direct project writer: faster, but too risky for existing projects with user-authored `AGENTS.md`, `.codex/`, workflow files, and local conventions.
- Templates only: safe, but not a working tool because Codex would still need to assemble infrastructure manually.

## Existing Foundation

Track 1 already provides:

- plugin manifest and package skeleton under `plugins/product-agent-os/`;
- `contracts.py` with lifecycle states, complexity profiles, control-plane file names, and handoff validation;
- `discovery.py` and `detect_project.py` for workspace audits;
- `validators.py` and wrappers for control-plane files, agents, and hooks;
- `merge_markdown.py` for managed Markdown sections;
- fixture projects and `run_fixture_eval.py`.

Track 2 already provides:

- lifecycle skills that produce staged packets rather than direct writes;
- shared references for lifecycle state, handoff, source policy, and complexity routing;
- static tests that enforce staged-only boundaries and candidate-only automation.

Track 3 should reuse these contracts and scripts. It should not duplicate lifecycle routing inside template files.

## Scope

Track 3 adds:

- template registry and template completeness tests;
- control-plane file templates for `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, and `RUNLOG.md`;
- project-scoped `.codex/config.toml` proposal template;
- project-scoped `.codex/agents/*.toml` templates;
- hook templates that are packaged but not enabled automatically;
- staged hook lifecycle config template for `.codex/hooks/hooks.json`;
- `.codex/workflows/*.md` task packet templates;
- `.codex/evals/*.json` eval skeletons;
- `.codex/runlogs/archive/` or `docs/runlogs/archive/` compaction proposal templates;
- `.codex/automation-candidates/*.md` candidate-only automation packets;
- PR and release packet templates;
- staged renderer that creates an infrastructure plan and rendered artifacts;
- CLI wrapper for dry-run and staged output generation;
- fixture coverage for greenfield, existing config, missing tests, monorepo, docs projects, unsafe write requests, and failed verification evidence.

## Out Of Scope

Track 3 does not create active automations, scheduled jobs, or recurring runs. Automation stays candidate-only until Track 4 hardening and explicit user approval.

Track 3 does not add the optional Agents SDK runner, Codex MCP orchestration runtime, or external system integrations.

Track 3 does not change global Codex config, write user-level memory, install dependencies, use network access, call external systems, or publish PRs.

Track 3 does not claim tests, builds, hooks, or evals pass unless the current run executes the relevant checks and records evidence.

## Package Layout

Track 3 should create this package structure:

```text
plugins/product-agent-os/
  assets/
    templates/
      control-plane/
        AGENTS.md
        REQUIREMENTS.md
        PLAN.md
        TEST.md
        EVALS.md
        RUNLOG.md
      config/
        config.toml
      agents/
        product-manager.toml
        architect.toml
        explorer.toml
        builder.toml
        tester.toml
        reviewer.toml
        docs-maintainer.toml
        release-operator.toml
      hooks/
        hooks.json
        session_start_context.py
        pre_tool_use_policy.py
        permission_request_summary.py
        post_tool_use_evidence.py
        stop_runlog_reminder.py
      workflows/
        source-context-pack.md
        worktree-ownership.md
        build-slice.md
        review-slice.md
        release-packet.md
        runlog-compaction.md
      runlogs/
        archive/
          README.md
      evals/
        project-readiness.json
        handoff-completeness.json
        renderer-fixtures.json
      automations/
        automation-candidate.md
      pr/
        pr-body.md
        release-notes.md
  scripts/
    product_agent_os/
      templates.py
      infrastructure.py
    render_infrastructure.py
```

The exact template list may grow later, but Track 3 should keep the first version deliberately small and complete.

## Data Model

The renderer should accept a `WorkspaceAudit`-like dictionary from `discovery.py` and an optional lifecycle packet bundle from Track 2 skills.

The renderer should return:

```yaml
infrastructure_plan:
  status: "ready | blocked | needs_approval"
  profile: "guided-small | standard-product | production-team | ai-product | enterprise-governed | autonomous-maintenance"
  create: []
  update: []
  leave_unchanged: []
  blocked: []
  approval_required: []
  warnings: []
  questions: []
rendered_artifacts:
  root: ""
  files:
    - target_path: ""
      staged_path: ""
      action: "create | update | leave_unchanged | blocked"
      write_policy: "staged_only | approved_write_required"
  managed_sections: []
  validation:
    ok: true
    checks: []
```

`create` means the target file does not exist. `update` means a managed section or staged companion artifact is proposed. `leave_unchanged` means a user-authored file exists and no safe managed section is available. `blocked` means the renderer cannot proceed without user input or approval.

## Template Rules

All templates must be deterministic, portable, and safe for fixtures.

Required rules:

- no secrets, tokens, private keys, credentials, customer data, PII, or raw private logs;
- no absolute user-specific paths;
- no hidden network access, dependency installation, destructive commands, or global config mutation;
- no active automation or schedule creation;
- no plugin-root lifecycle config that would activate hooks on install;
- no claims that checks passed;
- no instructions that bypass sandbox or approvals;
- managed sections use `<!-- product-agent-os:start <section-id> -->` and `<!-- product-agent-os:end <section-id> -->`;
- examples use synthetic data only.

Templates may include placeholders only if the renderer replaces them deterministically before writing output. Source docs must not contain unreplaced placeholder markers or vague filler.

## Control-Plane Templates

Control-plane templates should be concise and role-oriented:

- `AGENTS.md`: durable project rules, source policy, safety boundaries, verification policy, and pointer to deeper workflow docs.
- `REQUIREMENTS.md`: goal, users, scope, non-goals, constraints, acceptance criteria, assumptions, and open questions.
- `PLAN.md`: implementation slices, ownership, dependencies, risks, rollback, verification gates, and approval needs.
- `TEST.md`: deterministic checks, manual checks, visual/runtime checks, known gaps, and evidence format.
- `EVALS.md`: subjective rubrics, LLM-as-judge checks where relevant, thresholds, artifacts, and regression notes.
- `RUNLOG.md`: current lifecycle state, decisions, commands, verification evidence, failures, risks, and handoff summary.

Existing user content must be preserved. If a file already exists and lacks a managed section, the renderer should propose a staged append or companion artifact rather than overwriting it.

## Project Config Template

Track 3 should package a `.codex/config.toml` proposal template for project-scoped Codex defaults. The renderer must stage it as `.codex/config.toml` only when the project does not already have config, or as a managed companion proposal when config exists.

The template may include:

- project-scoped `[agents]` concurrency defaults;
- model and reasoning guidance as comments or proposed values;
- sandbox and approval policy notes;
- pointers to project agent files and workflow packets.

The template must not modify global `~/.codex/config.toml`, must not add secrets, and must not enable broad network access, active automation, or external writes. Existing project config without managed markers should be classified as `leave_unchanged` plus a staged companion proposal.

## Agent Templates

Project-scoped agents live under `.codex/agents/` in the target project.

Track 3 should package templates for:

- `product-manager`
- `architect`
- `explorer`
- `builder`
- `tester`
- `reviewer`
- `docs-maintainer`
- `release-operator`

Every agent template must include:

- `name`
- `description`
- `developer_instructions`
- ownership boundary
- inputs and outputs
- stop conditions
- model/reasoning guidance
- handoff requirements

The templates should validate with the existing `validate_agents.py` wrapper.

Agent templates should align with Track 2 lifecycle packets:

- `product-manager` owns requirements, scope, non-goals, and acceptance criteria;
- `architect` owns decomposition, ownership, rollback, and risk routing;
- `explorer` owns read-only codebase and source mapping;
- `builder` owns one approved implementation slice;
- `tester` owns deterministic checks, manual checks, eval gaps, and evidence capture;
- `reviewer` owns findings-first review, missing tests, regressions, and security risk;
- `docs-maintainer` owns documentation and runlog updates;
- `release-operator` owns PR/release packet drafts and rollout notes.

## Hook Templates

Hook templates are packaged examples, not silently enabled enforcement.

Track 3 should package:

- `hooks.json`: staged lifecycle config for a target project's `.codex/hooks/hooks.json`, not plugin-root auto-activation;
- `session_start_context.py`: summarizes active control-plane state for `SessionStart`;
- `pre_tool_use_policy.py`: detects obvious destructive commands, forbidden paths, and secret-risk writes;
- `permission_request_summary.py`: formats why an approval is needed for `PermissionRequest`;
- `post_tool_use_evidence.py`: formats command evidence for a runlog buffer or staged note;
- `stop_runlog_reminder.py`: reminds the agent to update `RUNLOG.md` when evidence exists.

Hooks must not store secrets. They must not call network services. Blocking behavior must be narrow and auditable. The templates should validate with the existing `validate_hooks.py` wrapper.

The packaged plugin root must not include an active `hooks/hooks.json` that Codex would load automatically on install. Track 3 stages hook lifecycle config for the target project only, and the final response must call out that enabling hooks requires explicit approval.

## Workflow Templates

Workflow packet templates should represent repeatable manual workflows, not active automations.

Initial workflows:

- `source-context-pack.md`: official-source and Context7 research packet with source status, freshness, unsupported claims, and registry/update notes;
- `worktree-ownership.md`: worktree and write-scope map for parallel implementation;
- `build-slice.md`: one approved implementation slice with inputs, ownership, commands, evidence, and stop conditions;
- `review-slice.md`: review packet with findings-first format, missing tests, risks, and verdict;
- `release-packet.md`: PR/release preparation with checks, user impact, rollback, residual risks, and approval requirements;
- `runlog-compaction.md`: hot/warm/cold context summary and archive proposal that preserves evidence.

These workflows are warm context. They should keep `AGENTS.md` small and prevent long operational guidance from accumulating in durable rules.

## Context Archive Templates

Track 3 should stage context overflow infrastructure, not perform archival automatically.

The renderer should include proposals for:

- `.codex/runlogs/archive/` or `docs/runlogs/archive/` depending on detected project conventions;
- a `runlog-compaction.md` workflow that summarizes old iterations into decisions, failures, evidence, risks, and next actions;
- a context pack format for source notes, active constraints, current plan, and open questions.

The archive proposal must preserve raw evidence until the user approves compaction. It must not store raw private chat logs, secrets, credentials, customer data, or PII.

## Eval Templates

Eval templates should be small JSON fixtures that validate agent operating quality, not application behavior.

Initial evals:

- `project-readiness.json`: checks that generated infrastructure names required artifacts, safety boundaries, and verification gaps;
- `handoff-completeness.json`: checks that handoff packets include sources, assumptions, files, evidence, risks, and stop reason.
- `renderer-fixtures.json`: checks greenfield, existing config, missing tests, unsafe write, monorepo ownership, docs source conflict, and failed verification cases.

They should not require network access or secrets. They should be usable by future Track 4 fixture hardening.

## Automation Candidate Templates

Track 3 should include a candidate-only automation packet template under `assets/templates/automations/automation-candidate.md`.

The template must require manual stability evidence, stable inputs and outputs, owner, cadence, verification, failure modes, rollback or disable path, and explicit write policy. It must not create a schedule, recurring run, GitHub Action, Codex automation, or external workflow.

## Renderer Behavior

The renderer should support two modes:

1. `dry-run`: print JSON infrastructure plan and proposed artifact paths without writing files.
2. `stage`: render artifacts into an output directory such as `.product-agent-os/staged/` or a caller-provided staging directory.

Default behavior should be dry-run. Stage mode writes only inside the requested staging directory unless the user explicitly approves project writes.

The renderer should:

1. run or accept workspace discovery;
2. infer profile and required artifact set;
3. compare target files against existing files;
4. decide create/update/leave_unchanged/blocked actions;
5. render deterministic artifacts;
6. validate generated agents, hooks, eval JSON, and staged config;
7. detect project config conflicts, duplicate managed sections, and unmarked user-authored files;
8. return a JSON plan with warnings, questions, and approval requirements.

## Profile Routing

The profile changes depth, not lifecycle order.

| Profile | Track 3 artifacts |
| --- | --- |
| `guided-small` | control-plane files, minimal workflows, reviewer/tester agent suggestions, no automation |
| `standard-product` | control-plane files, project config proposal, core agent templates, optional hook staging, test/eval skeletons |
| `production-team` | full agent templates, worktree ownership workflow, stricter handoff and review gates |
| `ai-product` | eval templates, source-context workflow, prompt/context policy sections, regression notes |
| `enterprise-governed` | strict approval notes, forbidden paths, audit-focused hook templates, config conflict reporting |
| `autonomous-maintenance` | automation candidate packet and runlog compaction proposal only, no active schedules |

## CLI Contract

`render_infrastructure.py` should support:

```powershell
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --dry-run
python plugins\product-agent-os\scripts\render_infrastructure.py <workspace> --stage <output-dir>
```

Ожидаемое поведение:

- dry-run exits `0` with JSON when a plan can be produced;
- invalid workspace exits non-zero with a clear error;
- stage mode creates only files under the output directory;
- generated agents, hooks, eval JSON, staged config, and managed-section targets are validated before success;
- failures are reported without Python tracebacks for expected user errors.

## Safety And Approvals

Track 3 must preserve the safety model from the plugin spec:

- user-authored content outside managed sections is preserved;
- direct project writes require explicit approval;
- global config changes are forbidden;
- active automation is forbidden;
- external writes are forbidden;
- secrets are never stored or repeated;
- source-of-truth updates require staged draft first;
- generated artifacts document verification gaps instead of claiming success.
- hook lifecycle config is staged for the target project and never activated from the plugin root by default.

## Testing Strategy

Track 3 tests should be deterministic `unittest` tests:

- template registry includes all required categories and files;
- every template file exists and has no forbidden placeholders or secret-like values;
- `.codex/config.toml` proposal is staged and existing project config is preserved;
- staged `hooks.json` exists for target projects, while plugin-root hook activation is absent;
- agent templates validate with `validate_agent_file`;
- hook templates validate with `validate_hook_file`;
- dry-run produces create/update/leave_unchanged decisions for fixtures;
- stage mode writes only under the staging directory;
- existing fixture files are not overwritten;
- existing `AGENTS.md` without markers yields a staged companion proposal;
- duplicate managed sections are reported as blocked;
- rendered control-plane files include managed section markers;
- generated eval JSON is valid;
- workflow templates cover source context, worktree ownership, build slice, review slice, release packet, and runlog compaction;
- automation candidate template is candidate-only and requires manual stability evidence;
- renderer handles invalid workspace paths without traceback;
- full fixture eval still passes.

## Критерии приемки

Track 3 is complete when:

- the plugin package includes templates for control-plane files, project config, agents, hooks, workflows, evals, automation candidates, and PR/release packets;
- the renderer produces a staged infrastructure plan for every existing fixture project;
- dry-run does not write files;
- stage mode writes only to the staging directory;
- existing user-authored files are preserved;
- generated agents and hooks pass validators;
- generated eval JSON and staged config pass deterministic checks;
- existing project config, existing `AGENTS.md`, duplicate managed sections, monorepo ownership, source conflict, unsafe write, and failed verification cases are covered by tests;
- no template stores secrets or claims checks passed;
- automation remains candidate-only;
- `python -m unittest discover -s tests -p "test_*.py" -v` passes;
- `python tools\check_docs.py` passes;
- strict MkDocs build exits `0`.

## Residual Risks

Static template validation does not prove that generated infrastructure works well in every real project. Track 4 should add stronger fixture evals, failure-log based regression cases, safe merge hardening, source policy checks, automation promotion gates, and optional Agents SDK runner design.

Track 3 should not broaden into Track 4. The goal is a safe, reviewable infrastructure generator that makes the next production hardening layer possible.
