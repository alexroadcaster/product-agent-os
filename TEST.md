# TEST.md

## FUNC-G06 — закрыта, 16.11.2026

Final `node --test --test-concurrency=1 tests/web/*.test.mts`:694/694,0fail/skip (.tmp/func-g06/web-native-final.log), после home-lock reviewfix; предыдущий694/694 сохранён как web-native-pre-review.log. F21focused20/20, F22focused11/11, typecheck/buildpassed. `managed-distribution-acceptance.mts --synthetic-managed --playwright-core ABS --chromium ABS`:10/10 actualinstalledCLI/NativeLauncherIPC/service/browserA/B/A, originalfilespreserved,newSQLiteaux recorded. Nativecandidate/defaultpassed currentab195406a2f961c55d90d3a1848d4bcd98b644f10c66da7085cde94d0f584f51. Final gates: RUENmatrixvalidators, changed-sourcecheck_docs, preservation+source/package/dist/nativebindings, diffcheck. No fullPython/site/hooks/provider route: contractsunchanged. [Решения/evidence](docs/planning/functional-remediation-2026-11-15.md#func-g06-results).

## FUNC-G05 — закрыта, 16.11.2026

Shared HTTP/storage/runtime changes проверены полным native Windows synthetic набором `node --test --test-concurrency=1 tests/web/*.test.mts`:686/686,0fail/skip (.tmp/func-g05/web-native-final.log). `npm run check:web-m1` и `npm run build:web` passed. `agent-capabilities-browser-acceptance.mts --synthetic-browser --playwright-core ABSOLUTE_INSTALLED_PATH --chromium ABSOLUTE_INSTALLED_PATH`: 16/16 (.tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json). `sandbox-broker-acceptance.mts --run-once --binary ABSOLUTE_SYNTHETIC_PATH --candidate-inspection` → reviewed manifest → default passed на текущем adapter aa9c663dd1df54c6f47258234b5b9e9b5df6e0980e5ff58677e4403e30584bcc. Closure gates: RU/EN matrix validators, changed-source check_docs, preservation/source/build/native consistency, git diff --check. EVALS/Python/plugin/site/hooks/provider suites не требуются: соответствующие контракты не менялись. [Решения и evidence](docs/planning/functional-remediation-2026-11-15.md#func-g05-results).

## FUNC-G04 — закрыта, 16.11.2026

Текущий полный native synthetic run: `node --test --test-concurrency=1 tests/web/*.test.mts` —658/658,0fail/skip (.tmp/func-g04/web-closure-native-final.log). Обычный sandbox attempt631pass/16fail/3skip и owned-child stop receipt сохранены отдельно; lease/symlink отказы не выданы за product RED. `npm run check:web-m1` passed (.tmp/func-g04/typecheck-closure.log); `npm run build:web` passed (.tmp/func-g04/build-responsive-final.log), UI source/build hashes текущие по browser receipt.

`node tests/web/single-window/functional-scale-acceptance.mts --synthetic-scale --phase final` даёт три текущих completed_measurement receipts на неизменном protocol: .tmp/func-g04/scale-closure/result-diagnostic-1794778219987.json; .tmp/func-g04/scale-closure/result-reference-1794778236139.json; .tmp/func-g04/scale-closure/result-filesystem-1794778628384.json. Это measured_with_deviations/bounded_outcomes. `graph-database-browser-acceptance.mts --synthetic-browser --playwright-core ABSOLUTE_INSTALLED_PATH --chromium ABSOLUTE_INSTALLED_PATH` —18/18 (.tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json). `sandbox-broker-acceptance.mts --run-once --binary ABSOLUTE_SYNTHETIC_PATH --candidate-inspection` → local manifest → production-default run passed; current adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b. No provider/model/credentials.

Closure gates: RU/EN task validators, `python -B tools/check_docs.py --paths ...` для32 changed Markdown sources, `node .tmp/func-g04/closure-consistency.mts` и `git diff --check`. Они проверяют AC/29foreign records/groups/M5/history/source/build/native preservation. [итоговые решения и evidence](docs/planning/functional-remediation-2026-11-15.md#func-g04-results). Full Python/site/hooks/provider routes не применяются: соответствующие контракты не менялись.

## FUNC-G03 — текущая проверка, 15.11.2026

Shared HTTP/storage/runtime wiring обосновывает полный `npm run test:web-m1`:594/594,0skip на owned native synthetic environment; `npm run check:web-m1` и `npm run build:web` прошли. Focused policy-race RED/GREEN и независимый review5/5; current source-bound `project-files-browser-acceptance.mts --synthetic-browser --playwright-core ABSOLUTE_INSTALLED_PATH --chromium ABSOLUTE_INSTALLED_PATH --phase final`:19/19. `sandbox-broker-acceptance.mts --run-once --binary ABSOLUTE_SYNTHETIC_PATH --candidate-inspection` → reviewed local manifest → production-default run без candidate flag прошли write/deny/drift/interrupt. Binary был взят из проверенного существующего cache и удалён; не устанавливался.

Matrix validators RU/EN, source-docs30, MD/JSON/AC/M5 preservation и source/build/native bindings обязательны для closure; [receipts/ограничения](docs/planning/functional-remediation-2026-11-15.md#func-g03-results). Первоначальные sandbox link/rpc setup failures сохраняются; точные native retests и полный native run их не превращают в green sandbox attempt. При source drift повторить affected checks и qualification; broad plugin/site/provider suites этим runtime slice не требуются: core Python не менялся, `site/` freshness и provider/human acceptance не заявлены.

## FUNC-G02 — scoped verification routes, 15.11.2026

Combined command: `node --test tests/web/poc/func-g02/f30-model.test.mts tests/web/poc/func-g02/codebase-memory.test.mts tests/web/poc/func-g02/tbls-poc.test.mts tests/web/poc/func-g02/prototype-model.test.mts tests/web/poc/func-g02/prototype-preview.test.mts` —22/22,0skip. `node tests/web/poc/func-g02/prototype-build.mts` —TypeScript/Vite passed; `prototype-browser.mts --synthetic-browser --playwright-core ABSOLUTE_INSTALLED_PATH --chromium ABSOLUTE_INSTALLED_PATH` —22/22. Evidence `.tmp/func-g02/` source/build/harness bound; UI P2 isolation/filter regressions включены.

Engine runners `f30-run.mts`, `codebase-memory.mts`, `tbls-poc.mts` используют pinned protocol/fixtures и сохраняют реальные failure receipts. F3017 scenarios; F3112 integrity/admission/preservation observations и unknown downstream metrics; F3226 observations =23positive/3candidate defects. Node alternative effective-nullability fix6/6 и baseline-only regeneration отделены от native runs. [Полный evidence/границы](docs/planning/functional-remediation-2026-11-15.md#func-g02-results). Closure требует RU/EN matrices, source-docs, MD/JSON status/AC и preservation остальных31 records. Full Web/Python/runtime/site suites не нужны для этого PoC: production source/tuple не менялись; renderer/browser проверены локально, provider/human acceptance не заявлены.

## FUNC-G01 — текущие проверки, 15.11.2026

[Evidence/команды/provenance](docs/planning/functional-remediation-2026-11-15.md#func-g01-results), [subsystem routes](docs/testing/test-map.md#func-g01--текущие-regression-routes). Current scoped checks: `npm run check:web-m1`, `npm run build:web`; `contracts-boundaries.test.mts`, decoder/preferences и dashboard tests; `func-g01-drafts-acceptance.mts --synthetic-browser`54; `func-g01-dashboard-acceptance.mts --synthetic-browser`30; runtime-manifest/sandbox-broker12 и native candidate→promotion→production default write/deny/restart. Existing dependency/binary paths, disposable roots, no providers/real credentials.

Web507 unique: исходный full run492pass/11fixture-EPERM/4skip + exact15 elevated boundary retests15pass0skip; исходный failed receipt сохранён, не объявляется green. CSS/readability delta проверен последующим browser30/build, full suite после CSS не повторялся. Все84 browser checks имеют source/build provenance; drafts54 относятся к F08 build до dashboard-only CSS. Исторические gates ниже не расширены; сайт, Python plugin/evals/hooks не менялись и не пересобирались/перезапускались этим slice.

DG07: [operations/plugin/final integration evidence](docs/planning/documentation-architecture-2026-11-15.md#dg07-results) — `.docs-tools/reports/dg07/site`; source4, matrices2, strict build/i18n/site7, implementation-domain/8-plan HTML links, source parity, contracts/FUNC/relocation preservation. Runtime/provider/install не выполнялись; прежний verification route сохранён.

DG06: [security/testing documentation evidence](docs/planning/documentation-architecture-2026-11-15.md#dg06-results) — isolated `.docs-tools/reports/dg06/site`, source3+card parity1, matrices2, site7, HTML/source links, 11 RU/EN source sets. TEST/EVALS routes и thresholds прежние; runtime/provider/security audit не выполнялись.

## Текущий выбор проверок — 15.11.2026

DG05: [AI/LLM/retrieval/graph documentation evidence](docs/planning/documentation-architecture-2026-11-15.md#dg05-results) — isolated `.docs-tools/reports/dg05/site`, source3+card parity1, matrices2, site7, HTML/source links и source sets 20 RU/EN пар. Runtime/model/provider evals не выполнялись; linked tests — traceability.

DG04: [frontend documentation evidence](docs/planning/documentation-architecture-2026-11-15.md#dg04-results) — isolated `.docs-tools/reports/dg04/site`, source3 + translation-card regression1, matrices2, site7, HTML/source links, 15-section inventory и 6 RU/EN source sets. Приложение не менялось; новый browser/runtime/a11y прогон не заявлен.

DG03: [source/site/schema/ERD evidence и команды](docs/planning/documentation-architecture-2026-11-15.md#dg03-results) — isolated `.docs-tools/reports/dg03/site`, source3 + translation-card regression1, matrices2, site7, HTML/source links, SQL inventory и Mermaid2. Runtime suites не запускались; ссылки на них — traceability.

DG02: [source/site/diagram evidence](docs/planning/documentation-architecture-2026-11-15.md#dg02-results) — изолированный output `.docs-tools/reports/dg02/site`; source3, site7, RU/EN matrices и card parity, HTML links, Mermaid parse/render2. Verification routes ниже не расширены на product runtime.

DG01: [результаты repair](docs/planning/documentation-architecture-2026-11-15.md#dg01-results) — source/archive/site/matrix/strict build и HTML links verified; translation preservation regression находится в `docs_archive_checks.py`. Текущий маршрут ниже не расширен.

Текущая реализация маршрута и focused evidence: [scoped verification](research/product-agent-os-scoped-verification-2026-11-15.md). Для отдельного полного fixture run используйте `python -B plugins/product-agent-os/scripts/run_fixture_eval.py --summary`; после full discovery повтор не нужен.

Этот раздел — единственный владелец текущего маршрута проверок. Выбор зависит от изменённого контракта и его потребителей. Сам факт изменения Markdown, control-plane файла или шаблона не запускает общую проверку продукта. Датированные receipts, прежние списки обязательных gates и batch-specific команды ниже сохраняют provenance, но не расширяют этот маршрут.

| Тип изменения | Проверки по умолчанию | Когда расширять |
| --- | --- | --- |
| План, карточки задач, статусы | `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <changed-plan>` для матрицы; ID, допустимые статусы, зависимости, изменённые ссылки; согласованность и сохранность MD/JSON, если оба — часть контракта; `git diff --check` | Проверка machine state — только если он или его revision pins изменены. Изменение плана не требует docs/site/hooks/runtime suites. |
| Явно запрошенный MD-отчёт | Содержание, целевой путь, изменённые ссылки, сохранность существующего текста и `git diff --check` | Проверки затронутых технических примеров или схем, если они изменены. |
| Исходная документация, registry, control-plane текст | `python -B tools/check_docs.py --paths <changed-files>`; семантическая проверка затронутых утверждений, источников, переводов и ссылок; `git diff --check` | `test_product_agent_os_docs` при изменении общего контракта исходной документации; tests соответствующего workflow/config только при изменении их поведения. |
| Навигация, локализация, генератор сайта, Mermaid, extensions, search/sitemap | Изолированная strict MkDocs сборка затронутого сайта и `python -B -m unittest tests.product_agent_os.site_checks -q`, с `PAOS_DOCS_SITE_DIR` на её output | Browser/render checks — для изменённого пользовательского сценария или отображения. Старый `site/` не доказывает результат новой сборки. |
| Исторические evidence-пакеты | Проверки изменённого пакета и его ссылок | `python -B -m unittest tests.product_agent_os.docs_archive_checks -q` — при явном аудите архива/исторической целостности; не для обычной правки продукта. |
| Реализация, workflow или шаблон поведения | Воспроизводимый regression и focused tests затронутых функций/потребителей; integration — для изменённой связи; `git diff --check` | Шире только для установленного cross-cutting риска, неизвестной области влияния, release qualification или явного запроса. Зафиксировать причину расширения. |
| Разрешения, hooks, пути, секреты, пользовательские данные, миграции/восстановление | Положительные и отрицательные сценарии изменённой границы, сохранность данных и соответствующая integration; validators изменённых hook/config определений | Расширять по реальной области влияния. Изменение маршрута проверок не отменяет эти защиты и не предоставляет полномочий. |

Имена unittest-модулей в таблице находятся в `tests.product_agent_os`. Для простого плана/отчёта не нужен отдельный полный стартовый пакет, evidence-файл или синхронизация всех корневых документов. Обновляется только владелец изменившегося факта; короткий результат содержит выполненные проверки и ограничения.

### Полный прогон и повторное использование evidence

При обоснованном выборе полного Python-прогона:

```powershell
python -B -m unittest discover -s tests -p "test_*.py" -q
```

Full discovery включает fixture/transcript evals. Не запускать после него те же `run_fixture_eval.py` и `run_transcript_eval.py` повторно. Отдельный runner нужен, когда выбран именно этот набор без полного suite, либо изменились его значимые входы. CLI-контракт проверяется компактными сценариями, полный набор eval выполняется один раз. Вывод — краткий итог; подробный synthetic JSON хранить только когда он нужен для диагностики или отдельного артефакта.

Codex compatibility проверяется при изменении manifest/config/MCP/agent declaration или при квалификации совместимости; это bounded local structure, не доказательство host activation. Валидаторы hooks выполняются для изменённых определений; lifecycle/infrastructure tests — для соответствующих изменений. Strict MkDocs нужен для сайта, а не каждого Markdown-файла.

Повторять команду только после изменения кода, config, fixtures, dependencies, environment или входных данных, способного повлиять на её результат, либо для разрешения конкретного сбоя/недетерминизма. Переиспользовать receipt с исходным provenance. Доработка текста результата не требует повторять runtime/evals. Общие проверки не являются условием закрытия независимой задачи из-за несвязанного дефекта; такой дефект фиксируется отдельно без ложного green-статуса.

### Исторические результаты

Все датированные результаты ниже относятся к указанным срезам. Они не являются проверками текущего запуска и не задают обязательный набор для новой задачи. Сохранённые старые формулировки «mandatory», «обязательны» и «full gates» описывают прежний маршрут и superseded текущей таблицей.

[FUNC](docs/planning/functional-remediation-2026-11-15.md)

## MD-отчёты и чтение — 15.11.2026

Выполненный focused route: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks -q`. [Evidence и TEMP](research/product-agent-os-report-read-fix-2026-11-15.md). Новые изменения проверяются по текущей таблице выше.

## Desktop UI/UX — actual app verification

V3: npm run check:web-m1/build:web/test:web-m1; task-overlay/settings-layout, M2b/M2c ui-v3 browser matrix, accessibility core, docs unittest/check_docs/task-matrix/diff. [Команды, receipts, review и gaps](design/2026-11-13-v3/implementation-evidence.md). tests/web/single-window/v3-state-capture.mts:85 продуктовых состояний ×2 темы; captured отдельно от personally reviewed. Последние web500/V3 browser378 passed. Human acceptance отдельно.

## Automatic launch — 13.11.2026

`node --test tests/web/launch-bootstrap.test.mts tests/web/launcher.test.mts tests/web/launcher-native.test.mts`; `single-window/launch-bootstrap-acceptance.mts --synthetic-browser` с installed browser paths. Web487/native-browser28, TS/build/Python1450(skip1)/docs105/evals passed; [exact commands, failures, limits](research/product-agent-os-web-m1-execution-2026-11-11.md#запуск-без-ручного-сопряжения--2026-11-13).

Settings,13.11.2026: Settings: `node --test tests/web/settings-desktop.test.mts`8/8; full Web495/495, TS/build exit0. Native chooser4cases и actual App/browser17cases passed; exact commands/failed receipts/full gates — [owning report](research/product-agent-os-web-m1-execution-2026-11-11.md). TEMP/TMP `.tmp/paos-settings/test-temp`.

## GAP-06 acceptance и исправление проверок — 2026-11-10

GAP-06 принят владельцем; T34 и fresh-session activation отдельно открыты. Исправления locally verified: full 1450 tests (skip 1), fixtures 91/91, transcripts 26/26; актуальные проверки: [owning evidence](research/product-agent-os-audit-closeout-tooling-2026-11-10.md). Regression command: `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_fixture_eval_runner -v`; затем обязательные full/fixture/transcript/compatibility/docs gates. TEMP/TMP — `.codex-tmp/audit-closeout-2026-11-10`.

## G9 T11–T17 — принятые результаты реализации

G9 закрыта после приёмки T17; текущие docs-only checks: 131 tests, strict preview и static gates passed. Receipt — [G9 report](research/product-agent-os-g9-execution-report.md#приёмка-t17-и-закрытие-g9). Runtime/eval результаты ниже — ранее выполненные и принятые.

Полный suite: 1448 tests / 504.318s, OK (skipped=1); финальные affected/docs/lifecycle checks: 224 tests / 23.886s, OK; fixtures 91/91, transcripts 26/26, compatibility compatible, strict preview passed. Версии, команды и неуспешные попытки: [G9 execution report](research/product-agent-os-g9-execution-report.md). Использовать workspace TEMP/TMP `.codex-tmp/g9-tests/documentation-sync` и существующие полные gates; focused tests: `test_document_navigation`, `test_task_plan_lifecycle`, `test_control_plane_compaction`, `test_project_formation`.

## PAOS-AUD-G9 — принятый первоначальный пакет

Первоначальный принятый пакет T01–T10: Ran 1435 tests in 803.716s, OK (skipped=1); post-fix focused 57 OK; fixtures 91/91, transcripts 26/26; compatibility compatible; strict MkDocs isolated preview passed. [Точные команды, failed attempts, final docs/matrix checks и evidence ceiling](research/product-agent-os-g9-execution-report.md). Проверены actual process crash/recovery, source binding, preservation, conditional selection и три synthetic formation profiles. Host activation и M1 SQL runtime не доказаны.

## PAOS-AUD-G8 — verification, 2026-11-10

G8 commands: `python -B -m unittest discover -s tests -p "test_*.py" -q`; focused `test_control_plane_documents`, `test_control_plane_compaction`, `test_document_navigation`, `test_g8_control_plane`, renderer/merge/hygiene/lifecycle/state suites. Pilot packet: `python -B -m tests.product_agent_os.test_g8_control_plane --report docs/superpowers/specs/paos-aud-g8-control-plane-results.json --baseline .codex-tmp/g8-tests/g8-baseline`. Use process-local TEMP/TMP `.codex-tmp/g8-tests`; no dependencies installed. Fixture/transcript/compatibility, docs tests/checker, task matrix and diff gates remain mandatory. Strict MkDocs builds only to `.codex-tmp/g8-tests/site`. Exact outcomes and failed attempts: [execution report](research/product-agent-os-g8-execution-report.md).

Уточнение владельца 10.11.2026: подробные матрицы в `docs/planning/` сохраняются целиком, default 40k size trigger исключён; оглавления/control-plane и explicit per-file limits сохраняют ограничения. Audit matrix в `research/` остаётся целой; split отложен, прежний preview не разрешён. G8-T14 и закрытие G8 явно приняты владельцем; fresh-session activation отдельно.

## Проверки Web M1 — актуальный маршрут 2026-11-10

M5 planning-only, 13-11-2026: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -v`; `python -B tools/check_docs.py`; `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md`; `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py .`; `git diff --check`. Проверить MD/JSON M5 parity и preservation baseline `.tmp/paos-m5-plan/baseline`; receipts — `.tmp/paos-m5-plan/`. [M5 / план v0.9](docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md#paos-m5). Runtime/DB/SIWC acceptance не выполняется.

PAOS-0030: `node --test tests/web/desktop-local.test.mts`, full Web, `npm run check:web-m1`, `npm run build:web`; `m4-packaging-acceptance.mts --approved-copy-pilot` с installed Playwright/Chromium/screenshots, включая owned native Cancel. Strict MkDocs в `.tmp/paos-m4-0030/site-final` + file-link postprocess; `$env:PAOS_DOCS_SITE_DIR='.tmp/paos-m4-0030/site-final'` для docs/full Python. Full unittest/evals/compatibility/hooks/matrix/state/docs/diff по этому TEST. [Exact commands и current receipts](research/product-agent-os-web-m4-0030-execution-2026-11-12.md).

Исторический срез до PAOS-0030 (provenance сохранён): PAOS-0029: Docs: strict build в `.tmp/paos-m4-0029/site-final`, затем `tools/fix_site_i18n_links.ps1 -SiteDir .tmp/paos-m4-0029/site-final`; для unittest задать `$env:PAOS_DOCS_SITE_DIR='.tmp/paos-m4-0029/site-final'`. По умолчанию tests используют canonical `site/`; environment выбирает проверенный isolated output без его promotion. `node tests/web/accessibility/browser-acceptance.mts --synthetic-browser --scenario core|matrix|states` с `--playwright-core`, `--chromium`, `--screenshots` и проверенными absolute installed paths; full Web473, `npm run check:web-m1`, `npm run build:web`; docs105/lifecycle251, check_docs/hooks/matrix/compatibility и strict MkDocs для новой навигации. [Exact commands, failed attempts и receipts](research/product-agent-os-web-m4-0029-execution-2026-11-12.md). Backend/native unchanged; прежние runtime/Python/eval receipts сохраняют provenance.

Исторический срез до PAOS-0029 (provenance сохранён): PAOS-0028: `node --test tests/web/m4-integration.test.mts tests/web/decision-service.test.mts`; full Web473, TS/build, Python1450(skip1), fixtures/transcripts/compatibility/docs. `m2-task-manager-browser-acceptance.mts --scenario integration` и `m4-integration-acceptance.mts --synthetic-browser` / `--actual-app-integration` с exact installed paths. [Commands, failures и receipts](research/product-agent-os-web-m3-0026-execution-2026-11-12.md).

Исторический срез до PAOS-0028 (provenance сохранён): PAOS-0026: `node --test tests/web/decision-service.test.mts tests/web/decisions.test.mts tests/web/app-agent-gateway.test.mts`; full Web/TS/build; `m3-decisions-acceptance.mts --synthetic-browser` / `--actual-app-decisions` с exact fixture paths; native candidate/default и существующие Python/eval/compatibility/docs gates. [Receipts, RED и repairs](research/product-agent-os-web-m3-0026-execution-2026-11-12.md).

Исторический срез до PAOS-0026 (provenance сохранён): PAOS-0025: `node --test tests/web/recipe-recovery.test.mts tests/web/recipe-crash.test.mts`; затем full Web/TS/build, native candidate/default, `m3-recovery-acceptance.mts --synthetic-browser` / `--actual-app-recovery` с exact fixture paths, existing Python/eval/compatibility/docs gates. SIGKILL disposable host проверяет crash persistence; controlled-tick browser restart проверяет UI/native checkpoint и lost ACK. [Receipts и failures](research/product-agent-os-web-m3-0025-execution-2026-11-12.md).

Исторический срез до PAOS-0025 (provenance сохранён): PAOS-0024: `node --test tests/web/scheduler*.test.mts tests/web/parallel-workspaces.test.mts`; затем full Web/TS/build и existing Python/fixture/transcript/compatibility/docs gates. `m3-queue-acceptance.mts --synthetic-browser` проверяет UI/HTTP/native queue; `m3-queue-parallel-acceptance.mts --synthetic-queue-native` и `--actual-app-queue` проверяют concurrent native barrier, outside deny и selective Stop. Exact cached pin/disposable roots; [receipts и failures](research/product-agent-os-web-m3-0024-execution-2026-11-12.md).

Исторический срез до PAOS-0024 (provenance сохранён): PAOS-0037: `node --test tests/web/execution-recipes.test.mts tests/web/recipe-pins.test.mts tests/web/recipe-runtime.test.mts`; затем full Web, `npm run check:web-m1`, `npm run build:web` и существующие Python/fixture/transcript/compatibility/docs gates. `tests/web/single-window/m3-recipes-acceptance.mts --synthetic-browser` проверяет production UI/HTTP/native; `--actual-app-recipes` — два actual App worker steps. Exact installed paths/disposable roots обязательны. [Текущие результаты, RED/failures и limits](research/product-agent-os-web-m3-0037-execution-2026-11-12.md).

Исторический срез до PAOS-0037 (provenance сохранён): PAOS-0023: `node --test tests/web/autonomy-policy.test.mts tests/web/autonomy-runtime.test.mts`; затем `npm run test:web-m1`, `npm run check:web-m1`, `npm run build:web`. Новый `tests/web/single-window/m3-autonomy-acceptance.mts --synthetic-browser --binary <exact-pinned-path> --playwright-core <installed-path> --chromium <installed-path> --screenshots <absolute-output>` проверяет production UI/HTTP/native broker с synthetic worker, без model/provider/credentials. Narrow paths/live API opt-in fail closed; pause требует terminal ACK. [Owning evidence](research/product-agent-os-web-m3-0023-execution-2026-11-12.md) хранит команды, RED/GREEN, failed sandbox receipts и hashes. Existing Python/fixture/transcript/compatibility/docs gates обязательны.

Текущий M2: `npm run test:web-m1`, `npm run check:web-m1`, `npm run build:web`; process-local workspace TEMP/TMP. Новые runners: `tests/web/single-window/m2c-browser-acceptance.mts --synthetic-browser` и `m2c-app-acceptance.mts --actual-app-m2c`, absolute installed paths/disposable roots. [M2c evidence](research/product-agent-os-web-m2c-execution-2026-11-12.md) владеет Web398/browser37/actual App29/2jobs/Python1450 skip1/fixtures91/transcripts26, hashes/failures/native3mode receipts. Exact manifest pin обязателен; current npm runtime_mismatch, cached fixture квалифицирован без installation. [M2b](research/product-agent-os-web-m2b-execution-2026-11-12.md) сохраняет provenance; docs/lifecycle/templates/hooks/checker/matrix/diff gates обязательны; [PAOS-0046 review](research/product-agent-os-web-commercial-review-2026-11-11.md) отдельно.

Результат M1 до PAOS-0046: Актуальный follow-up 2026-11-11: `node --test tests/web/*.test.mts`306/306 skip0 (6.667s), `npm run check:web-m1`/build exit0; actual `app-broker-acceptance.mts --app-broker-browser`105, task-lifecycle-browser39, data-journeys-browser25, native default broker149162 и headless33 passed/cleaned. Current workload10k/100k/1k: search p95 278.714ms, ACK9.504ms, page28.453ms; coldGUI/event-visible/exact4core не измерены. Runtime manifest/compat6, exacttuple loader+drift fences passed. Старые geometry669/explicitfixture55 и plugin1450/91/26 имеют прежний provenance, не новый model proof. Без отдельного provider/API key; [Execution report](research/product-agent-os-web-m1-execution-2026-11-11.md) владеет commands/hashes/RED/failed receipts и AC map.

Датированный baseline 10 ноября:

Source status: local contract checks and isolated stdio observed / Web runtime qualification blocked.

[Web-план v0.8](docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md), раздел «Матрица M1 DoD», владеет соответствием acceptance → owner task. PRD §17 / architecture §21 задают M1 profile. Первый срез проверяется `node --test tests/web/*.test.mts` и `node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema`. Команда генерации схемы, observed tuple и открытые gates находятся в [evidence PAOS-0001/0054](research/product-agent-os-web-m1-initial-qualification-2026-11-10.md).

Повторная оценка без запуска процесса выполняется `node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema <stdio-receipt> [<windows-boundary-receipt>]`. Для первого stdio receipt ожидаются `project_history` и `scoped_execution_policy`. Для второго с любым из двух текущих Windows receipts ожидается `scoped_execution_policy`. Для положительной квалификации нужен совпадающий SHA-256 бинарника, подтверждённый native MXC и результат записи в корень и явного отказа для доступного до запуска внешнего контроля. [Команды, receipts и ограничения](research/product-agent-os-web-m1-initial-qualification-2026-11-10.md).

`--sqlite-fixture-root .tmp/paos-m1` добавляет rollback, восстановление SQLite-снимка и FK на синтетической файловой БД. `node --test tests/web/runtime-compatibility.test.mts tests/web/runtime-events.test.mts tests/web/runtime-sqlite.test.mts` проверяет форму протокола, разделение статусов и возможности драйвера. Эти результаты отделены от Windows write/deny и приёмки Worker/storage.

| Проверяемая граница | Задачи-владельцы и evidence |
| --- | --- |
| Manifest, policy и secrets | 0001/0054/0039/0041: exact tuple, positive/negative contracts, credential isolation |
| Сессия, permissions, Stop, recovery | 0042/0043/0044/0055: SW-AC и UX-AC, duplicate/cleared/outcome; fixture отдельно от actual runtime |
| SQLite, FTS5 и данные | 0048/0049/0050/0051/0056: ST-AC и DATA-AC, conflicts/crash, restore rehearsal до switch, no lost deltas |
| UI и сквозная приёмка | 0004/0043/0045: M1 RU/EN, обе темы, a11y; real runtime + browser journey при закрытом Codex App по утверждённой матрице |

Live/provider/browser actions требуют применимой отдельной authority; их отсутствие — явный открытый gate, а не условный pass. Исторические проверки других направлений ниже не подтверждают Web M1. Текущие maintenance receipts: [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md).

Прежние evidence refs: [source](research/product-agent-os-web-m2-execution-2026-11-11.md).

## PAOS-AUD-G7 — current-run verification, 2026-11-10

T08 docs/acceptance-only: reuse unchanged T07 runtime suite; current frozen hashes verified. Current docs unittest 105 tests / 13.036 s; check_docs, matrix/state validators and diff check exit 0. Final acceptance edits checked below in execution report.

T07: full unittest 1379 / 516.855 s / exit 0 (1 platform skip); docs 105 / 7.834 s, fixture 91/91, transcript 26/26, compatibility passed. Exact commands, RED/GREEN и attempts — [execution report](research/product-agent-os-g7-execution-report-2026-11-09.md). TEMP/TMP: workspace `.docs-tools/reports/g7-deep-review-temp`. Attested comparison 12 admitted; oracle 6/6 на arm. Offline rescore hash-guards inputs, provider=0, published writes=0. T06 10/10 tool cases — прежний receipt, в этом T07 не повторялся.

## PAOS-AUD-G6 — 2026-11-09

G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; все три synthetic local pilots приняты владельцем. HOST-01 не является их зависимостью. T34 no-go и fresh-session activation HOST-01/HOST-02 остаются открытыми отдельно; manual_only сохраняется. [Результаты](docs/superpowers/specs/paos-aud-g6-pilot-results.json).

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G5 — 2026-11-09

G5: 105 docs tests passed; check_docs, README CLI dry-run, compatibility и strict MkDocs exit 0; 368 HTML / 220 routes без link/anchor/search gaps; 93/93 Mermaid renders. Команды, RED/GREEN, retries и final logs — owning evidence и .docs-tools/reports/paos-aud-g5/. Installer tests используют stubs, не установку.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G4 — 2026-11-09

Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only. Failed attempts и measurement provenance — owning plan. Final docs/matrix/consistency/diff checks обязательны после closure edits.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G3 — 2026-11-09

PAOS-AUD-G3: Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only). Current pointer только в PLAN.md; mismatch запрещает fallback. Source-policy needs_review не равен failed parser test. Failed attempts, UTC fixture correction, final checks и provenance — owning evidence.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G2 — 2026-11-09

PAOS-AUD-G2: full discovery 1305 tests, 748.949 s, OK (skipped=1), exit 0; final affected+docs 122 passed, после refactor final contracts 22 passed; fixture 91/91, transcript 26/26; compatibility exit 0, local structure only. Docs checker, hook validators и diff check passed. Проверять malformed/duplicate MCP, precedence, IDE unsupported conflict, unknown/old/version-surface, model mismatch, cache drift и read-only CLI; TEMP/TMP под ignored .docs-tools/reports/paos-aud-g2. Точные результаты и failed attempts — owning evidence.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G1 — 2026-11-09

PAOS-AUD-G1: full discovery 1297 tests, 532.640 s, OK (skipped=1), exit 0; affected suite 216 tests passed; final merge/renderer 67 tests passed после последнего alias-hardening. Fixture 91/91, transcript 26/26, docs 100/100; hook validators, parity/AST и native rules checks passed. Compatibility exit 1 needs_review — существующий G2/F01 legacy MCP gap. Даты, команды, failed attempts и provenance — owning evidence. Для повторения использовать ignored workspace TEMP/TMP под .docs-tools/reports/paos-aud-g1/tmp и PYTHONDONTWRITEBYTECODE=1; прежние TEMP cleanup failures не скрыты.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## Session lifecycle regression — 2026-11-09

`PAOS-SESSION-LIFECYCLE-2026-11-09`: run `python -m unittest tests.product_agent_os.test_lifecycle_hooks -v` for two-chat isolation, invalid/foreign identity, exact bootstrap, Windows case handling and SessionStart/Stop agreement, then required docs/template and plugin suites below. Current receipts: full discovery 1288 tests, one skip, exit 0; final affected suite 236 passed; fixture 91/91, transcript 26/26; hook validators/docs/diff passed. Compatibility exit 1 remains the existing legacy MCP gap. Exact state provenance and current-host versus synthetic evidence: `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`. No trust or sandbox bypass is part of verification.

## Ordinary route integration — 2026-11-05

`PAOS-ORD-01-06-2026-11-05`: verify public contract and infrastructure CLIs, malformed/unknown/stale task inputs, RU/EN/no-builder parity, sensitive Windows paths, mandatory project checks, approval/source-policy guards, isolated RED/GREEN behavior and target-file preservation. Commands and current receipts: [owning plan](docs/planning/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md). Final integrated verification passed: 1272 tests, 753.848s, OK (skipped=1), exit 0; fixture 91, transcript 26/26, compatibility and docs gates passed. Run the full unittest suite, fixture/transcript evals, compatibility validator, docs tests, docs checker and diff check. This slice uses an isolated TEMP and `PYTHONDONTWRITEBYTECODE=1`; sandbox TEMP failures are setup failures, not behavior evidence. Strict MkDocs output is isolated under `.docs-tools/reports/ordinary-route-preview`; root `site/` remains the earlier documentation build. Host activation and provider/model comparisons are separate gates.

## Documentation site refresh — 2026-11-05

For `PAOS-SITE-DOCS-REFRESH-2026-11-05`, run docs unittest and check_docs.py, approved strict MkDocs, existing `tools/fix_site_i18n_links.ps1`, then route/link/anchor/search checks, offline Mermaid parse/render and git diff --check. Run site-dependent docs tests after the build and postprocessing, not concurrently. Preserve plugin/tools/tests/config hashes. Evidence: `docs/superpowers/specs/site-docs-refresh-2026-11-05.json`. Observed: 100 docs tests passed; check_docs.py, strict build, 220 routes, all internal links/anchors/search routes and 93 Mermaid renders passed. Local RU/EN search and representative desktop/mobile pages checked. No runtime or hosted activation claim.


<!-- product-agent-os:start test -->
Project: Codex Docs / Product-Agent OS
Last compacted: 2026-07-07

## Purpose

`TEST.md` is the compact verification routing layer. It defines current checks, escalation boundaries and evidence owners. Detailed historical command logs and batch-specific command archives belong in [current control-plane state](docs/product-agent-os/control-plane-current-state.md), source backlogs, evidence packets and `prod_test.md`.

## Required Checks After Docs Or Control-Plane Changes

Текущий маршрут — таблица в начале `TEST.md`: изменённые источники отдельно от сайта, lifecycle/hooks/infrastructure только при изменении соответствующего контракта. Этот исторический anchor сохранён для ссылок; общего обязательного списка для любого control-plane edit больше нет.

Compatibility gate after PAOS-AUD-G2: `validate_codex_compatibility.py` exits 0 for the checked-in wrapped MCP declaration. This proves bounded local structure only; distribution remains gated and host diagnostics remain separate. Legacy flat, ambiguous and malformed inputs must still fail closed. Dated earlier needs_review receipts remain historical evidence, not current status.

## Required Checks After Plugin Or Runtime Changes

Начать с regression и затронутых integration checks из текущей таблицы. Full discovery — обоснованное расширение, а не обязательное продолжение каждого focused прогона. Если он выбран, не повторять fixture/transcript evals отдельно. Для долгого запуска использовать асинхронный tool session и короткие проверки результата, чтобы сохранять связь с пользователем.

## Current Verification State

Исторические записи и результаты ниже относятся к указанным срезам. Они не меняют очередь Web M1 и не являются проверками текущего запуска. При расхождении используются текущие owning artifacts; перенос истории не закрывает оставшиеся gates.


| Area | Current evidence state | Required next check |
| --- | --- | --- |
| Batch 35 `T10-LIVE-M41` | Closed as `owner_closed_no_op_git_release_pr`; no git writes occurred. | Fresh git preflight and exact approval before any future git write. |
| Batch 38 cache/readiness | `B38-S2` records `plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage`; historical `blocked_pending_explicit_cache_mutation_approval` remains preserved. | Treat as historical unless a new cache mutation is requested. |
| Batch 39 | `B39-S1` through `B39-S5` are source-owned; S5 is `closed_for_owner_feedback_testing_not_release_ready`. | Use `prod_test.md`, S5 packets, focused tests, full unittest, fixture/transcript eval, Codex compatibility, docs check and diff hygiene before stronger claims. |
| Batch 41 | S9 modernization and Neural_Flow comparison are generated-artifact evidence. | Use focused first-run/cockpit renderer tests and docs checks; browser/Cosmos.gl/WebGL/target-apply proof requires approval. |
| Batch 42 | Historical planned-only snapshot plus GAP-03 local inventory/metadata/routing evidence in current_execution. | M04 explicit-only decision and four metadata corrections are locally verified; M06 fresh-host evidence remains open; no fixed-auto-engagement claim. |
| Batch 44 | Self-Learning Loop S0-S7 are local/staged/manual evidence. | Run focused state/extensions/docs tests before S8 decision; no automation claim without owner approval and activation proof. |
| Batch 45 | A04-A06 locally implement/focused-verify T23-T29. T28: families 34 (limit 98), exceptions 3 (limit 10), combined test LOC 5658 (<8130 baseline), focused route 48/48. T29/promotion: 23/23. | Local contracts only; T30-T33, live/CLI/provider/external reviewer/model behavior/promotion and T34 exact approval remain open. |
| Track 11 DOC-M25 | Root `site`, search and sitemap freshness are source-owned by DOC-M25 packet. | Root site freshness checks prove generated site/search/sitemap only; browser proof and broad scans remain separate. |
| GPT-5.6 `.codex` remediation | R1-R6 current evidence: agent validator 15/15 with zero config errors; focused contracts 184 OK; docs 100 OK; hooks 19 OK plus both hook validators; strict doctor 0 fail; fixture eval exit 0; transcript eval 26/26; compatibility `compatible`; full discovery 1195 OK with 1 skip; docs structure OK. Source: `docs/planning/2026-08-05-gpt56-r1-r6-remediation.md`. | Maintain final diff/task-plan hygiene. Separately restart Codex for fresh MCP/`SessionStart` activation proof and run same-effort/one-lower-effort behavioral comparisons before promotion. |
| Lifecycle hooks / `B45-S9-H01` | Focused lifecycle/template suite 121/121 OK; both hook validators OK; docs 100/100 and checker OK; fixture eval exit 0; transcript eval 26/26; compatibility `compatible`. Broad discovery ran 1199 tests with one `Source status` formatting failure in the existing Batch 45 plan; the marker was corrected and the exact source-policy regression test reran green. Direct five-run script timing is diagnostic only: read fast path averaged 93.5 ms and current-file advisory 110.7 ms. | Use `/hooks` to review and trust changed hashes, then start a fresh task to collect real hook-runtime latency/activation evidence. Do not treat direct script timing as Codex App hook activation proof. |

## Batch-Specific Check Routes

| Batch or route | Compact check route | Evidence owner |
| --- | --- | --- |
| Batch 39 | `prod_test.md` attempt ledger, focused schema/collector/dashboard/route tests, fixture eval, transcript eval, Codex compatibility, docs check, diff hygiene. | `prod_test.md`; B39 packets. |
| Batch 44 | `python -m unittest tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_self_learning_extensions -v`, staged initializer/runner/export checks as scoped by packet, docs check, diff hygiene. | B44 packets; `docs/product-agent-os/self-learning-loop.md`. |
| Batch 45 Professional Code Authoring | Focused `test_comment_sufficiency`, `test_batch45_s3_professional_code_authoring`, `test_coding_standards_artifacts`, automation/self-learning tests where touched, docs check, diff hygiene. | B45 packets; `docs/product-agent-os/coding-standards.md`. |
| Batch 45 retest/post-Q4 | `python -m json.tool` for changed B45 packets, including `docs\superpowers\specs\batch45-postq4-t17-frozen-heldout-corpus.json`, `docs\superpowers\specs\batch45-postq4-t18-promotion-grade-eval-design.json`, `docs\superpowers\specs\batch45-postq4-t19-cost-timeout-retention-policy.json`, `docs\superpowers\specs\batch45-postq4-t20-promotion-grade-eval-approval-packet.json`, `docs\superpowers\specs\batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json`, `docs\superpowers\specs\batch45-postq4-t21-promotion-grade-eval-results.json` and `docs\superpowers\specs\batch45-postq4-t22-promotion-grade-decision-packet.json`, `python -m unittest tests.product_agent_os.test_codex_runtime_runner_model_output -v`, `python -m unittest tests.product_agent_os.test_coding_standards_artifacts -v`, docs check, diff hygiene. | Q0-Q4 and T01-T22 packets. |
| Batch 45 code-quality runtime recovery | T28 semantic/seeded-fault route 48/48; T29/promotion route 23/23; execution-loop/report route 7/7; final affected-contract route 208/208; Product-Agent OS docs 100/100; strict MkDocs build exit 0 with 652 generated files restored. | Task-group owns machine status; plans own detail; RUNLOG owns evidence; TEST owns ceiling. Hook activation remains a clean-session gap. |
| Track 11 docs toolchain | Project-local `.venv-docs`, `.docs-tools/node`, `.docs-tools/bin`, `.docs-tools/reports`, `docs/assets/javascripts/vendor` checks only within approved scopes. | Track 11 plan and DOC-M34..DOC-M41 packets. |

## Control-Plane Size Budgets

По `.codex/workflows/control-plane-sync.md`, default compactness target — 40 000 UTF-8 bytes с warning от 32 000. Это advisory и отдельная hygiene-задача, а не блокировка небольшой правки. Explicit per-file hard limits и реальные технические ограничения загрузки сохраняются. Перенос истории требует сохранения исходного evidence, проверки ссылок и защиты от concurrent edits; автоматически удалять/суммировать историю нельзя. Прежний 50 KiB guard superseded.

## MkDocs Runtime Location

Use the project-local docs runtime for current docs checks:

```powershell
.venv-docs\Scripts\python.exe -m mkdocs --version
.venv-docs\Scripts\python.exe -m mkdocs build --strict
```

The default `python` may not have MkDocs installed. Historical fallback paths such as `C:\tmp\codex_docs_mkdocs` or `tmp\mkdocs_deps_b40s4` are historical evidence only.

## Runtime And External-Action Verification Boundaries

Действующее разрешение, включая bounded standing authorization из `AGENTS.md`, требуется для:

- target workspace mutation;
- browser automation;
- provider/API calls;
- live server or dashboard launch;
- canonical graph-source mutation;
- git branch creation/switching, stage, commit, push, tag or PR;
- publication, deployment or external automation creation.

Approval for one surface does not authorize another. Runtime launch approval does not authorize browser automation; browser approval does not authorize provider calls; provider-call approval does not authorize canonical mutation or git/release actions. Не спрашивать повторно для действия в уже разрешённых границах. Managed sandbox, tool approvals и project trust сохраняют силу; эта таблица их не расширяет.

For real-project target tests, the default verification mode is read-only: inventory, route classification, source-policy status, control-plane presence, safe artifact maps, counts, digests and redacted summaries.

## Historical Evidence Owners

| Marker | Evidence owner |
| --- | --- |
| `T10-LIVE-M41`, `owner_closed_no_op_git_release_pr` | `docs/planning/product-agent-os-track-10-backlog.md`, `docs/sources/product-agent-os-batch35-approval-packet-draft.md` |
| `blocked_pending_explicit_cache_mutation_approval`, `B38-S2` | `docs/planning/product-agent-os-track-10-backlog.md`, `docs/product-agent-os/control-plane-current-state.md` |
| `B39-TEST-M01..M54`, `B39-S1..B39-S5` | `prod_test.md`, B39 packets |
| `B40-S2..B40-S5`, `manual_only`, `not_promoted` | `docs/planning/product-agent-os-track-10-backlog.md` |
| `B41-S1..S9` | B41 packets and Track 10 backlog |
| `B42-S1..S5` | `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json` |
| `B44-S0..S7` | B44 packets and Track 11 plan |
| `B45-PCA-M24..M27`, `B45-PCA-M37-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`, `B45-CQRR-A01`, `B45-CQRR-A02`, `B45-CQRR-A03`, `B45-CQRR-T23..T34` | B45 packets, Track 11 plan and registry |
| `DOC-M34..DOC-M41`, `DOC-M25` | Track 11 plan and documentation-refresh packets |
| Track 8 / Track 9 / Track 10 | `docs/planning/product-agent-os-track-8-detailed-backlog.md`, `docs/planning/product-agent-os-track-9-backlog.md`, `docs/planning/product-agent-os-track-10-backlog.md` |
| Source registry | `docs/sources/registry.md`, `docs/sources/registry.en.md` |

## Compatibility Anchors

Compact route anchors: `B37-S1`, `T10-PLAN-M01..M03`, `T10-PLAN-M18`, `task-matrix contract`, `task-matrix-plan.md`, `B39-TEST-M21-A01..A03`, `B39-TEST-M22-A01..A03`, `B39-TEST-M23..M33`, `B41-S5-M21..M23`, `B41-S6-M24..M30`, `B41-S7-M31..M40`, `B41-S8-M41..M47`, `B42-S1..S5`, `B44-S0` through `B44-S7`, `B45-RETEST-Q0-Q2-A01`, `B45-RETEST-Q3-FIXTURE-STATIC-A01`, `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, `B45-POST-Q4-NEXT-TASKS-A01`, `B45-POSTQ4-T01-T04-A01`, `B45-POSTQ4-T05-A01`, `B45-POSTQ4-T05B-A01`, `B45-POSTQ4-T06-A01`, `B45-POSTQ4-T08-A01`, `B45-POSTQ4-T10-A01`, `B45-POSTQ4-T11-A01`, `B45-POSTQ4-T12-RUN-A01`, `B45-POSTQ4-T13-A01`, `B45-POSTQ4-T14-A01`, `B45-POSTQ4-T14-RUN-A01`, `B45-POSTQ4-T15-A01`, `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `B45-POSTQ4-T18-A01`, `B45-POSTQ4-T19-A01`, `B45-POSTQ4-T20-A01`, `B45-POSTQ4-T20-A02`, `B45-POSTQ4-T20-A03`, `B45-POSTQ4-T21-PREFLIGHT-A01`, `B45-POSTQ4-T21-PREFLIGHT-A02`, `B45-POSTQ4-T21-PREFLIGHT-A03`, `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, `B45-POSTQ4-T22-A02`.

## Completion Claim Rule

Do not say that a feature works, a bug is fixed, tests pass, a release is ready, or behavior is verified unless:

- the relevant check ran in the current run; or
- the claim is explicitly scoped to earlier evidence and the evidence owner is named; or
- the missing verification is recorded as an accepted gap.

<!-- product-agent-os:end test -->

## Documentation refresh verification — 2026-11-03

Task: `PAOS-DOCS-REFRESH-2026-11-03`. Run the mandatory docs/control-plane route above, both new task-matrix validators, changed TOML/JSON example parsing, semantic RU/EN review, official-link/source comparison, protected-file hashes and strict MkDocs with `--site-dir .docs-tools/reports/gpt6-docs-preview`. The existing `.venv-docs` runtime is used without dependency installation. A preview build does not update or prove freshness of root `site/` and is not browser evidence.

Initial check after plan creation: combined four-module suite ran 224 tests, exit 1 (15 failures, 33 errors); errors include Windows temporary-directory permissions, new-page counts and a legacy validator hardcoding the August plan. Both hook validators and docs checker passed. Agent validator remains exit 1: `project config must set sandbox_mode = workspace-write`; this was already found in the read-only audit and is outside implementation scope. These are initial observations, not final acceptance. Current final evidence belongs to the [refresh plan](docs/planning/2026-11-03-gpt6-documentation-refresh.md) and RUNLOG.

Docs inventory maintenance accounts for three new localized page pairs while preserving historical site-promoted counts and pending-site semantics. It does not weaken assertions. Temporary files use an authorized workspace directory if the inherited TEMP cannot support the tests. Repeat only checks whose inputs or execution environment changed.

Final refresh evidence: 224 tests passed across the four required modules (100 + 5 + 25 + 94); both hook validators, task matrices, task-state consistency, docs structure and diff checks passed. Strict preview build passed; 20 official sources and 10 complete TOML/JSON examples checked. Root site and runtime activation remain unverified/unchanged. The agent-validator failure is a separate retained technical gap, not a green result.
