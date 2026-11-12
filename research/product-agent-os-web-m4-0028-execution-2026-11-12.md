# PAOS-0028 — Интеграционная проверка пути

Source status: project-authored / implemented and locally technically verified, 2026-11-12. Human/release acceptance separately owned.

## Scope и pre-edit план

Baseline HEAD `284a19da438e92482399a7906a444e96e2afd7ec`, worktree clean; scope clock14:43:26UTC /17:43:26MSK. PAOS-0028/M4/execution_order51; requirements — task card и PRD14.9 ten scenarios plus previous main journey. Root sole writer; `/root/integration_coverage` read-only GPT-6 Astra/medium исследует blocker фрагментированного покрытия. One independent assurance window; actual App worker может использовать только disposable acceptance. Остальные55cards/estimates/order/groups и previous failed receipts сохраняются. Next PAOS-0029 отдельно.

Existing capability scan: M2 TaskManager/browser runner covers hierarchy/catalogs/manual guards/links/comments/attachments/Kanban; workflow tests и M2b browser cover immutable versions/migration/editor; App gateway/recipe/native runners cover scope, command approval, exactly-key retry, Stop ACK/history. Их current source contracts — `task-manager/service.mts`, `workflows/registry.mts`, `runtime/app-agent-gateway.mts`, `tasks/user-commands.mts`, SQLite transaction owner, Web features. Smallest safe patch — reuse those runners, add one cross-domain preservation regression and one connected M4 native/browser journey. No new runner implementation/framework/dependency/provider API. Existing test seeding is fixture setup, не UI proof.

Owned create files: `tests/web/m4-integration.test.mts`, `tests/web/single-window/m4-integration-acceptance.mts`, this report, `product-agent-os-web-m4-0028-results-2026-11-12.json`. Existing acceptance files may receive scoped obsolete-selector repair only after observed failure. Product sources may receive minimum reproduced bugfix only; no speculative refactor. Docs owners REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG/Web README/RU+EN registry, current0028 MD+JSON card. Forbidden: unrelated cards, global policy, credentials/providers/Git/publication/install/target mutation outside disposable fixtures.

### Requirement → Given/When/Then → check → evidence owner

| ID / requirement PRD14.9 | Given / When | Then / check family | Owner |
| --- | --- | --- | --- |
| SC14-01 hierarchy | Epic/UserStory/Subtask; invalid parent/self | valid tree retained, invalid save rejected; M2 browser + integrated service | root |
| SC14-02 authorship | Agent draft on user request; later edit | creator agent/initiated_by user immutable; domain integration | root |
| SC14-03 manual | No run; criteria passed / required child open | owner Done allowed / child guard, Cancel reason; browser | root |
| SC14-04 versions | Bug affects1.2/fix1.3; filter | Fix filter finds only intended records; M2 browser | root |
| SC14-05 board | Drag/move to multi-status column | explicit target; invalid transition unchanged; browser | root |
| SC14-06 workflow | Publishv2 whilev1run; stale/absent migration mapping | immutable pins, no partial migration; workflow+integration | root |
| SC14-07 links | A→B→C; attemptcycle; reciprocal relates | cycle rejects without data loss; relates no gate | root |
| SC14-08 activity | User/agent comment, field/status edits, attachmentdelete | distinct Comments/History actor/time/before-after, tombstone | root |
| SC14-09 execution | Retry transition; terminal whilewriteractive | one run, Stop requested≠terminal, ACK then close | root/native |
| SC14-10 appearance | RU/EN×light/dark, keyboard editor/transitions | controls accessible and values retained; bounded browser matrix | root |
| MAIN legacy route | Task→plan→session→native diff/checks→owner accept | stable links/pins, no automatic Done, durable result | root/App worker |
| DATA negatives | Stale migration/linkcycle/badattachment after valid artifacts | exact revisions/metadata/bytes unchanged on rejection | root |

