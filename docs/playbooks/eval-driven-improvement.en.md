# Playbook: eval-driven improvement loop

Source status: `official + experiment`  
Sources: [Iterate on difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems), [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization), [OpenAI Cookbook](https://github.com/openai/openai-cookbook), [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses).

## Goal

Solve hard tasks through a scored improvement loop, not through a one-off prompt.

## Loop

1. Run baseline eval.
2. Identify the biggest failure mode.
3. Make one focused change.
4. Re-run eval.
5. Inspect generated artifacts.
6. Log scores and decision.
7. Continue until deterministic score and LLM-judge average meet thresholds.

## Eval matrix

| Check type | What it checks | Example |
| --- | --- | --- |
| Deterministic | Formal constraints | tests pass, lint, broken links, schema |
| LLM-as-judge | Subjective quality | usefulness, readability, visual quality |
| Artifact inspection | Real output | screenshot, report, generated page |
| Regression | Old scenarios | no previous pass regressed |

## Stopping rule

```yaml
overall_score_min: 0.90
llm_judge_average_min: 0.90
no_blocking_regressions: true
artifact_review_required: true
```

## RUNLOG rule

Each iteration must record:

- baseline or previous best;
- change made;
- score before/after;
- artifact inspected;
- bottleneck;
- next attempt.

