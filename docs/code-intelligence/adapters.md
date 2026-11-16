# Адаптеры и будущие интеграции

Source status: repository_source / bounded_f33_backend_native_verified + static_contract_review_and_synthetic_poc; 15.11.2026.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Реализованные локальные адаптеры

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) содержит `python_ast`, `typescript_javascript_stdlib` и `unsupported_file`. Python AST строит package/symbol/import/call/test overlays, ограниченный JS/TS adapter распознаёт выбранные экспортные и импортные source patterns; для файлов больше 1 000 000 байт и generated-файлов языковой overlay не строится. `unresolved` — сохранённая неопределённость, а не подтверждённая зависимость.

Web использует отдельный [parser worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) и [lexical builder](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts); это не запуск Python adapter. Python scanner имеет staged generated artifacts, optional local indexes и отдельные approval-bound extension gates. Это разные контракты, хранилища и пределы доказательств.

## Решения PoC и будущие интеграции

| Инициатива | Статус и ожидаемая работа |
| --- | --- |
| F26–F29: Files / scan / inventory / discovery | planned: отдельная директория, управляемый scan и UI/UX |
| F30 dependency-cruiser | implemented research: bounded_adopt, только imports; production F14 planned |
| F31 codebase-memory-mcp | implemented research: reject текущего Windows profile; unavailable до index |
| F32 tbls | implemented research: reject authoritative SQLite metadata; для F33 выбрана Node alternative |
| F33/F34 | planned: карта целевой БД и связи кода с таблицами, с отображением и evidence |

Точные acceptance, licensing и integration gates принадлежат [функциональному плану](../planning/functional-remediation-2026-11-15.md). Упоминание проекта здесь не означает установку, выполнение PoC, интеграцию с Web или разрешение на подключение к реальной БД. После выполнения конкретной FUNC задачи её владелец обновляет эти страницы и source registry.

Существующие AI adapters и query-quality границы описаны в [retrieval](../ai/rag/index.md). Связанные тесты: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). Это маршруты проверки, а не утверждение о новом прогоне.

## FUNC-30 — bounded import-only PoC, locally verified

В текущем checkout проверен dependency-cruiser18.6.0 (commit59606f7133843b190aa328c95d5c676631ca45f1), MIT, Node26.5.0/Windows10.0.26200x64. Изолированная копия использует cached TypeScript5.9.2 (Apache-2.0); TypeScript7 приложения не поддерживается этой версией cruiser и не менялся. Roster44 packages: MIT/ISC/Apache-2.0; version/lock/package/compiler hashes сохранены в tool audit.

На общем synthetic corpus:10/10 expected import edges, precision1/recall1; текущий lexical parser7/10, precision1/recall0.7 (alias/dynamic/CommonJS gaps). Задания incoming-lib/alias/cycle:3/3 против2/3 baseline. Медиана трёх cold-process запусков:817.39ms против218.27ms; RSS примерно140–143MiB против104–105MiB. Дополнительные200файлов:961.49ms,146.33MiB,142302bytes. Это малый synthetic benchmark, не оценка пользовательской продуктивности или production monorepo.

Итоговое решение PoC: **bounded_adopt для file imports**, без call/definition/multilanguage/index-daemon claims. Adapter сохраняет root identity, source revision, path/line, import direction, unresolved и unknown type-only classification. Import не становится call. Source/config/secret exclusions передаются через allowlisted projection; explicit no-config и trusted tsconfig data, Node measurement process отклоняет запись и network. Original hashes сохранены; rename/parse error/timeout/retry проверены. Baseline использует прежний parser Worker отдельно от нового engine. Normalization regressions4/4; engine scenarios17 выполнены.

Артефакты: `tests/web/poc/func-g02/f30-run.mts`, `f30-model.mts`, `tests/fixtures/func_g02/protocol.json`, `corpus.json`; результаты `.tmp/func-g02/f30/result.json`, `snapshot.json`, `tool-audit.json`. Context7 [CLI no-config](https://github.com/sverweij/dependency-cruiser/blob/v18.6.0/doc/cli.md) и [pre-compilation semantics](https://github.com/sverweij/dependency-cruiser/blob/v18.6.0/doc/options-reference.md) сверены с installed source. Изолированный V3 UI прошёл общую22-browser матрицу и source/build provenance check; production integration остаётся F14. Закрытие исследования не активирует adapter в PAOS. [Закрытие FUNC-G02](../planning/functional-remediation-2026-11-15.md#func-g02-results).

## F33: production backend выбранного SQLite metadata adapter

Текущая локальная реализация находится в `apps/local-service/src/database-map/`; она переносит проверенную F32 `sqlite_metadata_v2_effective_nullable` семантику в production module без импорта PoC runner. tbls остаётся rejected. Backend требует явной регистрации offline SQLite-файла внутри registry root; source candidates остаются metadata и не открывают БД автоматически. Никакие внешние DB connections, ORM/migration execution или whole-DB copy не добавлены.

Новая F28 capability `admitDatabaseSource` отдельно применяет policy/ignore/hard deny и проверяет только100-byte SQLite header. Она не меняет generic `database_content` denial. Windows native lease закрывает path-open race: selected file и root-to-file directories удерживаются без write/delete sharing; final path, volume/file IDs и Node root/policy/stat повторно проверяются до запуска SQLite. Existing writer, sidecars или WAL header2 дают отказ. Неподдерживаемый host/lease refusal — explicit unavailable; automatic fallback отсутствует. PAOS profile DB запрещена trusted constructor path/identity guard.

Owned Node child использует fixed metadata SQL и SQLite authorizer; user rows, ATTACH, DDL, target scripts и extensions не разрешены. Views/virtual tables дают partial без expansion. Composite FK, implicit PK ordinal resolution, generated columns, effective nullable и index direction сохраняются; raw DDL/default literals не экспортируются. Child deadline5s/output512KiB, lease15s; source128MiB,200tables/4096columns/1024FK/4096index parts. JS heap/watchdog limits не являются native RSS limits.

Analyzer F27 `schema` отдаёт компактный `snapshotRevision` и source provenance, а два schema snapshots сохраняются в profile CAS namespace. Public service предоставляет status, explicit select/clear, snapshot/filter/page/scoped Mermaid и compatible changes. Metadata stale доступна только в совместимом root/policy/source envelope; fresh source bytes она не подменяет. Revoke/cancel/selection CAS блокируют позднюю публикацию. Доказательства focused native tests — `.tmp/func-g04/f33/focused-native-final.log`; isolated production UI/browser и F34 code-to-table acceptance остаются отдельными этапами. [ERD и ограничения](../db/erd.md).
