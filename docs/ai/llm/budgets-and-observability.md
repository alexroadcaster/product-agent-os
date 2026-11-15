# Budgets и наблюдаемость LLM

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Владелец: runtime/LLM owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении route, prompt/output, credentials, budget или telemetry контрактов. Ссылки на тесты — маршруты проверки, не новый runtime-прогон.

## Что измеряется сейчас

[Team service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts) агрегирует source `local_observed_run_start_events`, IDs и исходы запусков. Coverage partial с причинами `host_history_not_exposed` и `duration_token_cost_telemetry_unavailable`; durationSeconds/tokenCount/cost равны null. Requested model/effort в pins не заполняют observed поля. Не превращайте null в ноль, не рассчитывайте деньги по предполагаемой модели и не складывайте несопоставимые project/agent totals.

## Лимиты по surface

| Surface | Реальное ограничение | Что оно не доказывает |
| --- | --- | --- |
| [Autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/packages/contracts/autonomy/policy.ts) / [service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/autonomy-policy/service.mts) | maxRuns, maxCommandsPerRun, maxRunSeconds, reservations и stop-on-failed-command; default 1 run/0 commands/300 s | tokenCostMetering unavailable, hostToolsConstrained false, perFileSandbox false; concurrency=1 здесь не глобальная ёмкость scheduler |
| [Local extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) | Approval-bound budgets; default constants prompt/output 1500, latency 250 ms; max20 proposals, cost_units=0 | Локальные eval/contract значения не означают реальные billed tokens, деньги или provider SLA |
| [Provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py) | Проверяет budget/eval/governance payloads и submitted result evidence; gate запрещает canonical mutation | Валидный gate не расходует provider budget и не подтверждает live output/latency |

## Ошибки, восстановление и дальнейшая работа

Autonomy admission отвергает неподдерживаемые поля, включая мнимые token/cost limits; исчерпанный бюджет останавливает новые допускаемые действия, а неизвестный исход требует recovery. Это не гарантия остановки любого инструмента App host. Для внешнего вызова нужны отдельные authority, metering и evidence; они не предоставляются страницей документации.

FUNC-11 владеет versioned duration/tokens/tool calls/cost telemetry с provenance и deduplication; FUNC-15 — расширением enforceable autonomy boundaries. Денежный лимит требует достаточного metering/reservation; эти задачи [planned](../../planning/functional-remediation-2026-11-15.md). M5 и будущие provider evals также не являются результатом DG05.

Проверки: [autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-policy.test.mts), [autonomy runtime](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-runtime.test.mts), [extraction eval](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_extraction.py), [provider safety](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_proposal_provider.py). [Retrieval evaluation](../rag/evaluation.md) отделяет retrieval quality от answer quality; ни одна ссылка не означает свежий live benchmark.