Business rules/invariants: done requires owner and criteria/dependencies/children; terminal requires no active writer; replay never duplicates grant/run; rejected writes leave all unrelated task/catalog/link/attachment data intact. TaskManager owns workflow/hierarchy/links, runtime owns active writer/ACK, store owns atomic CAS, Web renders owners. Term-to-source: PRD14.2/4/5/6/7/8 → above modules/API/UI labels; architecture unchanged, no new bounded contexts or FSD layers. New ADR/diagram not_applicable: tests exercise existing boundaries. Domain expert human acceptance not inferred from synthetic checks.

Compact code-change contract: existing_capability=listed fixtures/runners; smallest_safe_patch=tests+bounded observed repairs; invariants=above; dependency_decision=no_new_dependency; risk_selected_tests=lowest service/transaction layer for rollback, browser for navigation and state, actual native for Stop/approval; comment_decision=explain fixture injection/identity/cleanup only; performance_applicability=not_applicable workload/SLO promotion; evidence_and_gaps=proceed with current source checks, historical receipts explicitly dated. No artificial RED for test-only additions; actual bugs use intended behavioral RED→minimal GREEN. No weakens/skips to force pass.

Plan quality: exact commands `node --test tests/web/m4-integration.test.mts`, `node --test tests/web/*.test.mts`, `npm run check:web-m1`, `npm run build:web`; existing `m2-task-manager-browser-acceptance.mts --synthetic-browser`, `m2b-browser-acceptance.mts --synthetic-browser`; new `m4-integration-acceptance.mts --synthetic-browser` and `--actual-app-integration` with exact installed browser/native paths; native candidate/default when adapter changes; docs105/lifecycle251/check_docs/hooks/matrix/compatibility/eval gates. Expected exit0, no framework/page errors, named assertions, no external requests, current source hashes, fixtures cleaned. Rollback current hunks only, never delete persisted user data. Root evidence owner. No undefined plan placeholders; scenario gaps remain explicit until receipts. Conditional gates: test strategy/privacy/runtime/browser/API/transaction proof required; business-discovery/analytics/model-quality/SLO/release measurement/CI changes not_applicable (technical integration, no promotion). No hook/MCP/automation activation. Strict MkDocs not_applicable unless nav/config/Mermaid/site changes.

Browser flow: paired disposable local service→TaskManager task/plan→Session/native approvals→changes/checks→owner acceptance; second active run→Stop ACK→terminal. Browser plugin absent; existing Playwright1.63.0/Chromium1223 via absolute cached paths, no installation. Screenshots outside repo in permitted visualization directory. Isolated profiles and loopback only; secrets/capabilities stay memory-only. Build warning remains a known limit unless code changes justify new measurement.

## Обнаруженные разрывы и bounded repair

Read-only research `/root/integration_coverage` подтвердил: старый M1 task-lifecycle browser runner использует прежние selectors и не является текущим M2 proof (static incompatibility, не observed failure). Переиспользован current M2 runner, добавлен `--scenario integration`; отдельный M4 runner связывает UI task creation, UI session, planning, execution, diff/check projection, explicit acceptance и active Stop. Fixture setup, HTTP negative probes и UI actions различаются в receipts.

SC14-02 имел функциональный gap: save всегда записывал user creator; агент мог только предложить draft. Теперь в S09 execution есть явный одноразовый opt-in «Разрешить агенту создать Bug в этом запуске», выключенный по умолчанию. После подтверждённого send он сбрасывается; mode/target change также сбрасывают его. Autonomy/recipe jobs не получают это право. `/runtime/send` привязывает initiating actor к authenticated principal; входящий `taskCreationInitiator` запрещён. Флаг не разрешает native command и не расширяет scope исходного writer.

Private capability channel `task-create` принимает только runId/operationId/title/summary/acceptanceCriteria. Claimed execution job должен быть running, generation/lease актуальны, owner opt-in сохранён в server-owned job. Browser cookie не даёт private capability. Server выводит stable UUID, creator=`agent:<profile>:<run>`, initiatedBy=user, initial Backlog Bug и source comment с run/session ссылками. Лимит32Bug/run; new Bug не dispatches run и не получает acceptance. TaskManager сохраняет стандартные workflow/key/time/graph rules; SQLite проверяет claimed job/owner/expiry и CAS source run в одной транзакции с Bug, comment и receipt. Public save не принимает trusted options и не может изготовить agent provenance. Existing creator/initiator immutable при последующих owner edits.

