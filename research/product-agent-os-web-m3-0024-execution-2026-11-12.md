# PAOS-0024 — очередь, назначения и владение файлами

Source status: project-authored / current local implementation evidence, 2026-11-12. Human/commercial/release acceptance отдельно.

## Контракт и решения перед реализацией

Owning task — PAOS-0024 в Web task matrix; dependencies0015/0019/0023/0037/0038 implemented. Scope: durable scheduler, pinned assignments, admission guards, API/UI, необходимые runtime seams. Следующая0025 отдельно. Оценка16h сохраняется; остальные55 задач не меняются. Baseline HEAD `eefdeeb6fe0236a7f15ff34a28083da72a2b4651`, worktree чистый до нового session marker/test.

Материальный конфликт: Product value карточки обещает независимых parallel writers, policy имеет concurrency1 на проект, SW-07 требует одного writer на workspace. Решение: фактическая параллельность только между distinct non-overlapping canonical workspace roots, global cap4, project policy1 сохранена. В общем workspace даже непересекающиеся file declarations исполняются последовательно: native broker разрешает весь bound workspace, per-file sandbox отсутствует. Вложенные roots, aliases, hardlinked/reparse declared files fail closed. App-host tools не confined этим contract.

Queue entry замораживает Task revision/scope, workflow/recipe, role/skill pins/dependencies/resources, session/binding и policy budget/hash до admission. Pending очередь не занимает hard WIP и не запускает agent. Coordinator пропускает заблокированную голову ради следующего допустимого entry; причины ожидания видны. Изменившийся Task scope либо authority требует нового preview. Изменение policy не расширяет уже замороженное разрешение. Admission атомарно связывает entry, recipe execution и обычный Task transition с повторной проверкой blocks/hard WIP/ownership. Повтор запросов не создаёт новые entries/runs.

Очередь и recipe имеют разные lifecycle: Pause очереди запрещает новые admissions; остановка admitted execution использует существующие recipe Stop/ACK/reconcile. Restart не повторяет неизвестный dispatch. Queued cancelled entry не затрагивает чужой execution. Public direct Send/recipe start не обходит reserved queue Task или physical workspace ownership.

## Границы, словарь и code-change contract

Scheduler bounded context владеет entry/order/wait reason/admission в `scheduler/*` и `/scheduler`; Recipe владеет steps/attempts/outcome в `execution-recipes/*`; Gateway владеет worker/job/broker lease в `runtime/app-agent-gateway.mts`; SQLite worker — CAS и atomic ownership/WIP/links. UI features/workflows использует только browser-safe contracts/client; source/private pins не отдаёт. Это operational state machine, отдельная DDD/FSD scaffold не нужна. Термины entry, assignment, ownership, hard WIP, dependency и pinned recipe трассируются в PAOS-0024, PRD§14 и соответствующие API/UI/owners выше.

- existing_capability: recipe freeze/resolver/admission, task-manager ordinary transitions, SQLite BEGIN IMMEDIATE/CAS/receipts, board WIP/links, safe file capture и existing App channel.
- smallest_safe_patch: durable queue перед recipe admission, private frozen admission seam; singleton gateway заменён bounded map только ради реальной независимой параллельности. Global permissions и policy schema не меняются.
- invariants: project concurrency1, whole-workspace exclusive writer, immutable pins/scope, no hidden fallback/replay, acknowledged Stop, owner acceptance отдельно.
- dependency_decision: no_new_dependency; installed Node/React и existing helpers.
- risk_selected_tests: queue HTTP RED404; distinct-root gateway RED runtime_busy; dependency/WIP races, blocked-head skip, exact pins, direct bypass, CAS/replay/restart, actual native barrier и browser queue path.
- comment_decision: intent comments у admission, physical ownership, recovery, stable requests и queue/runtime distinction.
- performance_applicability: finite entries/pins/active workspace bounds; workload SLO/token/cost не измеряются, cap и ошибки явные.
- evidence_and_gaps: source-backed contract before behavior implementation; current commands ниже. Rollback — только hunks этого slice, persisted records/old statuses не уничтожаются; без destructive Git/schema migration.

