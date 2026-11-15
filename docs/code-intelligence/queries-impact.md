# Запросы, свежесть и impact

Source status: repository_source / static_contract_review + FUNC-31_native_admission_PoC; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Web graph

[service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/service.mts) требует `revision` для graph/node/impact/source; отсутствующая или несовпадающая revision даёт `GRAPH_REVISION_REQUIRED` / `GRAPH_REVISION_STALE`. Status отдельно возвращает fresh/stale/unavailable и coverage. Revision — digest manifest файлов, parser и config; snapshot находится в памяти.

Graph query фильтрует имя/путь, типы edges и соседей до depth 3. Страница по умолчанию 50, максимум 100 nodes; incident edges ограничены 100 и off-page endpoints возвращаются как contextNodes. `partial` означает, что показан не весь результат. HMAC cursor привязан к project, revision и фильтрам, с instance-random secret: после restart его сохранность не обещана.

Node impact возвращает непосредственно инцидентные edges и связанные tasks с `bounded_first_1000`, а не полный транзитивный blast radius. Source excerpt допускается лишь при fresh snapshot и проверенном file hash; по умолчанию до 2000, максимум 8000 символов и с redaction. При stale source вместо выдачи возникает `GRAPH_SOURCE_STALE`.

## Python graph-only packets

[project_graph_queries.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_queries.py) читает graph JSON/JSONL без повторного чтения source bodies. Поддерживает `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `read_order`, `hotspots`, `node`, `status`, `search`, `changed_since`, `why_changed`, `agent_reading_packet`. Defaults — 25 результатов и 4000 tokens; максимумы — 250 результатов, 20 000 tokens, depth 25; hub suppression и filters ограничивают обход. Уточняйте доступные CLI flags в [scanner CLI](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/scan_project_code_graph.py).

Не смешивайте Python path/trace и Web immediate impact. Обе поверхности ограничены статической coverage и stale evidence; отсутствие результата не доказывает отсутствие вызова. При drift сначала проверяйте текущий source и выбирайте разрешённый refresh; изменения в target и provider calls не следуют из query.

Связанные тесты: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). Это маршруты проверки, а не утверждение о новом прогоне.

## FUNC-31: codebase-memory-mcp — решение PoC

Решение 15.11.2026: **reject для текущего Windows workspace profile**. Это отказ от подключения проверенной сборки в данном окружении; пригодность движка на других host profiles не оценена. [Карточка F31 и текущие статусы](../planning/functional-remediation-2026-11-15.md#task-paos-func-31) владеют результатом группы и отдельной приёмкой UI-прототипа.

Проверена версия **0.12.1**, commit `a7158ac2f48ca646b4527341b76f930f2aeff87e`. Official Windows archive SHA-256 `4e4e0f16b45233af5c757a1fcbe3c3b16e9056375b1fbe2ce020b6de75dedcc0` совпал с release checksums; extracted binary SHA-256 `39f6a789cd858d7428561ac5afaefb9a47b018dcba0ad6fa41ae71a45e0ed656`. Core license — MIT; приложенные binary notices перечисляют также BSD и Apache-2.0. Проверка checksum не заменяет независимую аттестацию сборки или разрешение на redistribution. Installer, global MCP/skills/hooks/PATH, модели и credentials не использовались.

### Наблюдаемый admission gate

`--version`, `cli --help` и помощь `index_repository` выполнились. Первый daemon-backed `cli --quiet list_projects --format json` завершился с exit1 и `could not load saved runtime settings`: отдельно в sandbox и на разрешённом executor. Дополнительный вызов `index_repository --repo-path` со свежим home/cache, создаваемым самим движком, дал тот же отказ до индексирования. Cache/runtime files не появились; synthetic originals и разрешённая projection сохранили hashes. Исключённые `.env` и executable config не передавались движку.

Tag-pinned [runtime settings source](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/src/cli/runtime_settings.c) проверяет private cache ancestry до dispatch; [Windows IPC source](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/src/daemon/ipc.c) запрещает mutation-granting ACLs посторонних principals на существующих предках. Read-only ACL observation выявил такие grants на Desktop/workspace ancestors. Поэтому источник и наблюдения указывают на несовместимость ancestry текущего workspace; это **source/ACL inference**, а не внутренний diagnostic trace движка. ACL, sandbox или system policy не менялись; другие out-of-workspace cache roots не испытывались.

[Configuration](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/docs/CONFIGURATION.md) различает `CBM_CACHE_DIR` и `CBM_RUNTIME_DIR`; оба были направлены в owned disposable profile. [Bootstrap source](https://github.com/DeusData/codebase-memory-mcp/blob/v0.12.1/src/daemon/bootstrap.c) применяет runtime override ко всем endpoints; Windows named-pipe namespace включает hash runtime parent. Не использовались default rendezvous, `daemon stop`, installer/update или пользовательский daemon. Source analysis выполнили до native commands; Context7 использован для документации, а version-sensitive выводы сверены с тегом 0.12.1.

### Что проверено и что недоступно

`tests/web/poc/func-g02/codebase-memory.mts` воспроизводит credential-free preflight и fresh-cache admission probe. `node --test tests/web/poc/func-g02/codebase-memory.test.mts` — **3/3**: scoped environment, различение native rejection и executor failure, source-preservation hashes. Evidence `.tmp/func-g02/f31/result.json` содержит 12 положительных проверок целостности, отказа и сохранности; raw receipts — `preflight-sandbox.json`, `preflight-elevated.json`, `admission-rejection.json`, `acl-observation.json`.

Index/query accuracy, precision/recall, cold/incremental scan, rename/delete/branch-like changes, cancel/retry/restart, два проекта, RSS и query latency имеют статус **`not_executed_after_failed_admission`**. Их значения неизвестны; они не считаются passed или нулевыми. Передача cache SQLite движка как writable PAOS API не выполнялась.

Версионированный snapshot `paos_engine_poc_snapshot_v1` содержит `coverage=unavailable`, причину native refusal и отключённые search/definitions/references/calls/impact capabilities. Пустые nodes/edges здесь означают отсутствие измеренного результата, а не отсутствие файлов или связей. Proposed-contract fixtures в изолированном UI должны быть обозначены отдельно от фактического engine output.

Альтернатива для F14: использовать квалифицированный subset F30 для file dependencies и сохранить текущие bounded lexical JS/TS queries. Multilanguage semantic/call-path support остаётся явным design gap. Возврат к F31 требует отдельно квалифицированного host/adapter с выполненными privacy, lifecycle и benchmark gates; текущий reject не разрешает ослабить эти проверки.

Изолированная UI-приёмка: проверены F31 unavailable и отключённые query/export capabilities; отдельно помеченный symbol/call contract fixture проверяет навигацию без утверждения о measured CBM output. Общий browser22/22, model8/8; [закрытие FUNC-G02](../planning/functional-remediation-2026-11-15.md#func-g02-results).
