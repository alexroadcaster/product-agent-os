# Playbook: code review through Codex

Source status: `official + experiment`  
Sources: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex subagents](https://developers.openai.com/codex/concepts/subagents), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

## Goal

Use Codex as a reviewer that looks for bugs, regressions, test gaps, security risks and maintainability issues.

## Prompt for one agent

```text
Review current changes as a code reviewer.

Prioritize:
1. Bugs and behavioral regressions.
2. Security or data-safety risks.
3. Missing tests for changed behavior.
4. Professional coding failures that create real debt: unnecessary custom code, missing existing-capability scan, needless dependency, weak abstraction, brittle refactor or low-signal comments.
5. Maintainability issues only if they affect correctness.

Output findings first.
Each finding must include file, line, severity, and why it matters.
Do not rewrite code unless asked.
```

## Professional Coding Review

For non-mechanical code changes, the reviewer checks `.codex/workflows/coding-standards.md` and `.codex/artifact-templates/coding-standard-checklist.md` when they are present in the task packet. Findings should call out:

- custom code where delete/configuration/standard library/framework/current dependency/project helper would solve the same need;
- new dependency without `negative_dependency_rule`, rejected alternatives, compatibility and rollback/removal evidence;
- refactor that changes legacy seams without characterization tests or explicit accepted gap;
- shallow wrapper, clever abstraction or comments that restate code instead of explaining intent, invariant, risk or trade-off;
- unsupported claims such as "clean", "simple", "senior", "safe" or "minimal" without evidence.

Style-only preferences are not blockers unless they create behavioral, operational, security or maintainability risk.

## Parallel review

For larger PRs, you can explicitly ask for subagents:

```text
Use one parallel subagent per review track:
- Security risks
- Correctness bugs
- Test gaps
- Maintainability

Wait for all agents and return a consolidated review.
Do not include duplicate findings.
```

## Verification

- Check that findings refer to real files and lines.
- Request a reproduction or failing test for every high-severity bug.
- Do not accept stylistic comments as blockers without behavioral risk.
- Treat missing professional-coding evidence as a review gap, not as proof that runtime behavior was exercised.
