# LLM: маршруты и контракты

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Владелец: runtime/LLM owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении route, prompt/output, credentials, budget или telemetry контрактов. Ссылки на тесты — маршруты проверки, не новый runtime-прогон.

В PAOS есть два Web runtime routes и отдельные Python graph proposal/provider gates. Имя LLM, настроенная модель или разрешённый gate не доказывают внешний вызов. [AI orchestration](../agents/orchestration.md) описывает lifecycle; этот раздел владеет выбором маршрута и prompt/output/measurement границами.

| Вопрос | Руководство |
| --- | --- |
| Как выбирается route и что означает подключение? | [Routes](routes.md) |
| Кто собирает инструкции и проверяет результат? | [Prompt/output inventory](prompts-and-outputs.md) |
| Какие лимиты и метрики реально доступны? | [Budgets и observability](budgets-and-observability.md) |

Основные владельцы: [route-selector](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/route-selector.ts), [M1 recipe](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/m1-recipe.mts), [team pins/metrics](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts), [local proposal gate](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_llm_extraction.py). Web и Python не объединяются наличием похожих терминов.

Смежные контракты: [API](../../api/index.md), [backend recovery](../../backend/recovery.md), [retrieval](../rag/index.md), [code intelligence](../../code-intelligence/index.md). [FUNC-11/15](../../planning/functional-remediation-2026-11-15.md) владеют будущими metering/autonomy расширениями. Provider access, качество ответов и коммерческая готовность этим срезом не проверены.
