# PAOS-0037 — цепочки агентов и привязка к workflow

Source status: project-authored / current local implementation evidence, 2026-11-12. Human/commercial/release acceptance отдельно.

## Scope, контракт и решения

Владелец статуса — PAOS-0037 в [Web-плане](product-agent-os-web-task-manager-plan-2026-11-09.md) и [task-group JSON](product-agent-os-web-task-manager-task-group-2026-11-09.json). Зависимости PAOS-0036/0023 реализованы; следующий маршрут — PAOS-0024. Оценка20h сохраняется. Другие55 задач не входят в изменение статуса.

Execution recipe закреплена за transition опубликованного workflow. Manual выполняет обычный пользовательский переход без policy, worker, asset resolution или agent run. Recipe требует execution-сессию App, включённую политику PAOS-0023, точное назначение role→asset и доступную указанную version/hash. В этом срезе association transition ведёт в semantic category `in_progress`; цепочка работает внутри этой фазы. Произвольные новые фазы выполнения не объявлены поддержанными.

Версии workflow, recipe, profiles/skills с dependency closure и resource bytes замораживаются до admission. Managed historical versions и full source skill IDs поддержаны; unavailable/archived/sensitive/conflicting assets отклоняются. Requested model/effort — metadata, observed остаются null. Recipe не меняет host configuration или модель сама по себе.

Реальный scheduler расположен в `apps/local-service/src/execution-recipes/service.mts`; отдельный каталог `scheduler` не создан: дополнительный wrapper не давал отдельного контракта. Durable execution хранится как private settings, а каждый attempt — обычный App job. SQLite ownership fence удерживает Task между шагами; глобальный single-run guard сохранён. Private gateway admission не доступен через browser JSON. Обычный public Send сохраняет Ready gate.

Граф поддерживает последовательность, next branches, явные/выведенные joins и конечные циклы. Фактическая concurrency1. Проверяются unordered descendant writers: case, containment, вложенные ветви и неоднозначные Windows paths. Retry допускает только известный failed child, не interrupted/unknown; iteration/retry/timeout и общий policy budget ограничены. Checks требуют observed successful native operation, output artifacts — безопасное наличие/hash; worker prose не доказывает ни checks, ни Done. Initial input hashes входят в preview/start; downstream inputs сверяются с frozen initial/latest completed output.

Pause сначала сохраняет fence, затем запрашивает cooperative Stop. Terminal ACK показан отдельно. Paused execution с прерванным child не допускает Resume: отмена/сверка завершает его без повторного dispatch. Restart — `recovery_required`, без автоматического replay. Closed gateway inspection ждёт admission queue и ищет детерминированный child: активный child блокирует освобождение, terminal child либо подтверждённое отсутствие durable intent позволяют только cancellation. Ошибка чтения/неизвестный ответ без proof не выдаются за отсутствие запуска.

Success/failure targets проходят обычные agent transitions/guards. Done, Cancelled и human-only decision требуют пользователя; blocked guards дают `transition_blocked`, human target — `needs_user_decision`. Завершённая цепочка не равна принятой Task.

API: GET `/projects/:id/execution-recipes` и `/:executionId`; POST `/preview`, `/start`, `/:executionId/{pause,resume,cancel,reconcile}`. Start/controls используют CAS, authority epoch и idempotency key. Preview замораживает Task/workflow/assets/policy/input hashes. DTO содержит шаги, versions/hashes, граф, budgets, attempt/run IDs и outcomes; исключает private instruction content/resources. Browser хранит исходный запрос при lost ACK и повторяет тот же key. Редактор workflow содержит recipeId/successTarget/failureTarget; отдельный runner находится в Settings под редактором.

## Компактный code-change contract

