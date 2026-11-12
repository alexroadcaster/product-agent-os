# Product-Agent OS Web — PAOS-0019/0020/0021/0022/0027, 2026-11-12

Source status: project-authored / current local implementation evidence. Реализация и все применимые технические/docs gates завершены, пять карточек implemented; closure_level=implemented_locally_verified_app_active. Текущий результат зафиксирован в [machine results](product-agent-os-web-m2c-results-2026-11-12.json).

## Scope, baseline и ownership

Реализованы пять выбранных задач `PAOS-M2-generation-code-intelligence-search`: PAOS-0019 «Генерация по требованиям и описанию», PAOS-0020 «Индекс файлов и символов», PAOS-0021 «Граф и навигация к исходникам», PAOS-0022 «Влияние переменной и изменения», PAOS-0027 «Документы, проверки и общий поиск». Source-owned MD/JSON матрица, PRD TM-07/TM-09/TM-14, architecture graph identity contract и screens S17–S21 задают acceptance. Предыдущие21 задачи M2 сохраняют свой provenance.

Baseline: `.tmp/paos-m2c/baseline/manifest.json`,213 файлов, `2026-11-12T07:35:51.453500Z`, Git HEAD `63bb6580`; начальный worktree чистый, кроме собственного lifecycle marker. Root владеет интеграцией, UI, runtime evidence, пятью карточками и control-plane. Один canonical writer; максимум root+два агента. `/root/m2c_graph_contract` — read-only architecture/triage; `/root/m2c_graph_builder` — последовательно переданный code-index/impact slice; `/root/m2c_review` — независимый source review; `/root/m2_actual_worker` — только private consumer helpers и реальные App planning ответы. Другие51 карточка,56 estimates,12 groups/order и прежние receipts сохраняются.

Изменённые source paths и SHA-256 перечислены в соседнем JSON. Ведущие implementation paths: `apps/local-service/src/code-index/`, `impact/`, `artifacts/`, `team/skill-generation.mts`, `http/application.mts`, `runtime/app-agent-gateway.mts`; `packages/contracts/graph/code-graph.ts`, `artifacts/catalog.ts`; `apps/web/src/features/{graph,skills,artifacts}/`, shared client/App/CSS. Новые тесты переиспользуют существующие SQLite/HTTP fixtures и single-window acceptance инфраструктуру.

## Acceptance и результат

| Task | Given / When / Then и отрицательный случай | Полученное evidence |
| --- | --- | --- |
| PAOS-0019 | Закреплённые требования или описание → App planning → editable SKILL.md с requirement links → preview и отдельный Apply. Повтор не создаёт новый job/asset; недостаточные требования, недоступный App, неверный header/requirement ID и drift отклоняются | Focused10/10, actual App29, два независимо составленных proposal, explicit edit/diff/Apply/repeat |
| PAOS-0020 | Scoped workspace → rebuild → file/symbol IDs с lexical scope, namespace, location и revision. Unsupported/parse-error/dynamic/unresolved представлены явно | Graph13/13, public HTTP, stale/add/delete/root/link/oversize/cross-project fixtures |
| PAOS-0021 | Большой граф → поиск, фильтр связей, depth0–3, neighbors и страницы → bounded SVG/list, inspector и source anchor. Старые данные не выдаются за fresh | Production browser37, desktop/mobile RU/EN/light/dark, delayed-response regression RED/GREEN |
| PAOS-0022 | Одноимённые переменные в разных scopes → inspector → отдельные define/read/write/reference/call, явные task file references и matching/stale/unknown | Scope/shadowing/destructuring/switch regression fixtures, source/impact/task link в браузере |
| PAOS-0027 | Документы/checks/owner decisions → каталог, reader, outline, source anchors и общий поиск → version/time/links и отдельная acceptance. Изменение документа — staged proposal, исходник сохраняется | SQLite/API, secret/stale/retry negatives, built browser reader/proposal/search→symbol navigation |

Пять задач дают технический M2 **26/26** после финального sync. Это сумма текущих пяти, [M2b11](product-agent-os-web-m2b-execution-2026-11-12.md) и [первых10](product-agent-os-web-m2-execution-2026-11-11.md), а не повторная приёмка всех прежних сценариев или commercial release.

## Compact code-change contract и решение

