---
name: learning-loop-maintainer
description: Use after Product-Agent OS delivery, stopped lifecycle runs, or runlog evidence reviews that need lessons, failure capture, or durable-rule candidates.
---

# Learning Loop Maintainer

## Trigger

Use this skill after Product-Agent OS delivery, after a stopped lifecycle run, or when runlog evidence needs compaction into lessons and next actions.

## Boundaries

This is a Track 2 skill. Produce a staged `learning_loop_packet` only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not edit `AGENTS.md`, `RUNLOG.md`, project files, user-level memory, external systems, or any source-of-truth artifact.
Do not claim durable-rule readiness, skill readiness, lesson validity, verification coverage, or lifecycle advancement without evidence from the current run.
Ask for approval before any write, durable-rule promotion, expanded scope, external action, dependency change, or operation outside the staged packet.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Final result or stop reason from the Product-Agent OS run.
- Runlog evidence, command results, review notes, and handoff packets.
- Failures, decisions, blocked paths, repeated gaps, and open questions.
- Review findings, reusable methods, recurring manual steps, and observed recovery actions.
- Approval constraints, source status, unsupported claims, and evidence gaps.

## Process

1. Extract decisions from evidence and keep each decision tied to the source packet, command result, or review note.
2. Separate confirmed failures from residual risks, open questions, unsupported claims, and missing context.
3. Propose durable-rule candidates only when repeated evidence supports a stable project rule.
4. Propose skill candidates only after repeated manual success, clear reuse, named inputs, named outputs, verification, and failure modes.
5. Propose runlog compaction that summarizes lessons without deleting evidence or hiding failed attempts.
6. Route stable recurring workflows to `automation-promoter` for candidate-only analysis.
7. Keep all updates staged and list approval needs before any durable artifact change.
8. Return next lifecycle state `learning_ready` only when decisions, failures, proposed compaction, candidates, and next action are explicit.

## Outputs

Return a learning loop packet:

```yaml
learning_loop_packet:
  decisions: []
  failures: []
  durable_rules_candidate: []
  skill_candidates: []
  runlog_compaction: []
  observations: []
  files_proposed:
    - "RUNLOG.md"
    - "AGENTS.md"
  next_action: ""
  next_lifecycle_state: "learning_ready"
```

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Verification

Check that every decision, failure, durable-rule candidate, skill candidate, and runlog compaction note is backed by current evidence. Confirm that proposed files remain staged, approval needs are explicit, and unsupported claims are listed instead of promoted.

## Failure Modes

- If final result or stop reason is missing, stop and request the missing lifecycle evidence.
- If runlog evidence is absent, return observations and unsupported claims only.
- If a durable rule lacks repeated evidence, keep it as an observation or open question.
- If a skill candidate lacks repeated manual success or clear reuse, keep it as a possible future method.
- If a recurring workflow appears stable, route to `automation-promoter` without creating automation.
- If approval is needed, stop before edits, promotions, external actions, or lifecycle advancement.

## Final Response Contract

Return status, lifecycle state, `learning_loop_packet`, files proposed, evidence used, unsupported claims, approval requirements, residual risks, and the next recommended skill.
