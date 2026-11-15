# LLM routes and contracts

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Owner: runtime/LLM owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update with route, prompt/output, credential, budget or telemetry contracts. Test links identify verification routes, not a new runtime run.

PAOS has two Web runtime routes and separate Python graph proposal/provider gates. An LLM name, configured model or approved gate does not prove an external call. [AI orchestration](../agents/orchestration.md) owns lifecycle; this section owns route selection and prompt/output/measurement boundaries.

| Question | Guide |
| --- | --- |
| How is a route selected and what does connected mean? | [Routes](routes.md) |
| Who builds instructions and validates results? | [Prompt/output inventory](prompts-and-outputs.md) |
| Which limits and measurements are available? | [Budgets and observability](budgets-and-observability.md) |

Primary owners: [route-selector](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/route-selector.ts), [M1 recipe](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/m1-recipe.mts), [team pins/metrics](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts), [local proposal gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py). Similar terminology does not integrate Web and Python paths.

Related contracts: [API](../../api/index.md), [backend recovery](../../backend/recovery.md), [retrieval](../rag/index.md), [code intelligence](../../code-intelligence/index.md). [FUNC-11/15](../../planning/functional-remediation-2026-11-15.md) own future metering/autonomy extensions. Provider access, answer quality and commercial readiness were not verified in this slice.
