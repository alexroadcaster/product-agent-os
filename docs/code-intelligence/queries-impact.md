# Запросы, свежесть и impact

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Web graph

[service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) требует `revision` для graph/node/impact/source; отсутствующая или несовпадающая revision даёт `GRAPH_REVISION_REQUIRED` / `GRAPH_REVISION_STALE`. Status отдельно возвращает fresh/stale/unavailable и coverage. Revision — digest manifest файлов, parser и config; snapshot находится в памяти.

Graph query фильтрует имя/путь, типы edges и соседей до depth 3. Страница по умолчанию 50, максимум 100 nodes; incident edges ограничены 100 и off-page endpoints возвращаются как contextNodes. `partial` означает, что показан не весь результат. HMAC cursor привязан к project, revision и фильтрам, с instance-random secret: после restart его сохранность не обещана.

Node impact возвращает непосредственно инцидентные edges и связанные tasks с `bounded_first_1000`, а не полный транзитивный blast radius. Source excerpt допускается лишь при fresh snapshot и проверенном file hash; по умолчанию до 2000, максимум 8000 символов и с redaction. При stale source вместо выдачи возникает `GRAPH_SOURCE_STALE`.

## Python graph-only packets

[project_graph_queries.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py) читает graph JSON/JSONL без повторного чтения source bodies. Поддерживает `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `node`, `status`, `search`, `changed_since`, `why_changed`, `agent_reading_packet`. Defaults — 25 результатов и 4000 tokens; максимумы — 250 результатов, 20 000 tokens, depth 25; hub suppression и filters ограничивают обход. Уточняйте доступные CLI flags в [scanner CLI](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/scan_project_code_graph.py).

Не смешивайте Python path/trace и Web immediate impact. Обе поверхности ограничены статической coverage и stale evidence; отсутствие результата не доказывает отсутствие вызова. При drift сначала проверяйте текущий source и выбирайте разрешённый refresh; изменения в target и provider calls не следуют из query.

Связанные тесты: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). Это маршруты проверки, а не утверждение о новом прогоне.
