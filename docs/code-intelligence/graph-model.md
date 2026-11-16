# Модели графов и покрытие

Source status: repository_source / focused_f14_parser_verified + static_contract_review; 15.11.2026.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

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

## F14: проверяемые file imports и ограниченный resolver

Текущий slice от 15.11.2026 расширяет production `code-index/lexical.mts`, `parser-worker.mts` и новый `module-resolver.mts`. Исторические DG05-ссылки выше описывают прежнюю версию; F30/F31 PoC не становятся runtime dependency. Используется уже установленный публичный `rolldown/utils` parser в owned Node child; Worker остаётся отдельным focused test seam. Context7 `/rolldown/rolldown` подтвердил `parseSync`/program/errors и TS AST options; фактическая совместимость проверена установленным parser, без TS Compiler API, установки или импорта временных PoC engines.

File-level import edges строятся из AST `ImportDeclaration`, source-bearing reexports, `import('literal')` и unshadowed `require('literal')`. Relative workspace paths, cycles, type-only imports и Unicode/пробелы сохраняются. Для `require` используются существующие lexical scopes с function/import/parameter/catch/block/hoisted-var bindings, включая TypeScript constructor parameter properties. Shadowed require остаётся обычным local call. Dynamic inputs/template imports и member calls не превращаются в guessed imports. File dependency не становится cross-file symbol/call edge: импортированный symbol alias по-прежнему не доказывает runtime callee.

Resolver — чистая функция над allowlist уже admitted/indexed source paths; filesystem/package discovery отсутствует. Поддержаны bounded root-relative `baseUrl` и literal `paths` с максимум64aliases,8targets/alias,256chars/value, одним wildcard. Root wiring читает только разрешённый root `tsconfig.json` как bounded JSON, учитывает config/source hashes и передаёт `resolverConfig`/`configReasons` в parser child. `extends`, references, absolute/traversal paths, executable configs и неподдерживаемые структуры не расширяют root; relative imports остаются доступны с явным config diagnostic. Package exports/conditions, TS project references и полный TypeScript/Node module linker не заявлены.

Exact alias имеет приоритет над wildcard; для wildcard выбирается самый длинный prefix. Несколько допустимых target files, включая extension/directory ambiguity, дают `ambiguous_module`, а не произвольный выбор. Missing/unknown/bare external dependency остаётся unresolved; resolver не читает parent package.json, не запускает scripts и не возвращает файл вне allowlist. Изменение root config входит в source/revision freshness; поздние/чужие results регулирует общий publication contract.

Focused Worker ground truth `tests/fixtures/func_g02/corpus.json`: до изменения7/10 resolved imports, после10/10, precision1/recall1 на этом фиксированном корпусе. Проверка проходит также через production `createCodeIndex`: root alias wiring, config drift и hostile executable-config canary без execution. Отдельные fixtures проверяют ambiguity, unsupported config/accessors, dynamic inputs и shadowing; обнаруженный false import у TS parameter property устранён через RED/GREEN. Это качество import subset на синтетическом корпусе, не полнота всех языков или runtime call graph.

Воспроизведение: `node --test tests/web/graph-imports.test.mts`; затронутые старые regressions — `tests/web/code-index.test.mts`. Receipts: `.tmp/func-g04/f14/`; root владеет общей API/UI integration, native regression handoff и browser acceptance. Следующий артефакт — graph snapshot с compatible revision, unresolved reasons и проверкой выбранного source anchor. [Queries/impact](queries-impact.md), [адаптеры](adapters.md).

## Интеграция G04 и containment native failure

Production parser выполняется в owned Node child: minimal environment, пустой temporary cwd,128MiB JS heap, независимый ready-handshake watchdog,10s parent deadline и bounded stdin/stdout. Native stack failure остаётся внутри child; cancel ждёт close до cleanup. JS heap не является native RSS cap; child self peak RSS измеряется отдельно от service process. Focused Worker corpus tests отделены от production-child tests.

Graph status делает один F28 metadata walk без безусловного чтения source bodies; excerpt сохраняет raw SHA256 и final registry guard. Policy-revocation race сохраняет PROJECT_SCOPE_STALE. LRU8 и cursor generation позволяют девятый проект без restart. API/UI dependencies/symbols, incoming/outgoing,8-hop/1000-node path и graph/list/Mermaid используют одну revision. Source-backed DB usage показан отдельной bounded сетью код→таблица с confidence/evidence; это не угаданная архитектура или runtime call graph.
