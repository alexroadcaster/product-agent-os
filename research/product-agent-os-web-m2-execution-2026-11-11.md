# Product-Agent OS Web — выбранная очередь M2, 2026-11-11

Source status: project-authored implementation evidence; implemented_locally_verified_app_active для выбранных десяти задач. Итоговые receipts ниже; machine evidence — [results JSON](product-agent-os-web-m2-results-2026-11-11.json). Это техническое закрытие выбранного scope, не всего M2 и не release acceptance.

## Scope и источники

Авторизованная очередь: **PAOS-0031 → 0032 → 0033 → 0005 → 0006 → 0007 → 0008 → 0034 → 0038 → 0035**. Остальные 16 задач M2 и следующие этапы не входят в этот run. Карточки, зависимости и оценки принадлежат [Web-плану](product-agent-os-web-task-manager-plan-2026-11-09.md) и его JSON; требования — PRD §§13–14, экраны S04–S07/S24. [PAOS-0046](product-agent-os-web-commercial-review-2026-11-11.md) закрыта только как ранний review. AUTH-G1–G6/C46-01–08 и commercial release blocks сохраняются.

Baseline: `.tmp/paos-m2/baseline/manifest.json`, 172 исходных файла; сохранение закончено 2026-11-11T17:41:57.926359Z. В baseline включены уже существующие изменения M1/PAOS-0046. Откат касается только новых hunks этого run; Git history не изменяется.

## Реализация и acceptance trace

| Карточка | Наблюдаемое поведение / независимый отрицательный сценарий | Владелец evidence |
| --- | --- | --- |
| PAOS-0031 | Epic → standard → Sub-Task; illegal parent/cycle/reparent отклоняется; parent не закрывается с обязательным незавершённым child; roll-up не складывает вложенные roll-up повторно | Root; M2 profile/manager tests и browser |
| PAOS-0032 | Immutable creator/unknown provenance; 11 components, multi-select/archive; реальные календарные даты и timezone | Root; contract/API/browser |
| PAOS-0033 | Separate Affects/Fix, version registry/archive/release policy; Done не выпускает версию | Root; contract/API/browser |
| PAOS-0005 | List/board используют полный snapshot; filters/group/sort/view; явная DOM pagination сохраняет полный count | Root; UI model/browser |
| PAOS-0006 | Все исходные 12 полей и M2 extensions; draft допустим, Ready требует постановку; stale revision сохраняет пользовательский ввод | Root; API/browser |
| PAOS-0007 | Planned/actual операции, rename, source revision/context, assignments/artifacts/session references; stale источник не подменяется текущим | Root; reference tests/browser |
| PAOS-0008 | Manual evidence без agent run, completion/cancel/reopen, children/dependencies/terminal receipt; история и первый actual start сохраняются | Root; transaction/gateway/browser |
| PAOS-0034 | Managed copies, quota/MIME/path checks, lost-ACK replay, download-only, comment revisions/tombstones, отдельный безопасный audit; реальный backup/restore bytes | Root; attachment/API/browser |
| PAOS-0038 | Canonical/inverse edges + legacy preservation, DAG/duplicates/clones; cancelled blocker не удовлетворяет dependency; pending Stop привязан к исходному run | Root; transaction/HTTP/gateway/browser |
| PAOS-0035 | 8 statuses/7 columns, transition-only mutation, drag/menu target choice, WIP, cancellation reason/resolution | Root; transaction/UI/browser |

Given/When/Then применяется на публичных seams: сохранённая задача/связь/файл → пользовательская команда или реальный HTTP/browser action → сохранённые данные, отказ без мутации либо наблюдаемый результат. Scope исключает Jira sync, workflow editor PAOS-0036, M3 autonomy, новый provider/auth route и реальные project/customer данные.

## Границы кода и данных

