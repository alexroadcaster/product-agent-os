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
4. Maintainability issues only if they affect correctness.

Output findings first.
Each finding must include file, line, severity, and why it matters.
Do not rewrite code unless asked.
```

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

