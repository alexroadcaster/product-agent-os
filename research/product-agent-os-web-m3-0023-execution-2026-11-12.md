# PAOS-0023 — политика автономности и лимиты

Source status: project-authored / implemented_locally_verified / synthetic production UI-HTTP-SQLite-native evidence, 2026-11-12. Human/commercial/release acceptance отдельно.

## Scope и решения

Владелец статуса — карточка PAOS-0023 в [Web-плане](product-agent-os-web-task-manager-plan-2026-11-09.md) и [task-group JSON](product-agent-os-web-task-manager-task-group-2026-11-09.json). Зависимости PAOS-0008/0013/0017 имеют implemented status; их Web API/contracts используются без нового runner. Следующий маршрут — PAOS-0037; остальные задачи не реализуются этим срезом. Оценка 12 h сохраняется как rough planning estimate.

Policy — отдельный project-scoped admission contract. По умолчанию политика отсутствует, ручная работа сохраняет прежний маршрут. Пользователь выбирает задачи, actions execution/command, число запусков, число допущенных команд на запуск, deadline и stop-on-failed-command. Сохранение проверенного preview оставляет policy paused; Resume включает только admission, не создаёт очередь и не повторяет runs. Каждый send по policy имеет явный `autonomy: true`; trusted gateway сохраняет budget pin. M3 recipes/scheduler подключаются к этому же contract позднее.

Scope `.` означает весь bound workspace. Narrow paths проверяются синтаксически, но preview показывает `AUTONOMY_PATH_BOUNDARY_UNAVAILABLE`, включение запрещено: существующий native broker не обеспечивает per-file sandbox. App-host tools не ограничиваются этим contract; обеспечивается только PAOS-mediated work. Token/cost metering недоступен; неизвестные поля budget отклоняются. Native command approvals остаются явными; UI не меняет host permissions, сеть, sandbox, модели или глобальный config. `local_api_byok` отвергает opt-in с `AUTONOMY_ROUTE_UNAVAILABLE`, автоматического fallback нет.

Budget reservation расходуется консервативно до dispatch и сохраняется в SQLite: неизвестный исход не возвращает бюджет автоматически. Operation IDs идемпотентны; declined/pending команды входят в command budget. Deadline включает approval waiting и действует как wall-time лимит admission/Stop; мгновенная остановка native процесса не обещается. Pause сначала сохраняет durable fence, затем запрашивает existing runtime interrupt. `stop_requested`, `cancel_requested` и `recovery_required` не равны terminal proof. При restart незавершённый run требует сверки и не переигрывается.

## План реализации и engineering contract

- Корневой агент владеет `packages/contracts/autonomy/policy.ts`, `apps/local-service/src/autonomy-policy/service.mts`, интеграцией `runtime/app-agent-gateway.mts`, refusal в `runtime/live-gateway.mts`, HTTP API и тестами `tests/web/autonomy-*.test.mts`; документацией, карточкой, JSON, runtime qualification и lifecycle.
- Независимый GPT-6 Astra / medium владеет frontend-файлами `features/autonomy/AutonomyManager.tsx`, `api/client.ts`, `ui/App.tsx`, `locales/messages.ts`. Другой read-only GPT-6 Astra / medium проверяет diff; root исправляет findings. Нет перекрывающихся writers.
- Leverage path: существующие SQLite Worker/CAS/idempotency, settings entities, App gateway serial queue, broker approvals/interrupt и React forms. Новый dependency не требуется. UI-only guard и второй scheduler отвергнуты как не обеспечивающие серверную границу.
- Bounded context: project policy → reservation → mediated command; invariants: permissions не расширяются, pause текущий, budget durable, replay не повторяет работу. Source terms TM-13/S23 отображаются в policy API, UI и guards. Новый domain modeling bundle не нужен: существующие PRD/architecture и эта карта покрывают один bounded slice.
- Component boundary: `features/autonomy` использует typed API/contracts; existing design system и RU/EN labels. Полный FSD/Storybook, OpenAPI generator, analytics и release measurement не применяются: нет нового framework, внешнего API, rollout или заявления о продуктовой эффективности.
- Rollback: вернуть только hunks PAOS-0023 и убрать добавленные файлы среза; существующие task/settings/runtime history сохраняются. Policy settings additive, destructive schema migration отсутствует. Прежний manual route не заменён.
- Verification: focused Node tests → Web regression/typecheck/build → synthetic browser/real offline native sandbox → required Python, fixture/transcript, compatibility/docs/lifecycle gates → task-matrix/status preservation и final diff.