- `packages/contracts/issues/`: versioned `m2_task_profile_v1`; strict M1 decoder не ослабляется. ID/key, creator, provenance, links и unknown time сохраняются при явном расширении M1.
- SQLite Worker остаётся единственным транзакционным writer. Иерархия, immutable fields, revisions/authority epoch/idempotency, Ready, terminal gates и WIP проверяются сервером. Исходная SQL migration v1/checksum сохранена; M2 использует JSON/settings и существующие blob relations. При первом M2 write применяется additive migration2 с truthful compatibility stamp; M1-only database остаётся schema1.
- `apps/local-service/src/task-manager/` и authenticated HTTP commands владеют catalogs, links, comments, managed attachments и reference resolution. Browser не получает SQL или provider credentials.
- `apps/web/src/features/tasks/` — основной Tasks route. Pure model, Editor, Panels и Settings используют общий CSRF/authority API client. Session composer сохраняет M1 helper; selector расширен на M2 без Epic execution.
- `paos_full_local_profile_v1` — полный управляемый локальный архив SQLite + blobs, восстановление в новый inactive profile. Task-only JSON export не выдаётся за binary archive или переключение активного профиля.

Bounded context — issue management внутри существующего local service; словарь Epic/standard/Sub-Task, Ready, resolution, dependency, attachment и version соответствует PRD §14, typed contracts, API actions и UI labels. Отдельные микросервисы, новая БД, новый runner, FSD scaffolding, CI и telemetry не требуются.

## Code-change contract и verification policy

- Existing capability: переиспользованы LocalStore, SQLite Worker, session gate, generic events/history, snapshots/blobs, runtime gateways и theme/locales. Новых dependencies нет.
- Smallest safe patch: отдельный versioned profile и Task Manager feature; прежние M1 source contracts/tests остаются защитой совместимости. Hooks/config/model policy и прочие PAOS задачи не меняются.
- Invariants: source-owned task matrix остаётся file-owned; явные transitions/preview, без silent loss, secret/auth-cache чтения, payer fallback или automatic Done от model turn.
- Risk-selected tests: pure contracts → реальная SQLite transaction → authenticated Request/Response → built browser → нужная проверка существующего App route. Fixtures не называются actual model/native proof.
- Comments: поясняются trust/transaction/idempotency/compatibility boundaries; синтаксическая narration не добавляется.
- Performance: complete snapshot с явным ресурсным пределом; DOM list100/column50 + More. Большие selector inventories и design SLO не объявляются измеренными.
- Rollback: только собственные hunks и private fixture roots; restore не заменяет активную БД. Recursive cleanup проверяет принадлежность синтетического root.
- Docs: owning evidence здесь; REQUIREMENTS/PLAN/TEST/RUNLOG и карточки/JSON синхронизируются после проверок. EVALS/AGENTS/prod_test не требуют изменения правил, thresholds или Batch39 evidence.

## Наблюдаемые проверки до интеграционного исправления

Среда: Node v26.5.0, npm12.0.1, React19.3.1, TypeScript7.0.2; установленный Playwright core1.63.0/Chromium1223. Browser plugin not available; planned acceptance использует существующий local Playwright, без установки.