Business/product gates: существующие PRD/value являются входом, не новый market hypothesis. Analytics, discovery feedback, hosted release measurement и model-quality promotion not_applicable этому engineering slice; functional outcomes измеряются acceptance fixtures, human/commercial acceptance отдельно. AI model selection/prompts не расширяются; frozen context и routing сравниваются с existing manual/single-workspace baseline. Требуемые architecture/API/data/runtime/quality сведения хранятся здесь и в contracts/tests вместо дублирующих methodology-only файлов. Нет новых hooks/automation/provider/config activation.

## Acceptance: requirement → scenario → check → evidence owner

| Requirement / Given | When | Then / planned check | Owner |
| --- | --- | --- | --- |
| Queue без worker/policy | Просмотр | Пустой DTO,0dispatch; HTTP test | root |
| Два assignments, runtime занят | Enqueue | Обе frozen entries видны; pending не failed; sequential successor сам допускается | root |
| Первый entry blocked link | Coordinator tick | Следующий независимый entry допускается; новый block перед commit не обходится | root/SQLite tests |
| Hard WIP1, два запроса | Admission race | Один Task transition; второй waiting, никаких лишних runs | root |
| Пересечение Task/recipe ownership, alias/nested roots | Admission/direct Send | Shared root writer отклонён; disjoint roots допускаются под policy1 каждого | gateway + root |
| Registry/profile update после enqueue | Dispatch | Frozen bytes/version/workflow неизменны; Task scope drift требует re-preview | root |
| Lost enqueue/admit ACK, stale CAS/epoch, replay | Retry | Одна entry/execution, исходный receipt, conflict при другом payload | root |
| Restart/Cancel | Recovery | Unknown не replay; active child удерживает root до terminal ACK | root |
| Два distinct workspaces | Два native commands держат barrier одновременно | Actual parallel effects и deny outside own root; oneproject/root limit сохранён | root/native |
| RU/EN, desktop/mobile, keyboard/error states | Queue UI actions | Exact assignments, wait reasons, cap и stop outcome доступны | root/browser |

Non-goals: repair0025, metrics0026, external publication, provider credentials, arbitrary multiwriter в одном workspace. Элементы UI preview/enqueue/reorder/pause/cancel имеют отдельные сохранённые receipts. Evidence route — tests/web/scheduler*.test.mts, parallel-workspaces.test.mts и single-window/m3-queue-acceptance.mts; focused→full Web/TS/build→native/browser→Python/fixtures/transcripts/compatibility→docs/status gates. Ожидаются exit0/явные предусмотренные skips; failed setup не behavioral RED.

## Наблюдённые первые проверки

- HTTP queue test: корректный behavioral RED404 ROUTE_NOT_FOUND вместо200.
- Astra/medium gateway slice: корректный RED runtime_busy для второго distinct-root send; после bounded map barrier GREEN. Existing+parallel+recipe/autonomy60 passed, затем final parallel2/2 и tsc0; root full gates ещё обязательны.
- Root lifecycle guard отклонил readonly composite command после прошлого completion-ready marker, затем неправильный формат brief_digest; собственный marker обновлён под новый scope и корректный SHA256. Hooks/permissions не ослаблялись.

## Реализованный API и эксплуатационные границы

GET `/projects/:id/scheduler` возвращает queue revision, pause, order, public entries, wait reasons и capabilities. POST `/scheduler/preview` принимает recipe intent; `/enqueue` добавляет reviewed digest, expected queue revision, authority epoch и idempotency key. POST `/scheduler/{pause,resume,reorder,cancel,pause-entry,resume-entry}` использует тот же CAS/epoch/key и entryId либо полную перестановку pending order. Snapshot/preview не отправляют jobs. Direct Send и immediate recipe start не обходят reserved Task. Manual Task work остаётся отдельным разрешённым путём, изменение queued scope требует нового назначения.

