# AI, LLM и retrieval evals

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Владелец: AI/eval owner + verification owner. Scope/version: repository `259977f3b257ba7fc0e932396f8963262bd327ad`. Обновлять при изменении модели, маршрута, prompts, retrieval или eval contract. Рубрики и thresholds принадлежат [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/EVALS.md), выбор проверок — [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md). Ссылки ниже не означают текущего provider run.

## Выбор и сравнение

Для material AI/RAG, prompt, model, tool или routing change зафиксируйте baseline до изменения, cases и ожидаемое поведение, затем сравните candidate на сопоставимых inputs. Включите обычные, пограничные, adversarial и regression cases по риску; учитывайте privacy, tool failures, unsupported claims, quality и доступные cost/latency данные. Заморозьте значимые corpus, prompts, tools и permissions для сравнения модели; модель, effort и prompt меняйте раздельно, когда возможно. Пороги, бюджет, остановку и независимый review определяют до запуска. Неизвестные tokens/cost/latency не равны нулю.

| Слой | Что проверяет | Чего не доказывает |
| --- | --- | --- |
| [Behavioral fixture и transcript evals](../product-agent-os/behavioral-evals.md), [runner tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_transcript_session_evals.py) | Детерминированные expected/forbidden terms, структуру, маршрутизацию, privacy и fixture contracts. | Семантическую оценку всех реальных ответов, качество модели или массовую пригодность. |
| [Retrieval evaluation](../ai/rag/evaluation.md), [quality tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_project_graph_search_quality.py) | В пределах cases и thresholds — релевантность/ранжирование указателей и false positives. | Обоснованность конечного ответа, полноту реального проекта или качество live provider. |
| Provider gate / фактический provider eval | Gate проверяет подготовленные данные и условия; фактический run требует отдельных разрешений, данных, бюджета и trace. | Готовый gate, proposal или configured model не доказывают, что вызов состоялся или что выбранная модель доступна. |

Full unittest discovery уже включает fixture/transcript evals; повторно запускать тот же набор без изменения значимых входов или конкретной причины не требуется. Для отдельного fixture набора TEST указывает `run_fixture_eval.py --summary`. Фиксируйте failures и denominators, а не только агрегат. Если обязательный baseline или доступ отсутствует, остаётся `not_verified`/`blocked`, не promotion. По [LLM budgets](../ai/llm/budgets-and-observability.md) текущая наблюдаемость duration/token/cost может быть недоступна; F11/F15 и provider evaluation имеют отдельные владельцы и статус.

Источники тестов — traceability: [fixture runner](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_fixture_eval_runner.py), [provider gate](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_project_graph_embedding_provider.py). Данная страница не меняет рубрики, thresholds или authority.