Независимый `/root/integration_review` (GPT-6 Astra/medium, separate_fresh_context) воспроизвёл P2: `newM2Task` добавлял текущий createdAt в каждый retry input, вызывая IDEMPOTENCY_CONFLICT. Исправлено нормализацией createdAt=null перед trusted save; service задаёт реальный timestamp первой записи. Regression повторяет запрос после изменения времени. Root добавил отрицательные проверки creator injection, planning/no-opt-in/terminal/cancelled authority, stable retry и immutable initiator. Reviewer проверял состояние до позднего root S09 repair; повторное независимое окно не выдаётся за выполненное.

Сквозной native run обнаружил второй продуктовый дефект: sparse S09 pending snapshot и durable S22 App operation меняли evidence одной decision, создавая revision churn; inline approval отвергался с REVISION_CONFLICT. `inline-revision-red.log` получил intended 2≠1; `decisions/service.mts` теперь разрешает exact App identity через тот же durable operation и не берёт unrelated fileChanges из session snapshot. GREEN —17service/integration checks и полный Web473/473. Общий response owner/expiry/unknown-no-replay сохранён; guards не ослаблены.

## Traceability текущей проверки

| Requirement | Current executable evidence | Уровень / граница |
| --- | --- | --- |
| SC14-01 | `m2-task-manager-browser-acceptance.mts --scenario integration`: exact Epic→UserStory→Sub-Task, invalid parent options; `m4-integration.test.mts`: invalid Task/self-parent rejection | UI + transactional service, records/audit/blob preservation |
| SC14-02 | `m4-integration.test.mts`; M4 runner owner checkbox→private worker creation→owner edit | HTTP principal/private job/SQLite + actual App receipt отдельно |
| SC14-03 | M2 integration112: manual child/parent Done, missing criteria/child guards, Cancel reason,0runs | User-only UI, не agent stand-in |
| SC14-04 | M2 integration: v1.2 Affects/v1.3 Fix, distinct release filtering | UI/HTTP persistent profile |
| SC14-05 | M2 integration: drag guarded transition, multi-target outcome; M4 service: impossible transition leaves exact records/audit/blob | UI + service negative |
| SC14-06 | Full Web `workflows.test.mts`: v2 publish/pinned v1, active migration fence, stale/phantom previews; M2b current51: workflow editor/publish/migration/rollback; M4 service missing/stale mapping preservation | Actual UI + storage/runtime contract; не отдельный actual-native workflow migration claim |
| SC14-07 | M4 service three-node DAG/cycle+canonical reciprocal relates_to; M2 integration UI dependency/waiver | Canonical symmetric edge не дублируется; informational edge не блокирует source admission |
| SC14-08 | M2 integration user comment/edit/deletion/History/attachment tombstone; M4 worker-created source comment visible, owner priority edit retains creator | UI + source actor/time/history; private text redacted |
| SC14-09 | Full Web recipe-runtime idempotency; M4 runner native Start marker→terminal denied→Stop→terminal nonzero command receipt→worker interrupted ACK→TaskCancelled | Run/operation/task outcomes различаются; ранний side effect сохраняется, поздняя запись отсутствует |
| SC14-10 | M2 integration112: RU/light,RU/dark,EN/light,EN/dark; visible new fields, keyboard tabs/workflow focus, desktop/mobile geometry | Bounded functional acceptance; PAOS-0029 полный a11y scope отдельно |
| MAIN | M4 runner task/session созданные UI→read-only planning result→explicit execution/Bug/native command→file/check projection→owner Done→restart | Current owner-selected App route; historical closed-App standalone gate не подменяется |
| DATA | M4 service compares projectEntities, audit и exact downloaded bytes после rejected migration/link/attachment operations | No data loss assertion, не только наличие error |