Private `scheduler_entry` хранит frozen plan/pins; `scheduler_queue` — порядок/pause; отдельные receipts обеспечивают replay. Admission связывает entry/execution/Task одной SQLite transaction. Immutable workflow/recipe/version и current dependencies/WIP проверяются в worker, physical scope/CAS повторяются внутри transaction. Max32 live entries,200 retained entries и16MiB frozen queue state на проект; превышение явно отклоняется, история автоматически не удаляется. Один writer на workspace/project, до4 разных canonical roots. Pending entry не занимает WIP; semantic Task in_progress после завершения без перехода продолжает занимать свой WIP по board contract.

`heartbeat` добавляет `jobs[]` с сохранением legacy `job`; multijob consumer обязан обрабатывать каждый run и `cancelRequested`. `claim` может вернуть ранее выданный running job для lost-ACK replay: consumer различает runIds; optional `runId` выбирает exact replay. Один attached worker lease обслуживает несколько jobs; concurrent attach не выдаётся за поддержку независимых host identities. Model/profile pins являются frozen requested context, observedModel/effort остаются null. Этот slice не создаёт unattended App consumer/daemon.

Queue Pause запрещает новые admissions; ongoing execution не выдаётся за stopped. Cancel admitted entry использует recipe terminal evidence/reconcile. Restart сохраняет pending intent и переводит admitted unresolved work в recovery_required; неизвестный dispatch не повторяется. После завершения один workspace slot освобождается, следующий допустимый entry автоматически допускается. API/runtime unavailable остаётся ожиданием. Изменившиеся scope/policy/root/authority требуют cancel + новый preview.

## Проверки, failures и review

