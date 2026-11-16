# LLM budgets and observability

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.; FUNC-G05_locally_verified_with_explicit_limits, 16.11.2026.

Owner: runtime/LLM owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update with route, prompt/output, credential, budget or telemetry contracts. Test links identify verification routes, not a new runtime run.

## Current measurements

F11 backend now derives versioned `paos_run_metrics_v1` from retained PAOS run identities, scoped interval receipts and distinct mediated operation IDs (`apps/local-service/src/team/metrics.mts`). Source: `paos_observed_run_receipts_v1`. Confirmed duration excludes approval waiting; open, crashed or invalid intervals keep total duration unknown while exposing the confirmed part. Discussion/planning runs without a task retain a bounded server lifecycle journal, not a fictional task. Agent rows attribute pinned runs and are not additive. Tokens, cost and total host tool calls remain null; mediated commands are a separate observed scope. No prompts, argv or outputs are returned or newly persisted for telemetry. Numeric run receipts are retained with the existing run, at most10k interval events; metrics require a narrower period above1000 matching runs or1MiB output. Current backend RED→GREEN tests cover4s execution time,2s taskless discussion, retries and privacy; UI/integration and local technical acceptance are verified; human acceptance remains separate.

## Limits by surface

| Surface | Actual constraint | What it does not establish |
| --- | --- | --- |
| [Autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/packages/contracts/autonomy/policy.ts) / [service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/autonomy-policy/service.mts) | maxRuns, maxCommandsPerRun, maxRunSeconds, reservations and stop-on-failed-command; default 1 run/0 commands/300 s | tokenCostMetering unavailable, hostToolsConstrained false, perFileSandbox false; concurrency=1 here is not global scheduler capacity |
| [Local extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) | Approval-bound budgets; default prompt/output constants 1500, latency 250 ms; max20 proposals, cost_units=0 | Local eval/contract values are not actual billed tokens, money or provider SLA |
| [Provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py) | Validates budget/eval/governance payloads and submitted result evidence; gate forbids canonical mutation | A valid gate does not spend provider budget or establish live output/latency |

## Failure, recovery and future work

Autonomy admission rejects unsupported fields, including pretend token/cost limits; exhaustion fences newly admitted actions, while an unknown outcome requires recovery. This does not guarantee stopping every App host tool. An external call needs separate authority, metering and evidence; this documentation grants none.

FUNC-11 owns versioned duration/tokens/tool calls/cost telemetry with provenance and deduplication; FUNC-15 owns extensions to enforceable autonomy boundaries. Monetary limits require sufficient metering/reservation; F11 and F15 are locally verified; statuses are owned by the [matrix](../../planning/functional-remediation-2026-11-15.md). M5 and future provider evals are not DG05 outcomes either.

Checks: [autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-policy.test.mts), [autonomy runtime](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-runtime.test.mts), [extraction eval](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_extraction.py), [provider safety](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_proposal_provider.py). [Retrieval evaluation](../rag/evaluation.md) separates retrieval quality from answer quality; no reference establishes a fresh live benchmark.

## FUNC-F15 — command reservation cap

Optional maxCommandsTotal (0–64000) caps durable command reservations across the current policy window. Omission preserves per-run v1 behavior. Duplicate operation IDs are not charged twice, uncertain outcomes never refund reservations, and the last admitted command may finish while new commands/runs/resume are denied after exhaustion. Snapshot usedCommands/commandLimit/remainingCommands are admission accounting, not F11 executed-command metrics. Limits apply to PAOS-mediated commands over the entire workspace only; narrow paths are rejected, host tools remain unconstrained, and tokens/cost limits are unavailable.
