# Playbook: eval-driven improvement loop

Source status: `official + experiment`  
Источники: [Iterate on difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems), [Model optimization](https://developers.openai.com/api/docs/guides/model-optimization), [OpenAI Cookbook](https://github.com/openai/openai-cookbook), [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses).

## Цель

Решать hard tasks через scored improvement loop, а не через одноразовый prompt.

## Loop

1. Run baseline eval.
2. Identify the biggest failure mode.
3. Make one focused change.
4. Re-run eval.
5. Inspect generated artifacts.
6. Log scores and decision.
7. Continue until deterministic score and LLM-judge average meet thresholds.

## Eval matrix

| Check type | Что проверяет | Пример |
| --- | --- | --- |
| Deterministic | Формальные constraints | tests pass, lint, broken links, schema |
| LLM-as-judge | Subjective quality | usefulness, readability, visual quality |
| Artifact inspection | Реальный output | screenshot, report, generated page |
| Regression | Старые сценарии | no previous pass regressed |

## Stopping rule

```yaml
overall_score_min: 0.90
llm_judge_average_min: 0.90
no_blocking_regressions: true
artifact_review_required: true
```

## RUNLOG rule

Каждая итерация должна записывать:

- baseline or previous best;
- change made;
- score before/after;
- artifact inspected;
- bottleneck;
- next attempt.