| Команда / сценарий | Наблюдённый результат |
| --- | --- |
| `node --test tests/web/*.test.mts` |443/443, skipped0, exit0; `.tmp/paos-m3-0024/web-full-final.log` |
| `npm run check:web-m1` |exit0; `.tmp/paos-m3-0024/typecheck.log` |
| `npm run build:web` |exit0,56 modules, `index-8qDxxLUQ.js`; `.tmp/paos-m3-0024/build.log` |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` |1450 /667.999s, OK(skip1); `.tmp/paos-m3-0024/python-full.log` |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` |91 expected outcomes, exit0; `.tmp/paos-m3-0024/fixture-eval.log` |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` |26/26, failed0, exit0; `.tmp/paos-m3-0024/transcript-eval.log` |
| `node --test tests/web/scheduler-capacity.test.mts tests/web/scheduler-runtime.test.mts` |7/7, включая five projects и physical aliases; reviewer rerun также7/7 |
| `node tests/web/single-window/m3-queue-acceptance.mts --synthetic-browser --binary <exact fixture> --playwright-core <installed> --chromium <installed> --screenshots <absolute>` |88 checks passed; `.tmp/paos-m3-0024/browser-evidence-mEIqoy/result.json` |
| `m3-queue-parallel-acceptance.mts --synthetic-queue-native --binary <exact fixture>` |49 checks passed; `.tmp/paos-m3-0024/parallel-evidence-YsTAWI/result.json` |
| `m3-queue-parallel-acceptance.mts --actual-app-queue --binary <exact fixture>` |46 checks passed; `.tmp/paos-m3-0024/actual-parallel-evidence-YJyW9x/result.json` |

Независимый `/root/queue_review`, GPT-6 Astra / medium, `separate_fresh_context`: P2 cap4 считал jobs, но не reserved executions; valid RED пять admitted вместо4. Coordinator и SQLite теперь считают physical workspace reservations; fifth остаётся queued и после terminal первого автоматически допускается. P2 drive-root prefix давал false для root/descendant; pure-function RED воспроизведён без реального root binding, исправлен через relative/isAbsolute. Бounded repair7/7 и UI review: открытых подтверждённых P1/P2 нет. Root self-review сверяет runtime/native/current full gates; review не является owner acceptance.

Дополнительные исправления текущего run: frozen historical profile сначала получал ASSET_RUN_PIN_INVALID после обновления registry. Recipe child теперь использует доказанные immutable durable pins, ordinary Send по-прежнему требует current profile; queue regression подтверждает v1 при current v2. Optional queueEntryId выявил hash(undefined) regression, исправлен только undefined representation. Первый full443 имел442 pass/1fail из-за порядка idle/ownership errors; прежний ACTIVE_RUN_RECONCILIATION_REQUIRED восстановлен перед новым cross-workspace guard, targeted4 и final443 passed. Test-only setup failures (не RED): invalid Task UUID, fixture input name collision, async callback syntax; их не считают feature proof.

Browser88: production build/pairing → Manual0 → recipe binding save/publish → queue pause → reviewed preview → lost enqueue ACK/retry → одна entry → второй pending → reorder/pause head → skip paused head → native build/review → successor Resume/automatic admission → четыре policy attempts → stale CAS negative → pending Cancel без run. RU/light1440×1000, EN/dark390×844, keyboard, no overflow; page/console/external requests0. Обе screenshots просмотрены root. Первое browser ожидание смотрело API completion раньше UI polling и встретило ожидаемый stale queue revision; fixture ждёт видимое completion перед Resume, source guard не ослаблен. Context7 supplied [official React cleanup guidance](https://github.com/reactjs/react.dev/blob/main/src/content/learn/synchronizing-with-effects.md); установленная React19.3.1, Playwright1.63.0/Chromium1223, без установки.

Native49 и actual46: два разных workspace jobs одновременно создали started markers и удерживали процессы на barrier; до release не было settled command receipts. Попытки записи в противоположный root получили EPERM, canaries неизменны. Queue Cancel B дал native exit1 и interrupted ACK; A остался running, после release создал `parallel-A`, exit0 и Task Review. B proof отсутствует и Done не выставлен. Native candidate/default discussion/planning/execution write/deny/temp/Stop/cleanup прошли; final adapter `d8311aa149804f07059bd23dfbdcabd4dd03f02f6bb84f8fce49805051983ddc`, Codex0.167.0 exact SHA `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`. Existing verified cache fixture использован без install/global repin.

Actual `/root/recipe_app_worker` прочитал два unique jobs, frozen builder/workflow v1 и declared checks, отправил обе команды до polling, обработал `heartbeat.jobs[]`. A `app-run-86d6fc254840c331c12a6233910ad1f549f1efd63425dd25b2c65fcd4de2fc78`: stdout DENY=EPERM/PARALLEL_A_OK,0; B `app-run-b6b1d5b793c0664c00d1375efaa5bc07e10005c1cd601ae2f89584a3206ee647`: DENY=EPERM,1, interrupted report. In-memory stdin bridge exit0/heartbeat stopped; capabilities/leases не выводились. Host identity attested, не cryptographic; нет external provider/API client или credentials.

Первый native fixture превышал existing500-char check limit; вместо изменения schema использован frozen `parallel-check.cjs`. Следующий fixture дважды обработал replayed claim одного run, поэтому не достиг barrier; исправлен consumer dedup по runId, не gateway replay contract. Failed receipts сохранены. Model-quality, cost/latency и широкая multi-project usefulness не измерены.

## Финальная синхронизация и состояние

`sync_task_documents.py . preview/apply` применил exact reviewed digest `sha256:a93777db87f28a5d89b355dcd2961514253c8c414ef40408c6fe09382d73b87d`, exit0. Recovery journal — `.codex/product-agent-os/compaction/a93777db87f28a5d89b355dcd2961514253c8c414ef40408c6fe09382d73b87d.json`. REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG обновлены; AGENTS не менялся, prod_test not_applicable — Batch39 не затронут. README и RU/EN registry синхронизированы. Final assess текущих source/target revisions: reviewed_inputs_valid, gaps[]; это integrity проверка явно рассмотренных фактов, не автоматическая semantic completeness.

До обновления REQUIREMENTS занимал39922 bytes. Полная явно историческая таблица Current Product-Agent OS State перенесена в существующий `research/product-agent-os-requirements-history-2026-11-10.md`:12773 точных UTF-8 bytes, SHA256 `2bfb5192749a4c5801c3bf92e1d68f2bb79d64cd8dca2a7ce6b0fa729ca55edc`. Source/destination before-images и preservation map — journal `3a66270c8fa1c58fb6648029e21d557d0cf4333c5d05c58b63ff4712e5109563`; финальное сравнение подтвердило исходные bytes/rows. Active scope, constraints и gates сохранены, task matrix не разделялась. Первое предложение переноса двух прошлых абзацев было отклонено link guard до записи из-за относительных ссылок; failed receipt сохранён, guard не менялся. После compaction105 docs tests passed. Итоговые размеры: REQUIREMENTS27574, PLAN30114, TEST33949 (warning32000), EVALS26174, RUNLOG27056; все ниже40000.

После task-card и control-plane sync выполнены:

- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q`:251 tests,21.125s, OK, exit0.
- `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py`: compatible, exit0; bounded local structure, не host/distribution acceptance.
- `python -B tools/check_docs.py`: structure checks passed, exit0.
- `validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` и `validate_task_state_consistency.py .`: ok/errors[], exit0. Второй проверяет свой legacy projection, а не заменяет отдельное сравнение Web matrix.
- `validate_hooks.py .codex/hooks.json` и `validate_hooks.py .codex/hooks`: ok/errors[], exit0; hooks не активировались и не менялись.
- Exact-card comparison: только PAOS-0024 стала implemented; другие55 MD cards byte-identical и55 JSON tasks structurally identical,56 tasks/12 groups, все estimates/order/groups сохранены. Generic completion helper не переписывался ради capitalized legacy card. Первый adapter preparation assertion остановился до записи из-за оставшегося старого имени evidence file; исправлен task-local adapter, setup failure не behavioral RED.
- Первый final diff-check нашёл blank line at EOF после точного переноса исторической таблицы. Вместо удаления её исходных bytes добавлена короткая provenance note после таблицы; final diff-check exit0, preservation slice остаётся byte-identical. После этой механической правки и создания results JSON финальная `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q`:105 tests,7.857s, OK, exit0.
- Final source/receipt/build hashes и runtime adapter проверены; native fixture binary удалён после exact SHA/containment проверки, browser/parallel fixture roots0. Installed runtime не менялся. Final `git diff --check` и safe source fingerprints записываются в [results JSON](product-agent-os-web-m3-0024-results-2026-11-12.json).

Strict MkDocs not_required: nav/diagrams/extensions/config/site не менялись; freshness site не заявляется. Broad Python1450/fixtures91/transcripts26 выполнены в этом run до финальных docs; affected251 выполнены после sync, implementation hashes с момента native/browser proof неизменны. Полные команды, exit codes, checks и безопасные receipt hashes собраны в results JSON; исходные failures остаются локальными receipts.

Closure: `implemented_locally_verified`. Блокирующих технических gaps для PAOS-0024 нет. Следующая PAOS-0025 «Исполнение, восстановление и отмена», dependencies0011/0024/0044 implemented; её расширенный recovery contract не присваивается этой задаче. Existing policy1/project, active App consumer, PAOS-mediated sandbox ceiling, human/commercial/release boundaries сохраняются. Git/history/publication, provider, credential, installation и system-policy actions не выполнялись. Rollback — только текущие изменённые файлы/hunks; recovery journals сохраняют before-images и отказывают при последующих изменениях.
