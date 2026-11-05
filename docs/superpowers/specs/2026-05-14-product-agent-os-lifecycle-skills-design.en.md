---
title: "Archive - Product-Agent OS Lifecycle Skills Design"
---

# Archive - Product-Agent OS Lifecycle Skills Design {#product-agent-os-lifecycle-skills-design}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official + experiment`

This design defines Track 2 for the [Product-Agent OS plugin spec](../../product-agent/product-agent-os-plugin-spec.md). It builds on the completed Track 1 core plan (`docs/superpowers/plans/2026-05-14-product-agent-os-plugin-core.md`) and focuses only on packaged lifecycle `skills`.

## Goal

Track 2 turns `product-agent-os` from a core package into a usable lifecycle guide. The plugin gains packaged `skills` that can audit a workspace, route the project lifecycle, produce staged action packets, and enforce handoff contracts without silently creating project infrastructure.

The output of Track 2 is not generated project files. The output is a set of reusable skill instructions that tell Codex how to move through the project lifecycle safely.

## Existing Foundation

Track 1 already provides:

- plugin manifest and package skeleton under `plugins/product-agent-os/`;
- lifecycle state constants and handoff validation in `contracts.py`;
- workspace discovery in `discovery.py` and `detect_project.py`;
- validators for control-plane files, agents, and hooks;
- managed Markdown merge utility;
- fixture projects and fixture eval runner;
- test package shim for `unittest discover -s tests`.

Track 2 should reuse these contracts and scripts instead of duplicating their logic inside skill bodies.

## Scope

Track 2 creates `SKILL.md` packages under `plugins/product-agent-os/skills/`:

- `project-lifecycle-orchestrator`
- `workspace-discovery-auditor`
- `requirements-author`
- `implementation-planner`
- `agent-team-designer`
- `test-eval-designer`
- `risk-reviewer`
- `pr-release-operator`
- `learning-loop-maintainer`
- `automation-promoter`

Each skill package contains:

```text
<skill-name>/
  SKILL.md
  agents/
    openai.yaml
```

The plugin package also includes shared lifecycle references:

```text
plugins/product-agent-os/skills/references/
  lifecycle-states.md
  handoff-contract.md
  source-policy.md
  complexity-routing.md
```

## Out Of Scope

Track 2 does not create `.codex/agents/*.toml`, active hooks, project templates, workflow files, automations, MCP servers, or an Agents SDK runner. It may describe proposed files in output packets, but actual generation belongs to Track 3.

Track 2 does not change global Codex config, write user-level memory, install external dependencies, use network access, or call external systems. Skills may instruct Codex to ask for approval when these actions become relevant.

## Skill Anatomy

Every `SKILL.md` must include YAML frontmatter with only:

```yaml
---
name: skill-name
description: Clear trigger description that says when to use this skill.
---
```

Every `SKILL.md` body must include these headings:

- `# <Human Skill Name>`
- `## Trigger`
- `## Boundaries`
- `## Inputs`
- `## Process`
- `## Outputs`
- `## Verification`
- `## Failure Modes`
- `## Final Response Contract`

Skill bodies should be concise. Long lifecycle, source, and routing details live in `skills/references/` and are loaded only when needed.

Every skill also has `agents/openai.yaml`:

```yaml
interface:
  display_name: "Human name"
  short_description: "Short UI description"
  default_prompt: "Use $skill-name to ..."
policy:
  allow_implicit_invocation: false
```

`allow_implicit_invocation` is false for these lifecycle skills because they handle source-sensitive project state, write planning, risk review, release packets, and automation candidates. The user or orchestrator should invoke them intentionally.

## Shared References

`lifecycle-states.md` defines lifecycle order, valid transitions, and stop conditions. It mirrors `LIFECYCLE_STATES` from `contracts.py`.

`handoff-contract.md` defines the required fields from `REQUIRED_HANDOFF_FIELDS`, including constraints, sources, evidence, file ownership, risks, next task, and stop reason.

`source-policy.md` defines source status rules: official docs are source of truth, Context7 is accepted as official only when the underlying source is official, community claims are intake material, and secrets must never be stored.