## Acceptance traceability

| Requirement / правило | Given → When → Then | Проверка / evidence owner |
| --- | --- | --- |
| Preview policy объясняет возможности | Proposal → preview → видны scope, actions, бюджеты и ограничения; SQL/run не изменяется | `autonomy-policy.test.mts`; browser receipt |
| UI не расширяет host permissions | Unknown limits/unsafe paths/unsupported route → save/dispatch → invalid/unavailable, без native dispatch | contract tests; live gateway refusal; native receipt |
| Pause доступна | Queued/running/awaiting approval → Pause → durable fence, отмена pending actions, existing Stop; ACK отдельно | `autonomy-runtime.test.mts`; browser/native receipt |
| Бюджеты и deadline | Повтор message/operation → ровно одна reservation; exhausted/deadline → новая side effect запрещена | focused runtime tests; offline native case |
| Старый Pause не затрагивает successor | Pause(P) → Resume → новый run → retry P → successor продолжает работу | reviewer P2 regression, RED/GREEN |
| Restart/recovery | Закрыть gateway/store → открыть SQLite → pause/budget сохранены, прежний run recovery_required | реальный close/reopen test |
| Не-цели | Manual route / recipes / queue / provider inference | Existing manual regression; PAOS-0037–0026 остаются отдельными |

## Наблюдённые проверки и исправления

