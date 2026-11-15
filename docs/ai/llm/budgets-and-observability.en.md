# LLM budgets and observability

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Owner: runtime/LLM owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update with route, prompt/output, credential, budget or telemetry contracts. Test links identify verification routes, not a new runtime run.

## Current measurements

[Team service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts) aggregates source `local_observed_run_start_events`, IDs and run outcomes. Coverage is partial with `host_history_not_exposed` and `duration_token_cost_telemetry_unavailable`; durationSeconds/tokenCount/cost are null. Requested model/effort in pins do not fill observed fields. Do not convert null to zero, calculate money from an assumed model or add incomparable project/agent totals.

## Limits by surface

| Surface | Actual constraint | What it does not establish |
| --- | --- | --- |
| [Autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/packages/contracts/autonomy/policy.ts) / [service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/autonomy-policy/service.mts) | maxRuns, maxCommandsPerRun, maxRunSeconds, reservations and stop-on-failed-command; default 1 run/0 commands/300 s | tokenCostMetering unavailable, hostToolsConstrained false, perFileSandbox false; concurrency=1 here is not global scheduler capacity |
| [Local extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) | Approval-bound budgets; default prompt/output constants 1500, latency 250 ms; max20 proposals, cost_units=0 | Local eval/contract values are not actual billed tokens, money or provider SLA |
| [Provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py) | Validates budget/eval/governance payloads and submitted result evidence; gate forbids canonical mutation | A valid gate does not spend provider budget or establish live output/latency |

## Failure, recovery and future work

Autonomy admission rejects unsupported fields, including pretend token/cost limits; exhaustion fences newly admitted actions, while an unknown outcome requires recovery. This does not guarantee stopping every App host tool. An external call needs separate authority, metering and evidence; this documentation grants none.

FUNC-11 owns versioned duration/tokens/tool calls/cost telemetry with provenance and deduplication; FUNC-15 owns extensions to enforceable autonomy boundaries. Monetary limits require sufficient metering/reservation; these tasks are [planned](../../planning/functional-remediation-2026-11-15.md). M5 and future provider evals are not DG05 outcomes either.

Checks: [autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-policy.test.mts), [autonomy runtime](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-runtime.test.mts), [extraction eval](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_extraction.py), [provider safety](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_proposal_provider.py). [Retrieval evaluation](../rag/evaluation.md) separates retrieval quality from answer quality; no reference establishes a fresh live benchmark.