- existing_capability: существующие App gateway/channel, PAOS-0023 autonomy owner, task-manager transitions, SQLite CAS/receipts, workflow registry, Team assets и safe file capture.
- smallest_safe_patch: добавить durable execution owner и private continuation seam; сохранить обычный public Send и существующие workflow guards. Canonical browser-only types вынесены в `packages/contracts/execution-recipes/recipe.ts`.
- invariants: один active native run, original Task scope, immutable pins, conservative budgets, no replay неизвестного исхода, approvals/owner decisions сохранены.
- dependency_decision: no_new_dependency; используются React19.3.1, Node26.5.0 и установленная инфраструктура. Context7: [официальная React effect cleanup guidance](https://github.com/reactjs/react.dev/blob/main/src/content/learn/synchronizing-with-effects.md).
- risk_selected_tests: Manual0; exact historical/source pins; replay/lost ACK; finite self/multinode loops; deep join; nested overlap; policy exhaustion/reset; pause/commands; artifact drift/check evidence; outcome targets; production UI/native journey.
- comment_decision: intent comments у private admission, stable command identity, durable scope/pins, serial recovery proof, UI request retention и polling.
- performance_applicability: bounded32 steps,1000 attempts,256 assets,8MiB pins, concurrency1; long-scale load/latency/token/cost не измерялись.
- evidence_and_gaps: local technical verification; claim ceiling — active App consumer и PAOS-mediated commands. App-host tools не confined этим contract; narrow paths/API route остаются недоступными согласно PAOS-0023.

## Acceptance и наблюдённые проверки

| Критерий | Наблюдённый oracle |
| --- | --- |
| Replay не дублирует run | start/report/command receipts; потеря HTTP ACK после commit → повтор исходного запроса → одна execution, два различных planned child runs |
| Bounded retry останавливается | failed retry и finite self/multinode cycles; exhausted policy не допускает следующий child и не создаёт новый budget |
| Parallel writers проверяются | deep unordered descendants, case/parent containment/Windows ambiguous paths; deep join ждёт обе ветви |
| Recipe не расширяет policy | immutable budget ID/hash, atomic start fence, reservation каждого attempt, retained command approval, policy cap и pause negatives |
| Manual не запускает agent | HTTP unit и production browser без policy/worker: переход выполнен, execution/run отсутствуют |

Текущий backend+HTTP recipe suite: `node --test tests/web/execution-recipes.test.mts tests/web/recipe-pins.test.mts tests/web/recipe-runtime.test.mts` —20/20 после review repairs. Независимый reviewer `/root/recipe_review`, GPT-6 Astra / medium, context `separate_fresh_context`: P2 shrinking-timeout replay и отсутствовавшие transition binding fields исправлены; recovery linking проверен. Открытых блокирующих findings в просмотренном scope нет; review не является browser/host/human proof.

| Команда | Результат текущего запуска |
| --- | --- |
| `node --test tests/web/*.test.mts` | final433/433, failed0, skipped0; `.tmp/paos-m3-0037/web-full-final.log` |
| `npm run check:web-m1` | exit0, `.tmp/paos-m3-0037/typecheck.log` |
| `npm run build:web` | exit0,55 modules, `index-zgfXGWZ1.js`; `.tmp/paos-m3-0037/build.log` |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` |1450 tests /623.013s, OK(skip1); `.tmp/paos-m3-0037/python-full.log` |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` |91 expected outcomes, exit0; `.tmp/paos-m3-0037/fixture-eval.log` |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` |26/26, failed0, exit0; `.tmp/paos-m3-0037/transcript-eval.log` |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` |compatible, exit0; local structure only |

Browser command: `node tests/web/single-window/m3-recipes-acceptance.mts --synthetic-browser --binary <exact-pinned-fixture> --playwright-core <installed-path> --chromium <installed-path> --screenshots <absolute-output>` — **57 checks passed**, `.tmp/paos-m3-0037/browser-evidence-3R26KQ/result.json`. Production UI → paired HTTP → Manual0 → recipe association save/publish → policy → execution binding → reviewed preview → edit invalidation → lost ACK/retry → existing App jobs → synthetic worker → explicit native approvals → actual write/read/checks/artifact → success target Review. RU/light1440×1000 и EN/dark390×844, keyboard focus; page/console/external requests0. Обе screenshots просмотрены root. Установленные Playwright1.63.0/Chromium1223 использованы без установки, Browser plugin unavailable.

Native candidate/default: discussion/planning/execution, allowed write/denied outside/temp, Stop и cleanup passed. Final adapter `2ca41cdcadb8bbf179a506999d52e70ad40d2d6043d88fa570b6c025e8b68a80`; Codex0.167.0 pin `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`. Manifest меняет adapterRevision и добавляет current candidate evidence, старые pins/evidence сохранены. Изолированная копия взята из проверенного существующего cache, без install/global repin. Installed npm binary не квалифицируется этим fixture.

## RED, failures и corrections

- Начальный behavioral RED Manual HTTP:404 `ROUTE_NOT_FOUND` вместо200; после backend GREEN.
- Reviewer P2: одинаковая command identity с shrinking timeout давала `app_agent_operation_conflict`; новый regression RED12/13, stable requested-timeout digest →GREEN13/13.
- Rejected admission при policy exhaustion оставлял Task owned: regression RED `RECIPE_RECOVERY_UNRESOLVED`; closed queue/durable lookup и cancellation-only proof →GREEN. Persisted child/lost ACK regression запрещает release active child, после terminal связывает существующий run без нового dispatch.
- Initial frontend build потянул Node-only type graph и выявил optional preview fields; browser-safe shared contract устранил это, build0. Зависимости не добавлялись.
- Первый full Web433 имел432 pass/1fail: asynchronous recipe startup после store close (`STORAGE_CLOSED`). HTTP factory теперь await initialized; targeted11/11 и full433/433.
- Browser setup failures сохранены: трёхбуквенный prefix `REC` вместо требуемого4; неверный test locator «Сохранить» вместо «Сохранить черновик»; конфликт route-fetch/abort fixture; поздняя fetch injection не затрагивала captured API client. Fixture исправлен: exact labels, handled response waits и init-script одноразовая потеря ответа. Эти failures не являются behavioral RED продукта. Два unhandled fixture runs оставили synthetic roots для последующего scoped cleanup.

## Остаточные границы и синхронизация

Recipe является bounded App-active execution, не background Desktop daemon. Нет автоматического wakeup закрытого App, provider/API fallback, host tool confinement, token/cost telemetry или автоматического product acceptance. General project queue/repair/statistics принадлежат PAOS-0024/0025/0026. Workload performance и модельное качество этим deterministic suite не оценены.

Owning machine evidence — [results JSON](product-agent-os-web-m3-0037-results-2026-11-12.json).

### Actual App-agent и control-plane

`m3-recipes-acceptance.mts --actual-app-recipes` — **46 checks passed**, `.tmp/paos-m3-0037/actual-evidence-iDVFs3/result.json`. `/root/recipe_app_worker`, GPT-6 Astra / medium, прочитал actual claim и frozen builder/reviewer profiles v1, выполнил два declared checks через existing pull channel и native broker после отдельных fixture approvals. Build: `app-run-e8fe6a69878954b7bd0ca56ad219bd9a599ccc39e4074bead77e17e9c6bd5044`, stdout `RECIPE_WRITE_OK`; review: `app-run-736b4cd35faf3d1dfb49b00e3e07adada2f41da191deba0f7797b1edba1af8f6`, stdout `RECIPE_REVIEW_OK`; оба exit0, terminal reports accepted. Переданный predecessor hash независимо сопоставлен с ожидаемым содержимым. Это проверяет потребление нового context и native effects, не качество модели на реальных проектах. Отдельного provider/API client/ключа нет; observedModel/effort null, host identity attested.

Первая попытка worker transport через `node_repl` дала EACCES до attach. Поддержанная bounded native escalation разрешила stdin bridge: capability/lease оставались в памяти, stdout их не содержал. После двух jobs heartbeat остановлен; disposable helper завершён. Этот отказ сохранён как boundary receipt, защиты не ослаблялись.

Control-plane sync5 sections: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG обновлены exact proposal `sha256:2c2c075c9445495e9922f5fd984d99984b23c73798c783febe42442622436c17`; recovery `.codex/product-agent-os/compaction/2c2c075c9445495e9922f5fd984d99984b23c73798c783febe42442622436c17.json`. Первый preview отказал удалению прежних evidence links/identifiers; следующий сохраняет исходные paragraphs с явной historical label. Apply exit0. Размеры: REQUIREMENTS39922, PLAN29513, TEST33309, EVALS25659, RUNLOG26420 bytes; warning32000 для REQUIREMENTS/TEST, hard40000 не превышен. Перед следующим расширением REQUIREMENTS потребуется lossless history redistribution. AGENTS/prod_test — no_change_needed: durable rules/Batch39 не менялись. Web README и RU/EN registry обновлены; MkDocs nav/extensions/диаграммы/site не менялись, strict MkDocs/site freshness не заявляются.

Все successful browser/native fixtures закрыты и очищены; два orphan roots failed browser harness удалены после exact containment/profile checks. Удаление затрагивало только disposable fixture Chromium, пользовательские приложения исключены.

### Финальный gate и сохранность

После docs sync и изменения карточки: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q` — **251 tests /33.545s, OK**, exit0; `.tmp/paos-m3-0037/post-sync-docs.log`. Docs checker, task matrix/task-state consistency, hooks JSON/directory validators и `git diff --check` — exit0. Финальный adapter hash совпадает с manifest. Browser/actual App source/build hashes заново сравнены с текущими файлами: mismatches[]. Full Python/plugin source не менялся; затронутые docs/lifecycle повторно проверены после окончательной синхронизации, предыдущий full не выдан за повторный запуск.

Только PAOS-0037 получила implemented: **другие55 MD cards побайтно прежние, другие55 JSON tasks равны, все56 задач/12групп/estimates/order сохранены**. Exact-card adapter сохраняет заглавные исторические Completion Report labels; generic updater не менялся. Recovery `.tmp/paos-m3-0037/matrix-recovery.json`, preservation `.tmp/paos-m3-0037/preservation.json`. PLAN current-state source pins относятся к другим матрицам и сохранены; Web task matrix не добавлялась в чужую projection.

Временный cached binary удалён после exact SHA/parent containment checks; receipt сохранён. Provider/credentials/Git/publication/deployment/install/system policy не использованы. PAOS-0037 закрыта технически; следующий PAOS-0024 имеет выполненные0037/0023 dependencies. При следующем расширении REQUIREMENTS39922 потребуется lossless перераспределение истории. Parent M3, human/commercial/release readiness этим срезом не закрываются.
