# Budgets и наблюдаемость LLM

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.; FUNC-G05_locally_verified_with_explicit_limits, 16.11.2026.

Владелец: runtime/LLM owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении route, prompt/output, credentials, budget или telemetry контрактов. Ссылки на тесты — маршруты проверки, не новый runtime-прогон.

## Что измеряется сейчас

Backend F11 теперь выводит versioned `paos_run_metrics_v1` из сохранённых PAOS run identities, scoped interval receipts и уникальных mediated operation IDs (`apps/local-service/src/team/metrics.mts`). Source: `paos_observed_run_receipts_v1`. Подтверждённая длительность исключает ожидание approval; open/crashed/invalid intervals оставляют полную длительность unknown и показывают только подтверждённую часть. Discussion/planning runs без задачи сохраняют bounded серверный lifecycle journal, без фиктивной задачи. Строки агентов атрибутируют pinned runs и не суммируются. Tokens, cost и полный host tool count остаются null; команды PAOS — отдельный наблюдаемый scope. Для telemetry не возвращаются и дополнительно не сохраняются prompts, argv или outputs. Числовые receipts живут с существующим run, максимум10k interval events; при более1000 matching runs или1MiB output требуется сузить период. Backend RED→GREEN проверил4s execution,2s discussion без задачи, повторы и privacy; UI/integration и local technical acceptance проверены; human acceptance отдельно.

## Лимиты по surface

| Surface | Реальное ограничение | Что оно не доказывает |
| --- | --- | --- |
| [Autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/packages/contracts/autonomy/policy.ts) / [service](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/autonomy-policy/service.mts) | maxRuns, maxCommandsPerRun, maxRunSeconds, reservations и stop-on-failed-command; default 1 run/0 commands/300 s | tokenCostMetering unavailable, hostToolsConstrained false, perFileSandbox false; concurrency=1 здесь не глобальная ёмкость scheduler |
| [Local extraction](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py) | Approval-bound budgets; default constants prompt/output 1500, latency 250 ms; max20 proposals, cost_units=0 | Локальные eval/contract значения не означают реальные billed tokens, деньги или provider SLA |
| [Provider gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_proposal_provider.py) | Проверяет budget/eval/governance payloads и submitted result evidence; gate запрещает canonical mutation | Валидный gate не расходует provider budget и не подтверждает live output/latency |

## Ошибки, восстановление и дальнейшая работа

Autonomy admission отвергает неподдерживаемые поля, включая мнимые token/cost limits; исчерпанный бюджет останавливает новые допускаемые действия, а неизвестный исход требует recovery. Это не гарантия остановки любого инструмента App host. Для внешнего вызова нужны отдельные authority, metering и evidence; они не предоставляются страницей документации.

FUNC-11 владеет versioned duration/tokens/tool calls/cost telemetry с provenance и deduplication; FUNC-15 — расширением enforceable autonomy boundaries. Денежный лимит требует достаточного metering/reservation; F11 и F15 locally verified; статусы принадлежат [матрице](../../planning/functional-remediation-2026-11-15.md). M5 и будущие provider evals также не являются результатом DG05.

Проверки: [autonomy policy](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-policy.test.mts), [autonomy runtime](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/autonomy-runtime.test.mts), [extraction eval](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_extraction.py), [provider safety](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_llm_proposal_provider.py). [Retrieval evaluation](../rag/evaluation.md) отделяет retrieval quality от answer quality; ни одна ссылка не означает свежий live benchmark.

## FUNC-F15 — лимит резервов команд

Optional maxCommandsTotal (0–64000) ограничивает durable reservations команд за текущее окно policy. Отсутствие поля сохраняет прежнее per-run поведение v1. Повтор operationId не расходует резерв повторно, неопределённый исход не возвращает резерв. Последняя допущенная команда может завершиться; новые команды/runs/resume после исчерпания запрещены. Snapshot usedCommands/commandLimit/remainingCommands — admission accounting, а не метрика выполненных команд F11. Enforcement относится только к PAOS-mediated commands всего workspace: narrow paths отклоняются, host tools не ограничены, tokens/cost limits недоступны.