`complexity-routing.md` defines how `guided-small`, `standard-product`, `production-team`, `ai-product`, `enterprise-governed`, and `autonomous-maintenance` change depth and gates without changing lifecycle order.

## Orchestrator Contract

`project-lifecycle-orchestrator` is the entrypoint. It must:

1. Read `AGENTS.md`, existing control-plane files, `.codex/`, and Track 1 discovery output when available.
2. Determine the current lifecycle state.
3. Detect missing blockers and ask only blocking questions.
4. Select exactly one next lifecycle skill or return a stop condition.
5. Produce a staged action packet with proposed next files or questions.
6. Avoid skipping required gates.

The orchestrator cannot move from `uninitialized` directly to `build_active`. It cannot create automation, edit global config, or assert checks passed without evidence.

## Routing Rules

| Lifecycle state | Primary skill | Output |
| --- | --- | --- |
| `uninitialized` | `workspace-discovery-auditor` | read-only workspace audit packet |
| `infrastructure_planned` | `requirements-author` | requirements packet |
| `requirements_ready` | `implementation-planner` | implementation plan packet |
| `plan_ready` | `agent-team-designer` | role and ownership packet |
| `team_ready` | `test-eval-designer` | verification and eval packet |
| `build_active` | `risk-reviewer` | risk and review packet |
| `quality_gate` | `risk-reviewer` | blocking findings or clearance packet |
| `review_ready` | `pr-release-operator` | PR or release packet |
| `release_ready` | `learning-loop-maintainer` | lessons and update candidates |
| `learning_ready` | `automation-promoter` | automation candidate packet |
| `maintenance` | `project-lifecycle-orchestrator` | next maintenance route |

Complexity profile modifies depth, not order:

- `guided-small`: keep outputs lightweight; no custom agent generation.
- `standard-product`: require explicit acceptance criteria, test commands, and release notes.
- `production-team`: require ownership boundaries and reviewer handoff.
- `ai-product`: require eval criteria and prompt/context source policy.
- `enterprise-governed`: require stricter approval, forbidden paths, and audit evidence.
- `autonomous-maintenance`: require manual stability evidence before automation candidates.

## Skill Contracts

| Skill | Trigger | Required inputs | Output packet | Hard boundary |
| --- | --- | --- | --- | --- |
| `project-lifecycle-orchestrator` | User asks Product-Agent OS to guide a project or continue lifecycle | user goal, workspace path, existing control-plane files, discovery output if present | lifecycle route packet | never skip lifecycle gates |
| `workspace-discovery-auditor` | Project needs read-only audit or profile inference | workspace path, allowed read scope | workspace audit packet | no writes |
| `requirements-author` | Goal needs requirements, scope, users, acceptance criteria | audit packet, user goal, constraints | requirements packet | do not invent product decisions |
| `implementation-planner` | Requirements are stable and implementation needs decomposition | requirements packet, audit, constraints | implementation plan packet | no code changes |
| `agent-team-designer` | Work needs roles, handoffs, ownership, or parallelism | plan packet, complexity profile | agent team design packet | do not create `.codex/agents/*.toml` in Track 2 |
| `test-eval-designer` | Project needs verification or eval gates | requirements, plan, stack, risk profile | test and eval packet | do not claim checks pass |
| `risk-reviewer` | Diff, plan, or quality gate needs review | diff summary or proposed changes, requirements, verification evidence | risk review packet | findings first; no silent approval |
| `pr-release-operator` | Work is ready for PR or release packet | checks, review, runlog, rollback notes | PR or release packet | no external publish without approval |
| `learning-loop-maintainer` | Delivery completed or runlog needs compaction | final result, failures, decisions, reusable lessons | learning loop packet | no durable rule promotion without evidence |
| `automation-promoter` | Stable recurring workflow may become automation | manual success history, inputs, outputs, failure modes | automation candidate packet | no active automation creation |

## Output Packet Schemas

Skills should emit Markdown with a YAML-like packet block. The packet is a communication contract, not a machine parser requirement in Track 2.

### Lifecycle Route Packet

