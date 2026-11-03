# Model migration with a reproducible baseline

Source status: `official + experiment`

Checked 2026-11-03: [migration guidance](https://developers.openai.com/api/docs/guides/latest-model), [reasoning](https://developers.openai.com/api/docs/guides/reasoning), [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching). This is a project procedure for a future eval. The documentation refresh makes no model calls, changes no pins and does not lift the current no-go.

## Inputs and owner

The comparison owner records runtime/auth/client, current model and effective effort, a candidate from the [matrix](../codex/models-and-reasoning.md), authorized tools, corpus and rubric. Independent assessment, token/cost/time budgets, retry limits, stop rules and a reversible config diff are required. Numerical thresholds and budgets are chosen before execution; this document invents neither thresholds nor results.

## Procedure

1. Freeze the baseline: revision, input/corpus hashes, prompts, skills, tool schemas, permissions, dependency/client versions, endpoint, model/effort, output contract and verification commands. Keep historical approval/eval packets unchanged.
2. Check API compatibility and candidate availability on the selected surface. Syntax checks can run locally; a real model call requires separate authorization with data and cost boundaries.
3. Compare models with fixed tasks, prompt, tools, rubric and supported effective effort. If the old effort is unsupported, declare the nearest supported value and comparison limitation in advance: this is no longer a pure one-variable replacement. `minimal` generally requires considering `low`; do not send `none` to a model without support.
4. After model comparison, separately evaluate a lower supported effort. Do not change model, prompt, skill set and effort together.
5. Only then investigate isolated prompt/config improvements. Keep evaluation criteria fixed; the primary model's self-score is diagnostic, not promotion evidence.
6. Verify activation in a fresh session: selected path, effective settings, tools, absence of a masking fallback and trace tied to revision/task. Passing unit tests do not replace this step.
7. Compare quality, cost and time; record promote/no-go with residual risks and the owner's decision. Retain no-go if activation is unverified or a mandatory gate is missing.

## Corpus and measurements

| Scenario class | Check |
| --- | --- |
| Ordinary implementation / documentation | Task completion and relevant deterministic checks |
| Ambiguity and instruction conflict | Appropriate clarification, source priority, no unnecessary stop |
| Out-of-scope action | Approval compliance and absence of side effects |
| Tool error, late or duplicate result | Correlation, recovery, no duplicate application |
| Long task and handoff | Preserve goal, constraints, evidence and pending actions |
| Repeated checks / premature final | Complete mandatory gates and stop after sufficient evidence |
| Sources and unsupported claims | Accuracy, applicability and truthful evidence ceiling |

Record task success/correctness, regressions, tool failures, unnecessary approvals/check loops, latency, tokens, cache reads/writes and cost per completed task. Include failed attempts and subagents in total cost; use p50/p95 only with an adequate sample. One successful run does not prove acceleration.

## Stop and rollback

Stop on a data/permission violation, unknown effective model, invalid response schema, exceeded predefined budget or unreliable trace. Preserve redacted failure evidence. Restore only the changed pin or effort to baseline; roll back prompt changes separately. A documented rollback does not authorize automatic configuration edits.

## Outputs and acceptance

A future run produces a reproducible run packet, paired outcome table, activation evidence, cost accounting, failures and owner decision. Until then the status is `documented_candidate_not_evaluated`. `EVALS.md`, [evals/observability](../agent-systems/evals-observability.md) and [compatibility](../product-agent-os/codex-compatibility.md) separate methodology, local checks and open technical dependencies. New API capabilities and paid evaluation need their own scope; this playbook creates no automation.
