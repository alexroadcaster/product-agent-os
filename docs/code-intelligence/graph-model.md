# Модели графов и покрытие

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Матрица

| Поверхность | Языки / узлы | Связи и ограничения |
| --- | --- | --- |
| Web local service | JS/JSX/TS/TSX, включая mjs/cjs/mts/cts; file, symbol, unresolved | lexical `define`, `read`, `write`, `reference`, `call`, `import`; imports/aliases и dynamic/member calls не являются разрешёнными runtime зависимостями |
| Python plugin | file-level graph; Python AST package/module/class/function/method; JS/TS ограниченный stdlib adapter | Python import/call/test edges, JS/TS source-pattern overlay; dynamic calls и нераспознанные связи остаются uncertain/unresolved |
| Python contract overlays | Markdown и поддерживаемые форматы документации/API/schema/diagrams | Contract references и observations не доказывают полный runtime schema или API |

Web [lexical.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts) делает два прохода lexical scope, без type resolution или module linker; [parser-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) определяет parser и статусы. Web видит прочие расширения как `unsupported`, а не как выполненный анализ языков.

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) реализует Python AST и ограниченный JS/TS adapter, [project_graph_ontology.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_ontology.py) владеет типами и уверностью. Статические связи являются наблюдениями: wiring, динамический dispatch, runtime aliases и выполнение функций требуют отдельной проверки.

См. [Web API](../api/endpoints.md), [Python contract](../product-agent-os/graph-intelligence-contract.md), [adapters](adapters.md).

Связанные тесты: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). Это маршруты проверки, а не утверждение о новом прогоне.