| Команда | Результат и provenance |
| --- | --- |
| `node --test tests/web/m2-profile.test.mts tests/web/m2-manager.test.mts` | Backend handoff:8/8,1239ms,exit0; ещё не финальная интеграция |
| `node --test tests/web/ui-m2-manager.test.mts tests/web/ui-session-target.test.mts tests/web/ui-api.test.mts tests/web/ui-task.test.mts` | Frontend handoff:20/20,160.3527ms,exit0 |
| `npm run check:web-m1` | Backend и frontend handoff exit0; повтор после runtime repair обязателен |
| `npm run build:web` | Frontend handoff exit0,42modules; JS `index-B83skSLk.js`372.00kB/gzip111.44kB; CSS `index-C6CatpJF.css`11.10kB |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` | 1450 tests,537.679s,OK,skip1,exit0. До финальных docs edits; Python implementation не менялась. `.tmp/paos-m2/full-unittest.log` |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | 91 fixtures; все `expected_checks` true;exit0. `.tmp/paos-m2/fixture-eval.log` |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | 26/26,exit0. `.tmp/paos-m2/transcript-eval.log` |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | compatible,exit0; local structure, не host activation. `.tmp/paos-m2/codex-compatibility.log` |

Context7: official React `/reactjs/react.dev` — stale Effect responses/cleanup и сохранение state; official Node `/nodejs/node/v26.0.0` — DatabaseSync foreign keys, prepared statements и transaction state. Версии установленных библиотек проверены локально; сеть не использовалась для provider calls.

## RED, ошибки и исправления

- Поведенческий RED: повтор managed upload возвращал `IDEMPOTENCY_CONFLICT`; последующий GREEN проверяет durable replay и восстановление metadata/bytes.
- Missing API/module/export и TypeScript nullable/useRef errors были setup/implementation gaps; они исправлены, но не выдаются за независимый поведенческий RED.
- Raw `risks:['dependency_review']`/`['scope_review']` не должны освобождать новые transitions от guards. Проверка зависит от точного набора изменённых переходов, а не от пользовательской строки risk.
- Bootstrap сначала имел будущий `updated_at`; hook отказал. Исправлен полный собственный marker. Literal PowerShell write был denied filesystem; защищённые настройки не менялись. Это metadata receipt, не product proof.
- Диагностическое CIM чтение процессов недоступно; результат unittest получен из собственного лога/exit0, отсутствие процесса не интерпретировалось как успех.

## Исторический список repair gates до интеграции

Перед техническим закрытием нужны: generic decoder и own-run ordering в обоих gateways; safe pending Stop с исходным run/binding/generation; idle/structural/Done guards публичных writes; M1 upgrade/link removal regression; calendar/timezone/catalog validation; cleanup raced uploads; итоговые HTTP/browser/runtime checks и independent review. Никакой из этих пунктов не объявлен accepted gap для выбранных десяти задач.

Начальный checkpoint этого раздела: independent review/browser ещё не выполнялись, статусы не повышались. Это сохранённый исходный gap, закрытый техническими проверками ниже; он не является текущим verdict.

## Итоговая проверка реализации

Все десять выбранных карточек реализованы. Source ownership передавалось последовательно architect/frontend → backend → root, с одним source writer. Root проверил публичные seams, итоговый diff и ограничения; отдельный reviewer проверил исходники и после repair дал `closed_allowed`. Остальные **16/26 M2 tasks остаются planned**, следующая плановая PAOS-0036 не выполнялась по этой команде. Сумма оценок выбранных карточек 140 h остаётся плановой оценкой; per-task active duration не измерялась и не подменяется общей длительностью чата.

| Команда / сценарий | Наблюдаемый итог текущего run |
| --- | --- |
| `node --test tests/web/*.test.mts` | **345/345, fail0, skip0, 6136.5744ms, exit0**. `.tmp/paos-m2/final-web.log`; process-local TEMP/TMP — `.tmp/paos-m2/final-native-temp` (Windows canonical lower case). Включены реальные synthetic junction/hardlink cases. |
| `npm run check:web-m1` | exit0 после всех source repairs. |
| `npm run build:web` | exit0,44 modules; JS `index-DgQ0iIeg.js`376.16kB/gzip112.90, CSS `index-C6CatpJF.css`11.10kB/gzip3.08. |
| `node tests/web/single-window/m2-task-manager-browser-acceptance.mts --synthetic-browser --playwright-core <installed absolute path> --chromium <installed absolute path>` | **88 checks, passed**, `.tmp/paos-m2/browser-evidence-LzkG0t/m2-browser-result.json`, browser/service closed, fixture cleaned. |
| Тот же browser runner `--scenario settings-cas` / `--scenario markdown` | **17 / 11 checks, exit0**: `.tmp/paos-m2/browser-evidence-1gr8BZ/` и `browser-evidence-UCrvzs/`. Выполнены после исправления соответствующих алгоритмов; последующий UI description не меняет CAS/Markdown logic. |
| `node tests/web/single-window/sandbox-broker-acceptance.mts --run-once --candidate-inspection --binary <pinned installed codex.exe>` | final candidate native **passed**, 3 modes/write-deny/Stop/cleanup. `.tmp/paos-m2/native-broker-candidate-final.log`. |
| Тот же native runner без `--candidate-inspection` | final default loader **passed**, 3 modes, outside/TEMP deny, Stop, auth file absent, cleanup. `.tmp/paos-m2/native-broker-qualified-final.log`. |
| `node tests/web/single-window/m2-app-acceptance.mts --actual-app-m2 --binary <pinned installed codex.exe> --playwright-core <installed absolute path> --chromium <installed absolute path>` | **27 checks, passed_actual_m2_app_native, exit0**. `.tmp/paos-m2/actual-app-evidence-w8nuna/m2-app-result.json`; actual App consumer `/root/m2_actual_worker`, command source `paos_domain`, native exit0, cleanup. |
| `node .tmp/paos-m2/verify-manifest.mts <pinned binary>` | Unconfigured denied; exact tuple qualified; changed binary hash denied; process launches0; cleanup. `.tmp/paos-m2/manifest-loader.log`. |
| `node .tmp/paos-m2/downgrade-check.mts` | Сохранённый настоящий v1 source принимает schema1, отклоняет schema2 с `SCHEMA_INCOMPATIBLE`; новый source повторно открывает schema2; v1 SQL checksum неизменен, cleanup. Ранее выполненный current-run receipt, не новый повтор. |

Browser acceptance прошёл создание Epic/Bug/Sub-Task и неполного draft, Ready refusal, 11 components, отдельные Affects/Fix и version description, unsaved navigation/tab state, stale revision, reviewed reparent, exact pinned file read, сохранение filters, child/dependency guards, manual Done/cancel/reopen/first start, inverse/cycle links, safe Markdown/edit/delete/audit redaction, managed copies с одинаковым именем, потерянный ACK и retry без дубликата, MIME rejection, exact downloaded bytes, tombstone, legacy M1 upgrade с unknown creator, all-project archive/inactive restore, настоящий drag через transition и multi-status menu choice, RU/EN, dark/mobile390. Page errors и unexpected external browser requests отсутствуют. Desktop/mobile screenshots просмотрены root: document overflow не обнаружен; полный WCAG audit не заявляется.

Actual App consumer самостоятельно прочитал correlated prompt и вычислил 17+4+9=30. Единственный `command` создал `m2-proof.txt` с `wx` после UI approval; root сверил точные bytes, exit0, recorded `actualOperation=create`, App answer и отображение в browser. До ручного acceptance задача оставалась in_progress: model turn не выполнил automatic Done. Checked schema — `m2_task_profile_v1`, M1 fallback не скрывал сценарий. Это реальный активный App worker и offline command broker; отдельного provider client/API key, OS credential операций и account/quota qualification не было.

## RED и dispositions независимого review

Review `/root/m2_independent_review`: начальный контекст `separate_fresh_context`, targeted repair pass — `separate_reused_context`, два прохода. Reviewer не запускал runtime самостоятельно: проверял source и фактические root/builder receipts. Все три findings получили `confirmed_fixed`, итог `tester_verdict=closed_allowed` в bounded local engineering scope.

| Finding | Исправление и regression |
| --- | --- |
| P1: generic `/commands` понижает existing M2 до M1 и теряет fields/guards | Prior-M2/new-profile invariant до decoder в atomic writer + friendly public refusal. HTTP/direct-store tests подтверждают отказ, сохранение data/revision/events и отсутствие receipt; unknown selector также rejected. |
| P2: Due Date меняется без reason через generic API | Единая writer/public проверка; negative no-mutation, positive ordinary title edit и deadline с reason. |
| P2: soft WIP override не журналируется явно | Writer вычисляет фактический count атомарно, удаляет supplied override metadata и записывает column/limit/count/actor/reason в existing receipt/public history. Checkbox без реального превышения не создаёт ложный override. |

Дополнительно version description ограничен 20000 символами, malformed/oversize отклоняются; archive с omitted description сохраняет прежний текст. Browser проверяет editor и сохранение. Parent deadline warning показывает превышение без наследования или изменения дат.

Focused final repair: **31/31,2976.1227ms,exit0**, `.tmp/paos-m2/review-repair-green.log`; typecheck0 и scoped diff0. `.tmp/paos-m2/review-repair-red.json` — явно обозначенный индекс исходных current-run tool receipts, не повторный RED run. Re-review source prefixes: user-commands `c7c06c17b3c2`, sqlite-worker `546c4d0c2f14`, service `ad9d6e19f11b`, repair tests `2e5eb5539ea4`. Полные source hashes находятся в results JSON.

Root browser RED: plain-text comment не имел `<strong>`; stale catalog draft после Refresh отправлял новую revision и перезаписывал server winner. Исправлены bounded safe Markdown renderer и base-revision binding каталогов/доски; конкретные повторные browser scenarios прошли. Full journey нашёл пустые criteria evidence на обычном transition: UI теперь не отправляет незаполненные evidence, Ready и Done дают соответствующие domain guards.

Остальные failed receipts сохранены и классифицированы, не выданы за behavioral RED: reload открывал Overview, legacy не имел M2 tabs, file input и button имели одно accessible name, scoped `has` и premature count были ошибками harness. Все исправлены ожиданием/selector/navigation без ослабления product checks. Managed full Web attempts 327/337 (skip1), затем322/337 (skip2) имели EPERM/junction/hardlink и fixture root mismatch; native final345/345 исполнил проверки без skip. Canonical-root fixture reconciliation исправлена, containment assertion сохранён. Windows ESM/`--input-type` Worker setup failures не являются feature RED; Context7 official Node worker documentation проверена для причины inherited execArgv.

Два actual App bind отказа `BROKER_RUNTIME_UNQUALIFIED` корректно остановили dispatch при adapter pin M1. После positive candidate native proof manifest перепривязан к exact final adapter `311f5daed342d4e63d9ea20c6ba307c318e21a747b578b7b43be269f7b87a2db`, затем default loader/native и actual App пройдены заново. Binary/OS/Node/SQLite/lock/capability pins не ослаблялись. Первоначальные и intermediate passed receipts сохранены с собственным provenance, final JSON указывает последний проверенный source.

## Compatibility, пределы и rollback

Lazy migration2 предотвращает запуск старого v1 source на M2 database; не заявляется retroactive fencing произвольного старого процесса с уже открытым SQL handle. Archive metadata правдиво несёт schema2/`paos-m2-v1`; v1 backups по-прежнему восстанавливаются. Полный локальный архив включает **все проекты локального профиля**; UI раскрывает это до export/restore. Restore создаёт отдельный inactive profile и не заменяет текущие данные. Откат приложения к v1 после M2 write требует отдельной старой schema1 backup copy; нельзя просто направить старый binary на schema2.

Markdown — объявленное безопасное подмножество: paragraphs/headings/lists/emphasis/code/HTTP(S) links, без full CommonMark/GFM claim. HTML/images/unsafe or credentialed links остаются инертным текстом; `dangerouslySetInnerHTML` и внешние preview fetch не используются. Attachment active formats download-only. Memory-only drafts не пишут project text в browser persistence.

Активные Codex App и consumer обязательны, host identity attested, sandbox только PAOS-mediated commands. Automatic wakeup, Desktop daemon, whole-App sandbox, real ChatGPT principal/quota/entitlement, broad performance, production/human/commercial acceptance не квалифицированы. AUTH-G1–G6/C46-01–08 по PAOS-0046 остаются release blocks; повторный review — PAOS-0030. Это не открытый обязательный gate внутри десяти выбранных implementation cards.

Rollback: восстановление только своих hunks относительно `.tmp/paos-m2/baseline`, сохранить PAOS-0046/чужие dirty changes; никаких Git history operations. Synthetic browser/native fixtures удалены по проверенным границам, failed receipts сохранены вне пользовательских project данных. Root marker изменяется только для собственной session после всех проверок.

## Control-plane sync

REQUIREMENTS/PLAN/TEST/RUNLOG и десять полных cards/JSON требуют обновления. Чужие 46 cards/objects, 56 tasks,12groups,execution order и все estimates должны остаться неизменными; detailed matrix не разделяется. EVALS/AGENTS — `no_change_needed` (rubrics/instructions/authority unchanged); prod_test — `no_change_needed` (Batch39 evidence не затронута). RU/EN source registry и Web README получают current pointer. Strict MkDocs — `not_applicable`: nav/Mermaid/config/extensions/site evidence не меняются. Финальный post-sync gate записывается ниже после фактического выполнения.

Итог sync: REQUIREMENTS/PLAN/TEST/RUNLOG обновлены через reviewed `documentation_sync_v1` digest `07438702ec67d393a9b87e16f9adc7cc6191b647e22d572b6627557e6f42ece3`; private recovery journal сохранён. Обычный apply получил filesystem permission denied на project `.codex/.../writer.lock`; тот же exact reviewed apply в authorized native context завершился exit0, без правок config/hooks/policies. Generic helper отдельно отказался обновлять pre-existing большую research matrix из-за 40000-byte facility limit; она сохранена целиком по явному правилу владельца. Десять card sections и matching JSON применены guarded source-owned CAS с before/after images `.tmp/paos-m2/matrix-cas-journal.json`, без изменения helper или отключения checks. Top current pointer, Web README и RU/EN registry синхронизированы. Дополнительных control-plane handoffs нет.

Post-sync: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q` — **251 tests,16.299s,OK,exit0**; process-local TEMP/TMP `.tmp/paos-m2/docs-temp`, log `.tmp/paos-m2/final-docs-suite.log`. `python -B tools/check_docs.py`, `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md`, оба `validate_hooks.py .codex/hooks.json` / `.codex/hooks`, `git diff --check` — exit0. Git предупреждает CRLF→LF normalization, whitespace errors не найдены.

Integrity `.tmp/paos-m2/final-integrity.json`: 56 tasks/12groups, выбранные10 implemented, остальные16 M2 planned, MD/JSON status parity, 46 других card blocks сохранены побайтно, 46 JSON objects и все estimates/execution_plan неизменны. Source hashes и final browser/actual App hashes совпали с текущими файлами. Root UTF-8 bytes: REQUIREMENTS39262, PLAN28347, TEST31654, RUNLOG25026 — ниже40000. Финальные full Python1450/fixture91/transcript26/compatibility receipts выше имеют явно сохранённый provenance до docs edits, неизменённая Python implementation не тестировалась повторно без причины.

Технический итог: **10/10 выбранных задач закрыты, closure_level=implemented_locally_verified_app_active**. Required implementation/review/runtime gates выбранной очереди выполнены; human/commercial/release и оставшийся M2 scope не повышены. AGENTS/EVALS/prod_test unchanged; чужой session marker и исходный PAOS-0046 пакет сохранены. Model/reasoning родителя — inherited baseline, точный ID/effort и совокупные token/tool counters недоступны в полном trace после compaction; четыре top-level agent spawns, два independent review passes наблюдались. Это не метрики стоимости или качества модели.
