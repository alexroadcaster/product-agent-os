---
name: project-lifecycle-orchestrator
description: Route Product-Agent OS lifecycle work to the next staged skill from current state, blockers, complexity, and evidence.
---

# Project Lifecycle Orchestrator

## Trigger

Use this skill when a Product-Agent OS project needs lifecycle routing, state recovery, next-role selection, blocker triage, or maintenance routing.

## Boundaries

This is a Track 2 skill. Produce a staged lifecycle route packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim readiness, passing checks, or lifecycle advancement without evidence from the current run.
Ask for approval before external writes, permission changes, deployment, billing, auth, database, production operations, or any action outside the current write scope.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- User goal, workspace path, and requested lifecycle action.
- Existing `AGENTS.md`, control-plane files, `.codex/` inventory, and previous packets when available.
- Discovery output from `workspace-discovery-auditor` or `plugins/product-agent-os/scripts/detect_project.py` when available.
- Current commands run, verification evidence, unsupported claims, risks, approval constraints, and complexity profile.

## Process

1. Identify the current lifecycle state from available packets, files, and evidence.
2. Check lifecycle order and stop if a required gate would be skipped.
3. Detect blocking missing inputs and ask only questions required for routing.
4. Select exactly one next skill from the route map.
5. Apply complexity depth from `guided-small`, `standard-product`, `production-team`, `ai-product`, `enterprise-governed`, or `autonomous-maintenance` without changing lifecycle order.
6. Return a staged `lifecycle_route` packet with proposed files, approval needs, blockers, and stop reason.

Route map:

| Lifecycle state | Recommended skill |
| --- | --- |
| `uninitialized` | `workspace-discovery-auditor` |
| `infrastructure_planned` | `requirements-author` |
| `requirements_ready` | `implementation-planner` |
| `plan_ready` | `agent-team-designer` |
| `team_ready` | `test-eval-designer` |
| `build_active` | `risk-reviewer` |
| `quality_gate` | `risk-reviewer` |
| `review_ready` | `pr-release-operator` |
| `release_ready` | `learning-loop-maintainer` |
| `learning_ready` | `automation-promoter` |
| `maintenance` | `project-lifecycle-orchestrator` |

## Outputs

Return a lifecycle route packet:

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

## Verification

Check that the selected route matches the route map, the state is not skipped, each readiness claim cites current evidence, and every proposed write remains staged.

## Failure Modes

- If lifecycle state is unknown, route to `workspace-discovery-auditor` for read-only audit.
- If evidence is missing, stop and list unsupported claims.
- If approval is required, stop before external writes or privileged operations.
- If the request asks for Track 3 generation, return proposed files and route details only.
- If automation is requested without manual stability evidence, route to candidate-only analysis.

## Final Response Contract

Return current state, next state, recommended skill, blockers, questions, proposed files, approval requirements, unsupported claims, risks, and stop reason.
