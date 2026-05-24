# Playbook: product-ready PR with Codex

Source status: `official + experiment`  
Источники: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex GitHub integration](https://developers.openai.com/codex/integrations/github), [Codex best practices](https://developers.openai.com/codex/learn/best-practices).

## Цель

Подготовить PR, который reviewer может оценить без повторного расследования.

## PR packet

```markdown
## Summary
- What changed
- Why it changed
- Product/user impact

## Verification
- Command:
- Result:
- Manual/visual QA:
- Evals:

## Risks
- ...

## Rollback
- ...

## Agent notes
- Sources:
- Assumptions:
- Follow-ups:
```

## Review gates

- Tests and evals run after final diff.
- No unresolved unsupported claims.
- No broad permissions hidden in automation.
- Risky behavior has rollback note.
- Release notes are written if user-facing behavior changes.

## Prompt

```text
Prepare this branch for a product-ready PR.

Read AGENTS.md, REQUIREMENTS.md, PLAN.md, TEST.md and RUNLOG.md.
Return:
- PR title;
- PR body;
- verification evidence;
- risks and rollback;
- release notes draft.
Do not claim tests pass unless you ran them in this turn.
```