- `existing_capability`: checked project identity/source handles, SQLite authority/receipts, team proposals/versioned Apply, App planning, безопасный Markdown, task references/history/search и shared authenticated client.
- `smallest_safe_patch`: отдельные доменные code-index/impact/catalog services и feature panels; skill generation использует существующий team-proposal/Apply. Вторые auth client/DB/runtime runner не вводятся.
- `invariants`: containment/root identity, запрет linked/sensitive traversal, revision/hash truth, bounded pages, exact reviewed proposal/retry/CAS, отсутствие автоматической installation/task acceptance. Граф — derived orientation, lexical AST не доказывает type/runtime semantics.
- `dependency_decision`: установленный Rolldown1.2.18 предоставляет public `rolldown/utils` parseSync. TypeScript7 установлен как native CLI без прежнего JS compiler API. Новых dependencies и изменений lockfile нет. Context7 `/rolldown/rolldown` и официальный [parse.ts](https://github.com/rolldown/rolldown/blob/main/packages/rolldown/src/utils/parse.ts) подтверждают parser API; установленный AST shape проверен локально. Документация библиотеки не является proof продукта.
- `risk_selected_tests`: meaningful HTTP404 RED для новых маршрутов, lexical oracle regressions, header/stale checks, real SQLite/HTTP, actual App planning и production browser. Setup/import/selector/flag ошибки отделены от feature RED.
- `comment_decision`: комментарии объясняют scope/parser limits, immutable revision, source trust, dedupe и proposal/acceptance границы. Нет квоты комментариев или пересказа синтаксиса.
- `performance_applicability`: файлы/bytes/nodes/edges/depth/страницы и DOM ограничены; partial/omitted показываются. Не заявляются придуманные latency/SLO.
- `evidence_and_gaps`: измерения находятся в receipts и JSON; текущая native qualification относится к exact cached pinned binary, а не к обновившемуся npm executable. App consumer обязателен; host identity attested, не cryptographic.

Bounded contexts: requirement/recommendation/proposal → team generation; file/symbol/scope/edge/revision → code-index/impact; document/check/source/acceptance → artifact catalog/reader/search. Local service контролирует source trust, SQLite — product mutations, Web — отображение и draft. Business hypothesis/PMF, новая архитектурная топология, FSD/Storybook и новый design system не требуются для этой реализации. Использованы canonical `implementation-planner` с прямыми shared references и advisory React/frontend-testing guidance; Python production implementation не менялась.

## API и поведение

Все маршруты под `/api/v1/projects/:projectId`, через существующие pairing/CSRF/authority/revision guards.

| Маршрут | Контракт |
| --- | --- |
| `POST graph/rebuild`, `GET graph/status` | Immutable derived snapshot в памяти; restart→unavailable, rebuild нужен явно |
| `GET graph`, `graph/nodes/:id`, `graph/nodes/:id/impact` | Обязательная revision; query/nodeId/depth/edgeTypes/cursor/limit; HMAC cursor привязан к проекту, revision и фильтрам |
| `GET graph/source` | Только snapshot fileId и checked fresh file; UTF-16 start/end, проверенный SHA-256; stale anchors не открываются как fresh |
| `POST team/skills/generation`, `GET team/skills/generation/:id` | requirements revision/range или bounded description; planning binding, assetKind skill, host requirement refs; stable generation key/coalescing/reuse |
| `POST team/skills/generation/:id/apply` | Редактируемый валидный SKILL.md, provenance key, reviewed previewDigest, stable Apply receipt; перед Apply требования перепроверяются |
| `GET artifacts`, `GET artifacts/:id?version=` | Документы/proposals/checks/acceptance/tasks/sessions/messages/comments и bounded graph results; version/time/coverage, stale/missing/unknown явно |
| `POST artifacts/proposals/preview`, `POST artifacts/proposals` | Version-pinned staged proposal в SQLite; исходный файл не меняется; секретный новый текст отклоняется, before-image redacted |

Index: максимум1000 source files,8MiB total,512KiB/file,25k nodes,50k edges, parser Worker10s/128MiB,150k AST nodes/depth200,8 projects, page100, neighbor depth3. Graph primary nodes/incident edges/contextNodes ограничены раздельно; dense occurrences доступны через paged impact. JS/TS/JSX/TSX lexical subset; class/JSX/type/dynamic/external aliases имеют явные ограничения. Static relative imports разрешаются только при однозначном file mapping. TypeScript type checker/runtime resolution не подменяются эвристикой.

Catalog: safe MD/TXT sources,500 sources/8MiB budget,500KiB per file; available SQLite projections, frozen cursor15min/max50 snapshots/32MiB. Host/external unavailable и first1000-task impact coverage объявлены. Check receipt сравнивается с сохранённым task revision; отсутствие пригодного pin даёт unknown. Это не полноценное доказательство freshness всех исходников. Owner acceptance хранится и показывается отдельно; check сам не переводит Task в Done.

## Проверки текущего run

| Команда / сценарий | Наблюдаемый результат | Receipt под `.tmp/paos-m2c/` |
| --- | --- | --- |
| `node --test tests/web/skill-generation-artifacts.test.mts` |10/10, skip0, exit0 | `generation-artifacts-green-5.log` |
| Graph focused builder + root full regression |13/13; входят в full suite | Builder packet и `web-full-final.log` |
| `npm run test:web-m1` |398/398, skip0,8788.3495ms, exit0 | `web-full-final.log` |
| `npm run check:web-m1` | exit0 | `backend-types-final.log` |
| `npm run build:web` | strict TypeScript + Vite,52 modules, exit0 | `ui-build-3.log` |
| `node tests/web/single-window/m2c-browser-acceptance.mts --synthetic-browser --playwright-core <installed-absolute-path> --chromium <installed-absolute-path>` |37 checks, no page errors/external requests, fixture cleaned, exit0 | `browser-evidence-829eD8/result.json` |
| `node tests/web/single-window/m2c-app-acceptance.mts --actual-app-m2c --playwright-core <installed-absolute-path> --chromium <installed-absolute-path>` |29 checks, два actual App planning jobs, no native/provider/credential operations, fixture cleaned, exit0 | `actual-app-evidence-2xi0Ih/m2c-app-result.json` |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` |1450 tests,1582.011s, OK skipped1, exit0 | `full-unittest.log` |
| `python plugins/product-agent-os/scripts/run_fixture_eval.py` |91/91, exit0 | `fixture-eval.log` |
| `python plugins/product-agent-os/scripts/run_transcript_eval.py` |26/26, exit0 | `transcript-eval.log` |
| `python plugins/product-agent-os/scripts/validate_codex_compatibility.py` | compatible, exit0; host activation остаётся отдельно | `compatibility.log` |
| Docs/lifecycle/hooks/templates pre-sync4modules |251 tests,26.062s, OK, exit0 | `docs-pre-sync.log` |

Browser plugin в доступном tool inventory отсутствовал; применён существующий installed Playwright/Chromium runner. Screenshots graph canvas/inspector и mobile canvas, а также actual skill result просмотрены root. Результаты привязаны к source/built asset hashes; предыдущий UI не маскировал проверку: отдельная prior build воспроизвела R6/R7, текущая сборка дала GREEN. Реальные App jobs вернули requirement refs `requirements:1-4` и `user-description`; worker самостоятельно прочитал catalog/schema/input и составил разные skills. Утверждения о subjective model quality, native skill activation или пользовательской приёмке не делаются.

## Независимый review, RED и исправления

`context_mode=separate_reused_context`, reviewer `/root/m2c_review`, один review window, два repair cycle. Семь P2 source findings `confirmed/fixed`, открытых source blockers нет: R1 computed keys/default RHS в destructuring; R2 switch discriminant scope; R3 cross-page edge context endpoints; R4 edited SKILL.md без header; R5 native check stale task revision; R6 Expand neighbors отправлял прежний query; R7 late source/impact response попадал в inspector другого узла. Root проверил runtime gates; source review сам их не доказывает. После review добавлен только явный Discard document draft с preview sequence guard; root self-review, browser/full checks пройдены.

Meaningful RED: `generation-artifacts-red.log` public404; `backend-review-red.log` native stale assertion; `edited-skill-header-red.log`200 вместо400; prior UI `browser-evidence-sh69Tc/result.json` обе регрессии false. Prior build metadata `ui-review-baseline.json` содержит variant hash и `source_restored=true`. Graph builder наблюдал RED для R1–R3 и передал13/13 GREEN; raw terminal packet не выдан за отдельный сохранённый лог.

Отдельно сохранены setup/harness failures: неверный bootstrap brief digest (hook отверг; исправлен собственный marker без изменения защиты); initial backend type errors; неподдерживаемый Node flag; browser selector search label mismatch; первая actual App receipt `actual-app-evidence-VcqLJA/m2c-app-result.json` — generation/edit/Apply прошли, но runner обратился к закрытому `entities?kind=run` и получил ошибку. Исправлен только runner; retry дал29 GREEN. Дополнительные negative tests сначала ошибочно ожидали null при повторном active claim и допуск secret-bearing proposal; ожидания приведены к существующему безопасному контракту. Эти ошибки не считаются feature RED. Все failed receipts сохранены.

## Exact native tuple и предел qualification

Текущий npm `codex.exe` имеет SHA-256 `6f65c42e3769209976cce097a400720b5d877e1d24ec8bb6272bf0f02d5e0fd7`, отличный от закреплённого0.167.0 `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`. Первый candidate остановился `runtime_mismatch` до sandbox commands (`native-candidate.log`), защита сохранена.

Read-only agent нашёл уже имеющийся npm cache archive0.167.0, проверил SHA-512 integrity и exact member SHA-256. Root скопировал только проверенный member в отдельный `.tmp/paos-m2c/native-cached-fixture/`; установки/сети/global repin не было. `sandbox-broker-acceptance.mts --run-once --binary <exact-fixture> --candidate-inspection` и затем default loader без candidate flag прошли три режима: bounded write, outside denial, stop/cleanup, provider/model/credential operations0. Exact receipts/hashes — соседний JSON; `qualified-manifest.json` меняет только adapterRevision и добавляет m2cNativeCandidate, прежние pins/evidence сохранены. Эти receipts квалифицируют выбранный fixture tuple, не текущую npm installation. Новые пять функций работают через local index/catalog и actual App planning без native command dependency. Более широкое native readiness для обновлённого executable потребует отдельного version qualification; нет автоматического fallback.

## Control-plane sync, preservation и остаточные границы

Финальный sync обновил пять карточек/JSON и текущие секции REQUIREMENTS/PLAN/TEST/RUNLOG через reviewed documentation-sync proposal/CAS/recovery. Большая исходная research matrix сохраняется целиком: selected card replacements имеют exact before/after recovery bytes и hash guard; другие51 карточка/все56 estimates/12 groups/order проверяются отдельно. Текущий header фиксирует26/26, старые dated receipts остаются историческими.

Canonical API/operator documentation — `apps/web/README.md`; claim/source index — `docs/sources/registry.md` и `registry.en.md`, записи WEB-M2C-TASKS-01. EVALS/AGENTS/root README/prod_test — no_change_needed: рубрики, durable instructions, общий mission и Batch39 ledger не менялись. MkDocs strict — not_applicable: nav/config/Mermaid/extensions/site/search не меняются; generated site freshness не заявляется. Обязательные final docs/checker/matrix/both-hook/diff outcomes приведены ниже; required gates не waived.

Rollback: только собственные hunks/newfiles из213-file baseline; recovery journal защищает существующие bytes и concurrent edits. Branch/stage/commit/push/PR/publication, provider/model API, real credentials, system-policy changes и внешний target не выполнялись. Managed skill не означает native installation; staged document proposal не означает source mutation. Commercial gates AUTH-G1–G6/C46-01–08, PAOS-0030, human/release acceptance, M3/T1 не закрываются этими проверками. Полная проверка lexical/type/runtime поведения всех языков и весь host history не обещаются.


## Финальный sync и проверка сохранности

Reviewed proposal digest `sha256:25322c0e074b7eb19b8c7a0d06db6dbf8edbd7761af0ce94ffb72396365c5ca3` применён существующим `sync_task_documents.py . apply ... --approved-digest ...`; recovery journal находится в `.codex/product-agent-os/compaction/`. Первая попытка получила filesystem permission denied на private writer.lock, не изменила control-plane; bounded escalation разрешила только существующий journal/lock и четыре reviewed sections. Hooks/config/rules не менялись. Полная matrix имеет отдельные exact before/after bytes и CAS recovery `.tmp/paos-m2c/matrix-recovery.json`; это recoverable coordination, не ACID. Перед proposal source/target pins проверены; более поздняя запись итоговых receipts не выдана за исходный pinned report.

После sync выполнены `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q` — **251 tests,20.753s,OK,exit0**; `python tools/check_docs.py`, `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md`, `python plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json`, тот же validator для `.codex/hooks`, `git diff --check` — **exit0**. Receipts перечислены в JSON. Git предупреждает о будущей CRLF→LF нормализации в затронутых файлах; whitespace errors отсутствуют, Git write actions не выполнялись.

Preservation receipt `.tmp/paos-m2c/preservation.json`:198/213 baseline files побайтно сохранены,15 существующих файлов изменены только в owned scope; другие51 MD cards побайтно идентичны, другие51 JSON tasks равны,56 estimates/12 groups/order неизменны. M2 technical26/26. AGENTS19008,REQUIREMENTS39441,PLAN28451,TEST31779,EVALS25030,RUNLOG25077 bytes; активные control-plane files ниже40000. Pre-existing root README48566 bytes побайтно сохранён: его общий mission не изменён, сокращение вне этого scope; oversize не скрыт как новый green budget check. Наблюдаемого нового functional tech debt по пяти карточкам нет.

Exact cached binary fixture удалён после candidate/default verification; browser/service/native workspaces cleaned, private failed receipts и recovery bytes сохранены. `tester_verdict=closed_allowed` для выбранного local technical scope. M3/T1 и commercial/human/release остаются отдельными owner gates.

После записи итогового evidence и уточнения Source status в Web README повторены affected docs/task-plan113 tests,9.278s,OK,exit0; `check_docs` и `git diff --check` также exit0. Source/build hashes остаются прежними. Измеренный интервал от baseline 2026-11-12T07:35:51.453500+00:00 до 2026-11-12T08:45:14.583362+00:00 — 4163.13s; ранняя discovery до baseline и индивидуальные активные durations задач не измерены. Полные token/tool counters после compaction недоступны и не реконструировались.