Context7 `/microsoft/playwright/v1.63.0` подтвердил [официальный waitForResponse-before-action contract](https://github.com/microsoft/playwright/blob/v1.63.0/docs/src/network.md) и [dragTo](https://github.com/microsoft/playwright/blob/v1.63.0/docs/src/input.md). Installed Playwright/cache использованы без изменения зависимостей. Selected frontend-testing-debugging и React best-practices advisory; root lifecycle final contract имеет приоритет над optional QA gallery.

## Receipts, failures и claim ceiling

Scratch `.tmp/paos-m4-0028/` содержит current gates и сохранённые failures. `agent-create-red.log` — unsupported fields baseline; reviewer и `integration-first.log` подтвердили timestamp retry bug. Ранние тестовые ошибки DUPLICATE_ISSUE_LINK (симметричная связь canonical), stale parent revision после upload, неверное имя transition error и interrupt без runId были fixture/oracle errors; исправлены без изменения product guards. `inline-revision-red.log` — valid revision-churn regression. Initial M2 integration90 failed из-за отсутствующей fixture Cancel control; исправлен только переход к existing item, final112 passed.

M4 fixture failures сохраняются: S22 selector «Принять» вместо current «Разрешить действие»; navigation обратно в catalog без выбора session; wrong Stop locale keys; audit object ошибочно считался array. Отдельная failed receipt показала ожидание operation.state=cancelled, хотя native contract возвращает terminal completed/nonzero после Stop; oracle уточнён по существующему contract. Последний synthetic M4 run51 прошёл native start marker, terminal guard, settled process, worker ACK и restart. Нельзя считать ранние fixture failures regression RED. Поздний native write не скрывался cleanup: до teardown проверены scoped marker и terminal receipt.

Full Web final473/473 skip0,15.8567142s/exit0; typecheck/build exit0. Final suite includes explicit priority/status actor/before/after/time assertions. Build57modules, JS516.36kB/gzip150.01kB, existing >500kB warning; SLO/performance promotion not_applicable. Native cached Codex0.167.0 SHA256 `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`,369062704bytes; current adapter `67d6ced8b371be3dcf433637a3df7a8ed5ad3140c7a412e40178ad05abbe5869`, candidate/default passed without providers/auth. Manifest preserves every other pin and prior evidence; earlier candidate receipts are not called final current proof.

## Финальные результаты и handoff

| Команда текущего запуска | Outcome | Receipt относительно `.tmp/paos-m4-0028/` |
| --- | --- | --- |
| `node --test tests/web/*.test.mts` |473/473,0skip,exit0 | `web-full.log` |
| `node --test tests/web/m4-integration.test.mts tests/web/decision-service.test.mts` |17/17,exit0 | `focused-green.log` |
| `npm run check:web-m1`; `npm run build:web` |both exit0 | `types.log`, `build.log` |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` |1450tests/622.134s,OK(skipped1),exit0 | `python-full.log` |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` |91all ok,exit0 | `fixture-eval.log` |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` |26/26,status ok,exit0 | `transcript-eval.log` |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` |compatible,exit0 | `compatibility.log` |
| M2 TaskManager runner `--synthetic-browser --scenario integration` |112checks,passed,cleaned | `../paos-m2/browser-evidence-GOxpeG/m2-browser-result.json` |
| M2b workflow runner `--synthetic-browser` |51checks,passed,cleaned | `../paos-m2b/browser-evidence-ePiNlO/result.json` |
| M4 runner `--synthetic-browser` |51checks,passed,cleaned | `browser-evidence-MFZZRv/result.json` |
| M4 runner `--actual-app-integration` |46checks,passed,cleaned | `actual-evidence-fZiWyh/result.json` |
| Native broker runner `--run-once [--candidate-inspection] --binary <exact fixture>` |candidate/default passed,exit0 | `native-candidate.log`, `native-default.log` |
| Docs/lifecycle251 command below |251tests/29.600s,OK,exit0 | `docs-lifecycle.log` |
| Hooks JSON/dir, task matrix/state, check_docs, diff |all exit0 | named `*-validation.log`, `hooks-*.log`, `check-docs.log`, `diff-check.log` |

Exact M4 arguments: `--binary C:/Users/user/Desktop/project/codex_docs/.tmp/paos-m4-0028/native-fixture/codex.exe --playwright-core C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core --chromium C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe --screenshots C:/Users/user/.codex/visualizations/2026/11/12/01a1cedc-5a90-7a23-bb27-6f755c6885ce`. These are host-specific evidence invocation paths, не distributable fixture constants. M2/M2b use the same browser arguments without native/screenshot options. PATH/Path normalized process-locally; Python TEMP/TMP point to canonical task-owned test-temp, без изменения OS environment.

Actual `/root/recipe_app_worker` handled3uniquejobs: plan `app-run-2868b88ffc2fe08d2257fbf49d93882f1c43458b41e3cabc0b91dbcc24bb1c1d` (read-only, no create/commands); build `app-run-ae8377fd965223780a4b9282d72d952dc927afdcb05ad838ac7124357e8bd33d`, check-build exit0/M4_BUILD_OK; cancel `app-run-5acfff723f3c3b252973e07b9592c012317e0a573baf79c3810f36f55d69d836`, check-cancel terminal transport completed/exit1/M4_WAITING, затем job interrupted ACK. Created Bug `5320e71e-339f-4dd7-aa08-9b459fdb1fd9`, creator/initiator проверены UI+service. Worker прочитал scopes/workflow defaultv1; assetPins=[] — наличие frozen role profile не заявлено. Helper exit0/heartbeat stopped. Host identity attested, не cryptographic; native sandbox ограничивает только PAOS-mediated commands. Native Stop сохранил `cancel-proof.txt=M4_RUNNING`, поздний append не выполнен; cancel Task разрешён лишь после terminal process receipt и worker ACK.

Root просмотрел actual acceptance screenshot и EN/dark integration screenshot: реальные controls rendered, keyboard focus виден; actual screenshot прокручен к lower acceptance controls/Reopen, поэтому Done подтверждён API assertion, не вымышленным заголовком на screenshot. Скриншоты не доказывают полный contrast/screen-reader audit; это PAOS-0029.0page/console/external-request errors в final M4 receipts.

Control-plane approved digest `sha256:31e69a58da8cbd76971fb2e03f1c2eabcaca57b3044e9c2a5e07cb6e469485e2`: owning sections REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG применены с recovery journal, source pin preserved. Card MD+JSON beforeimages и exact preservation находятся в task-owned matrix recovery receipt; legacy capitalized task card обновлена scoped writer,55other cards byte/value unchanged. README/RU+EN registry синхронизированы. Current assessment reviewed_inputs_valid/gaps[]. Все root files <40000UTF8bytes; TEST warning32000 не hard-limit violation. `AGENTS.md`, `prod_test.md`, MkDocs nav/config/Mermaid/site not_applicable/unchanged; fresh-session hook activation и site freshness не заявлены.

Post-sync command: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q`. Validators: `validate_hooks.py .codex/hooks.json`, `validate_hooks.py .codex/hooks`, `validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md`, `validate_task_state_consistency.py .`, `python -B tools/check_docs.py`, `git diff --check`. `adapterRevision()` совпал с qualified manifest. Final docs105, safe receipt/source hashes и cleanup записаны в [machine results](product-agent-os-web-m4-0028-results-2026-11-12.json).

Exact synthetic binary удалён после hash/containment check; browser fixture roots и owned test TEMP очищены, существующие пользовательские процессы не завершались. Final self-review сопоставил10requirements с проверками и ограничениями; reviewer P2 repaired/root verified, late S09 defect root RED/GREEN/browser+actual verified. No human/commercial/release acceptance, broad model-quality/token/cost/SLO or closed-App daemon claim. No Git writes, dependency installation, provider API calls or user process termination. Следующая PAOS-0029 «Доступность, языки и темы»: dependency0028 implemented; отдельный scope.