```yaml
lifecycle_route:
  current_state: ""
  next_state: ""
  recommended_skill: ""
  complexity_profile: ""
  blockers: []
  questions: []
  proposed_files: []
  approval_required: []
  stop_reason: ""
```

### Workspace Audit Packet

```yaml
workspace_audit:
  status: "ready_for_plan | blocked | needs_user_input"
  detected_stack: []
  existing_control_plane: []
  missing_control_plane: []
  existing_codex_assets: []
  risks: []
  complexity_profile:
    name: ""
    confidence: ""
  next_action: ""
```

### Requirements Packet

```yaml
requirements_packet:
  goal: ""
  users: []
  in_scope: []
  non_goals: []
  constraints: []
  acceptance_criteria: []
  open_questions: []
  files_proposed: ["REQUIREMENTS.md"]
```

### Implementation Plan Packet

```yaml
implementation_plan_packet:
  objective: ""
  slices: []
  ownership: []
  verification: []
  rollback: []
  risks: []
  files_proposed: ["PLAN.md"]
```

### Agent Team Design Packet

```yaml
agent_team_design_packet:
  roles: []
  ownership_boundaries: []
  handoff_requirements: []
  model_policy: []
  files_proposed: []
  track_3_candidates: []
```

### Test And Eval Packet

```yaml
test_eval_packet:
  deterministic_checks: []
  manual_checks: []
  evals: []
  thresholds: []
  evidence_required: []
  files_proposed: ["TEST.md", "EVALS.md"]
```

### Risk Review Packet

```yaml
risk_review_packet:
  findings: []
  missing_tests: []
  approval_risks: []
  source_risks: []
  verdict: "blocked | changes_requested | ready"
  next_action: ""
```

### PR Or Release Packet

```yaml
pr_release_packet:
  summary: ""
  checks_run: []
  user_impact: ""
  rollback: ""
  residual_risks: []
  approval_required: []
```

### Learning Loop Packet

```yaml
learning_loop_packet:
  decisions: []
  failures: []
  durable_rules_candidate: []
  skill_candidates: []
  runlog_compaction: []
  next_action: ""
```

### Automation Candidate Packet

```yaml
automation_candidate:
  name: ""
  purpose: ""
  trigger_or_cadence: ""
  required_inputs: []
  write_policy: "read_only | draft_only | approved_write"
  verification: []
  failure_modes: []
  owner: ""
  rollback_or_disable: ""
  readiness: "candidate_only"
```

## Safety Rules

All Track 2 skills must state:

- do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs;
- do not mutate global config;
- do not perform destructive commands;
- do not create active automations;
- do not write generated infrastructure directly in this track;
- do not claim verification passed without command evidence from the current run;
- ask for approval before external writes, permission changes, deployment, billing, auth, database, or production operations.

## Validation Strategy

Track 2 is verified with Python `unittest` tests that inspect packaged skill files and references. The tests should not execute Codex skills. They validate:

- all required skill directories and `SKILL.md` files exist;
- every skill has required frontmatter fields;
- every skill has required body headings;
- every skill has `agents/openai.yaml` with display name, short description, default prompt, and `allow_implicit_invocation: false`;
- orchestrator routing covers every lifecycle state from `contracts.py`;
- no skill claims it can perform out-of-scope writes for Track 2;
- no skill stores or asks to store secrets;
- no skill creates active automations;
- reference files exist and include lifecycle, handoff, source policy, and complexity routing content;
- references named in skill bodies resolve to existing files.

The final verification commands are:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python tools\check_docs.py
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

## Acceptance Criteria

Track 2 is complete when:

- packaged lifecycle skills exist under `plugins/product-agent-os/skills/`;
- each skill is concise and follows the common contract;
- each skill has UI metadata in `agents/openai.yaml`;
- routing covers all lifecycle states from Track 1 contracts;
- skills produce staged packets and do not silently write project infrastructure;
- tests validate structure, routing, boundaries, references, UI metadata, and source or secret policy;
- docs checks and strict MkDocs build pass.

## Self-Review

This design is intentionally limited to lifecycle skills. It does not include generated project infrastructure, project-scoped agents, hooks, active automations, or an Agents SDK runner. Those remain separate tracks so each layer can be tested and reviewed independently.