- Первые два запуска нового HTTP fixture имели setup failures (`PROJECT_IDENTITY_CONFLICT`, затем отсутствующий Host header). Fixture исправлен; они не считаются behavioral RED.
- `node --test tests/web/autonomy-policy.test.mts`: затем наблюдён корректный RED, exit 1, `ROUTE_NOT_FOUND` 404 вместо ожидаемого preview 200. После API/service — 3/3, exit 0.
- `node --test tests/web/autonomy-runtime.test.mts`: корректный RED на неподдерживаемом opt-in (`app_agent_input_invalid`); после integration GREEN. Ошибочный reset Task In Progress→Ready в тесте заменён отдельной Ready task, существующий workflow guard не изменён.
- Independent review `/root/autonomy_review`, context `separate_fresh_context`, GPT-6 Astra / medium: P2 старый Pause мог interrupt successor. Добавлен тест, наблюдён RED 1 вместо 0 interrupts; receipt сохраняет исходный cohort; исправление GREEN.
- `node --test tests/web/autonomy-policy.test.mts tests/web/autonomy-runtime.test.mts`: 11/11, exit 0 на текущем срезе после P2 repair, включая реальный SQLite close/reopen.
- `npm run check:web-m1`: первоначально TypeScript nullability/spread errors; исправлены function declaration/narrowing. Повтор exit 0.
- `npm run build:web`: exit 0, 54 modules, production bundle `index-CWjlzlFA.js` в этом промежуточном срезе; последующие изменения требуют нового build.
- Full Web под MXC: exit 1, 409 tests / 402 pass / 4 fail / 3 skip; link/symlink EPERM. Повтор с workspace TEMP: exit 1, 396 pass / 9 fail / 4 skip, те же filesystem setup restrictions. Сохранены `.tmp/paos-m3/web-tests.log` и `web-tests-workspace.log`; native retry запрошен через managed approval, guards не ослаблялись.
- Context7 `/nodejs/node/v26.0.0`, [официальный timers API](https://github.com/nodejs/node/blob/v26.0.0/doc/api/timers.md): проверены `setInterval`, `unref`, `clearInterval`; deadline watchdog не удерживает процесс, cleanup снимает timer. Не добавлены зависимости.
- Npm executable drift исследован read-only агентом `/root/autonomy_boundary_research`: найдены существующие cached 0.167.0 archive/member; SHA-512 integrity и exact member SHA-256 проверены. `python .tmp/paos-m3/prepare-native.py`, exit 0: isolated fixture `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`, 369062704 bytes. Сеть/установка/global repin отсутствуют; qualification ещё должна пройти на финальном adapter.

## Итоговые проверки

| Команда / проверка | Наблюдённый результат |
| --- | --- |
| `node --test tests/web/autonomy-policy.test.mts tests/web/autonomy-runtime.test.mts` | 15 passed, exit 0; дополнены concurrent last-budget, watchdog без UI/heartbeat, permission-boundary Stop и отказ API-route до RPC |
| `node --test tests/web/*.test.mts` | 413/413, skip 0, exit 0; native run с workspace TEMP/TMP, `.tmp/paos-m3/web-tests-final.log` |
| `npm run check:web-m1` | exit 0 на final implementation |
| `npm run build:web` | exit 0, 54 modules, final browser build `index-DhQVqT8h.js` |
| `python -B -m unittest discover -s tests -p 'test_*.py' -q` | 1450 tests / 638.427 s, OK (skipped=1), exit 0; `.tmp/paos-m3/python-full.log` |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | 91/91 expected outcomes, exit 0; `.tmp/paos-m3/fixture-eval.log` |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | 26/26, failed 0, exit 0; `.tmp/paos-m3/transcript-eval.log` |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | `compatible`, exit 0; local structure only, host/distribution не квалифицированы этим validator |
| `python tools/check_docs.py` | documentation structure checks passed, exit 0 |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json` и `.codex/hooks` | оба exit 0, errors []; hooks не изменены и не активировались |
| Task matrix и task-state validators | exit 0; финальный post-sync docs/lifecycle/template gate указан ниже |

После добавления permission-boundary Stop выполнен отдельный RED: запрет команды возвращался, но run оставался running. Минимальное исправление сохраняет stopReason; GREEN требует cancel_requested и zero broker calls. Это не изменение host permissions. Две поздние правки названий тестов уточняют отличие persisted state от настоящего close/reopen; поведение тестов не менялось, targeted suite повторяется в post-sync gate.

### Browser и native activation

`node tests/web/single-window/m3-autonomy-acceptance.mts --synthetic-browser --binary <absolute exact fixture> --playwright-core <installed absolute path> --chromium <installed absolute path> --screenshots <absolute visualization directory>`: final **47 checks, exit 0**, receipt `.tmp/paos-m3/browser-evidence-R1FHss/result.json`. Проверены production build → paired HTTP → policy editor → narrow-path refusal → preview invalidation → save paused → Resume admission-only → stale CAS с сохранением draft → execution/session opt-in → existing App gateway → synthetic worker claim → explicit native approval → actual command/file/output → Pause → pending command denied → cancel_requested → interrupted ACK. Task осталась In Progress, owner acceptance не выдумана. Viewports 1440×1000 RU/light и 390×844 EN/dark, geometry и keyboard focus, page errors/console errors/external requests — 0. Root просмотрел обе screenshots. После последнего source refinement browser/native gate повторён; промежуточный receipt `browser-evidence-wV33RB` сохранён с прежним provenance.

Installed Playwright core1.63.0 и Chromium1223 использованы без установки; Browser plugin not available. Приёмка использует новый synthetic worker, **actual App-agent/model reasoning не выполнялись**. Это проверка новой policy wiring и native effects; модельный контракт и выбор модели не менялись. Existing manual runtime регрессии входят в Web413; API-route negative test доказывает отсутствие silent fallback до создания RPC.

Final native source tuple: adapter `cb01327876c661be98d21ea35e680462a6abde1f374a5264015f84476ea85345`. Candidate и default loader прошли discussion/planning/execution, write inside/deny outside/deny temp, native Stop и cleanup. Receipts `.tmp/paos-m3/native-candidate-final.log` и `native-default-final.log`; exact hashes — [results](product-agent-os-web-m3-0023-results-2026-11-12.json). `qualified-manifest.json` меняет только adapterRevision и добавляет current candidate receipt hash, прежние evidence сохранены. Текущий npm binary заново прочитан: SHA-256 `6f65c42e3769209976cce097a400720b5d877e1d24ec8bb6272bf0f02d5e0fd7`, отличается от pinned `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`. Его qualification не объявляется, install/global repin не выполнялся.

## Review, синхронизация и сохранность

Независимый review `/root/autonomy_review`, GPT-6 Astra / medium, `separate_fresh_context`: один P2 исправлен; bounded повторное чтение подтвердило original-cohort Pause replay и реальный graceful SQLite close/reopen. Crash-kill этим тестом не заявляется. Root final self-review сопоставил acceptance, HTTP guards, source diff, native activation/negative route и требуемые gates. `tester_verdict=closed_allowed` только для local technical PAOS-0023.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG обновлены через просмотренный proposal `sha256:b2599bff77de0e38f45d2b698fdb7752fc2b8b02abb7baaffb5954fd22f488fb`. `sync_task_documents.py . apply ... --approved-digest ...` сначала получил permission denied на private writer.lock до изменения документов; bounded native approval разрешил только эти четыре sections и recovery journal. Итог exit 0, `.codex/product-agent-os/compaction/b2599bff77de0e38f45d2b698fdb7752fc2b8b02abb7baaffb5954fd22f488fb.json`. После stop-condition refinement текущий source digest повторно оценён: `reviewed_inputs_valid`, gaps [], no new section writes required. EVALS — no_change_needed: deterministic guard rubric достаточен, модельные prompts/selection/retrieval и качество не изменены. AGENTS/prod_test — no_change_needed, durable rules/Batch39 evidence не изменены. Web README и RU/EN registry обновлены; навигация, Mermaid, MkDocs extensions/site не менялись, strict MkDocs не требуется и свежесть site не заявляется.

Generic TaskCompletion updater оказался несовместим с заглавными labels исторического Web Completion Report (`task block missing field: status`); он остановился **до записи**. Новая plugin-логика в этот scope не добавлялась. Локальный exact-card adapter сохраняет текущий формат и сравнивает source bytes перед записью; recovery `.tmp/paos-m3/matrix-recovery.json`. После apply **другие55 MD cards побайтно идентичны, другие55 JSON tasks равны; 56 задач,12групп,оценки/порядок сохранены**. Receipt `.tmp/paos-m3/preservation.json`. Существующая чувствительность общего updater к регистру остаётся отдельным tooling follow-up; она не мешает переходу к PAOS-0037 через проверенный карточечный workflow.

Root budget: REQUIREMENTS39661, PLAN28971, TEST32589, RUNLOG25724 bytes после section sync. Все ниже40000; REQUIREMENTS и TEST выше warning32000. README root не менялся; pre-existing размер/старые receipts не выданы за новые green checks. Измеренный интервал начинается первым clock sample 12:37:57 MSK после discovery; индивидуальная active duration не измерялась, JSON duration=null намеренно. Финальный elapsed и provenance доступны в results.

PAOS-0023 закрыта технически; следующая PAOS-0037 имеет выполненные зависимости0036/0023. Остальные четыре задачи M3 остаются planned. Human acceptance, commercial/release и unrestricted unattended delivery не заявляются. Narrow paths, API opt-in, token/cost metering и собственные tools App host сохраняют явно показанные ограничения.

### Финальный post-sync gate и cleanup

После закрытия карточки и записи результатов: `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -q` — **251 tests / 20.045 s, OK, exit 0**; receipt `.tmp/paos-m3/post-sync-docs.log`. Final targeted Node suite15 passed, docs checker, task-state consistency и `git diff --check` — exit 0. Git сообщает только будущую CRLF→LF нормализацию, whitespace errors нет. Final browser source hashes заново сравнены с source/build: mismatches []. Изолированный cached binary удалён после проверки containment/parent/digest; private failed receipts, extraction integrity receipt и recovery bytes сохранены. Browser/service/native fixture roots закрыты и очищены; пользовательские приложения не завершались принудительно. Branch/stage/commit/push/PR/publication/deploy не выполнялись.
