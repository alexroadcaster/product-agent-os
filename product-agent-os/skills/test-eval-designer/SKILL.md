---
name: test-eval-designer
description: Use when a Product-Agent OS plan needs deterministic tests, manual checks, eval gates, or test gap documentation before implementation or review.
---

# Test Eval Designer

## Trigger

Use this skill when a Product-Agent OS project needs test commands, eval criteria, quality gates, or explicit verification evidence requirements before implementation, review, or handoff.

## Boundaries

This is a Track 2 skill. Produce a staged `test_eval_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write `TEST.md` or `EVALS.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim test coverage, eval quality, command success, runtime behavior, or readiness without evidence from the current run.
Ask for approval before any write, external action, expanded scope, dependency installation, or operation outside the allowed workspace.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `requirements_packet` with acceptance criteria, constraints, risks, and open questions.
- `implementation_plan_packet` with slices, proposed gates, rollback notes, and ownership boundaries.
- `workspace_audit` or stack summary with available build, lint, test, docs, visual, and eval commands.
- Known test, lint, build, docs, browser, native, API, visual, or eval commands and their limits.
- Risk profile, approval limits, acceptance criteria, and required verification evidence.

## Process

1. Validate that requirements and implementation plan packets are staged and the lifecycle state is `team_ready` or equivalent pre-build handoff.
2. Map every acceptance criterion to at least one deterministic check when a suitable command exists.
3. Add manual checks only when runtime, visual, UX, device, or external-environment verification cannot be automated in the available workspace.
4. Add eval gates for AI behavior, UX judgment, documentation quality, subjective acceptance, or long-horizon quality criteria.
5. Mark missing, unavailable, unknown, or approval-gated commands as test gaps instead of inventing evidence.
6. Define thresholds, pass criteria, failure signals, artifacts to inspect, and evidence required for each check or eval gate.
7. Keep proposed artifacts staged as `TEST.md` and `EVALS.md`; do not write them directly.
8. Return `build_active` only when deterministic checks, manual checks, eval gates, thresholds, evidence, and gaps are explicit.

## Outputs

Return a test and eval packet:

```yaml
test_eval_packet:
  deterministic_checks: []
  manual_checks: []
  evals: []
  thresholds: []
  evidence_required: []
  gaps: []
  assumptions: []
  files_proposed:
    - "TEST.md"
    - "EVALS.md"
  next_lifecycle_state: "build_active"
```

## Verification

Check that each acceptance criterion maps to a deterministic check, manual check, eval gate, or explicit gap. Check that thresholds are observable, evidence is named, approval needs are flagged, and every proposed artifact remains staged. Do not claim without evidence.

## Failure Modes

- If acceptance criteria are missing, stop and route to `requirements-author`.
- If implementation slices or ownership are missing, stop and route to `implementation-planner` or `agent-team-designer`.
- If commands are unknown, record test gaps and discovery needs.
- If eval criteria are subjective but unstated, return open questions and proposed rubric fields.
- If approval is needed, stop before writes, runtime actions, or external actions.

## Final Response Contract

Return status, lifecycle state, `test_eval_packet`, files proposed, commands proposed or already evidenced, verification evidence, unsupported claims, approval requirements, risks, and the next recommended skill.
