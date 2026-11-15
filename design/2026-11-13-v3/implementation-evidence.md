# Внедрение UI-01–UI-12 — V3 и Sidebar collapse

Source status: local UI repair and visual comparison, 13.11.2026. Current result: locally_verified / needs_user_acceptance. Строгое пиксельное совпадение и новая пользовательская приёмка не заявлены.

## Повторная доработка — результат текущего среза

Перенесены рабочие композиции всех 85 продуктовых экранов V3: shell и sidebar, список/доска/полная карточка задачи, настройки задач, процессы, сессии, assets, генератор, документы, проверки, решения, autonomy, import/backup, dashboards и graph views. Два оставшихся route из 87 — component-lab и motion-lab альбома, не продуктовые разделы.

Исправления затрагивают `apps/web/src/design/{theme,workspace,parity}.css`, `ui/{App,Sidebar,Modal,Operations,ConnectionControls,SessionContext}.tsx` и presentation-компоненты `features/{tasks,workflows,sessions,team,skills,graph,artifacts,autonomy,decisions,dashboard}`. Статический diff для `apps/local-service` и `packages/contracts` пуст. Во время repair зависимости не устанавливались. Сохранены формы, обработчики, previews, подтверждения, CAS/revision и идемпотентность.

- Задачи: toolbar в колонке списка, компактный инспектор; одна форма в большом dialog по двойному клику, две колонки полей, контекст справа, закреплённые заголовок/вкладки/действия. Остались все 8 функциональных вкладок и отдельный экран расхода.
- Процессы: отдельные разделы вместо единой длинной формы, список состояний/переходов рядом с редактором, таблицы назначений/версий, двухколоночная миграция. Все поля остаются в исходной форме; hidden-панели не создают вторых редакторов.
- Сессии: список слева, рабочая область в центре, запуск/проверки/вопрос справа. Контекст и вопрос разделены; история открывает выбранную сессию, сохраняются anchors и поиск.
- Assets/документы: каталог и контекст справа, редактор и diff слева; генератор с тремя шагами; proposal/apply остаются отдельными действиями.
- Dashboards: 4 метрики, аналитика/очередь/нагрузка и таблицы; неизвестные показатели показываются как unavailable, не как ноль. Визуальные демонстрационные суммы не переносятся в реальные данные.
- Карта: D3, Mermaid и список с одним источником узлов; модуль, zoom и локальная прокрутка. Список ограничен по высоте рабочей области. Схема процесса первоначально вписывается целиком, кнопка 100% позволяет читать мелкие подписи.
- Обе темы: компактный ритм, двухтонные локальные SVG, общий набор borders/focus/disabled/notice. Sidebar216↔64, исходные spring constants, GSAP lifecycle и reduced motion сохранены.

## Поэкранный визуальный review

[Альбом сравнения](implementation-gallery.html) содержит V3 и actual app рядом, выбор всех 85 экранов, light/dark и полноразмерные PNG. [Машиночитаемый ledger](implementation-visual-review.json) перечисляет каждый экран, тему, hash изображения, audit и source hashes. Это статические изображения; анимации проверяются отдельно в приложении.

Root лично сопоставил все 170 состояний из `browser-evidence-V81wgT` с PNG V3: 29 сравнительных листов, дополнительно 13 листов нижних частей 37 длинных экранов; task overlay и runtime question проверены полноразмерно. После последнего исправления graph-list/workflow-diagram/asset editor повторены full capture и automated audit (`NqJx7X`), затронутые композиции вновь просмотрены в обеих темах. Для остальных неизменённых композиционных областей использован уже выполненный review; новые временные метки и fixture IDs не считаются изменением дизайна. Review mode: `self_review`; предыдущие независимые reviews не выдаются за review последней сборки.

За время сравнения исправлены: потеря начала dialog из-за autofocus, избыточные row grids редакторов, двойные заголовки, каталог с неправильной стороны, смешанные context/question/checks, нечитаемый масштаб Mermaid, цвет текста Mermaid в dark, растянутая таблица graph-list, duplicate asset IDs при скрытом втором каталоге. **Captured не использовалось как синоним reviewed.**

## Текущая проверка

| Проверка | Команда / receipt | Результат |
| --- | --- | --- |
| TypeScript | `npm run check:web-m1`; `.codex-tmp/v3-final-typecheck.txt` | exit 0 |
| Production frontend build | `npm run build:web`; `.codex-tmp/v3-parity-build.txt` | exit 0; JS `index-B7jp5dfA.js`, CSS `index-xRVpE75C.css` |
| Полный web suite | `npm run test:web-m1`; `.codex-tmp/v3-final-layout-tests.txt` | 500 passed, 0 failed/skipped; 56.512 s |
| V3 browser | `node --experimental-strip-types tests/web/single-window/m2c-browser-acceptance.mts --synthetic-browser --scenario ui-v3 --playwright-core <installed-playwright-core> --chromium <installed-chromium>`; `.tmp/paos-m2c/browser-evidence-NqJx7X/result.json` | passed, 378 checks; 170 captures; no page errors / external requests / root overflow / audited contrast findings |
| Existing team/workflow actions | `m2b-browser-acceptance.mts --synthetic-browser` with same browser arguments; `.tmp/paos-m2b/browser-evidence-UIqzYt/result.json` | passed, 51 checks; before final presentation-only graph/asset grid tweaks; command handlers unchanged |
| Task overlay | `m2-task-manager-browser-acceptance.mts --scenario task-overlay`; `.tmp/paos-m2/browser-evidence-gueRa6/m2-browser-result.json` | 19 passed; reused evidence for unchanged task handlers |
| Settings layout / CAS | `.tmp/paos-m2/browser-evidence-Z6vkxH/`, `.tmp/paos-m2/browser-evidence-ONAWBD/` | 14 / 17 passed earlier in this repair; later tables covered by V3 capture and M2b actions |

Installed paths: `C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core` and `C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe`. Runs use disposable loopback profiles; fixtures cleaned. No provider/model calls, real credentials or real project mutations. Generated skill, binding response and recipe recovery GET are explicit visual-only mocks listed in the receipt. They prove rendering, not provider execution.

Browser checks cover RU1280/1440/1920 and EN1440, both themes, 15 destinations; 85 internal product states at1440, keyboard tabs/dialog focus, Sidebar sizes/reduced motion, renderer activation and zoom. RGB contrast audit excludes native widget paint/gradients and does not establish full WCAG certification. Motion interpolation was observed earlier in this repair on actual Sidebar; the final automated run confirms endpoints/reduced motion. Static captures cannot prove subjective smoothness.

Intermediate failed receipts retained: sandbox symlink EPERM; build-inventory failure when tests overlapped rebuilding (stable rerun500); old harness navigation timeouts after pages split into tabs (M2b UIqzYt passed after explicit navigation); earlier Mermaid contrast/selector/duplicate asset failures. None is relabelled as a pass. The latest two final runs are successful.

## Различия и границы приёмки

| Область | Что отличается от демонстрационного V3 и почему |
| --- | --- |
| Метрики | API не даёт полноценные tokens/cost/tool_use. Карточки и chart frames присутствуют; вымышленные полосы/цены не добавлены. Сбор telemetry — отдельное функциональное изменение. |
| Наборы данных | Количество задач, статусов, агентов, узлов, документов и очередь определяются существующими источниками. Поэтому длина списков и геометрия графа не совпадают с примером. |
| Поля | Существующие metadata/confirmations сохранены даже там, где пример их опускает. Поля, не имеющие контракта (например, описание компонента или причина recovery), не добавлены как фиктивно работающие. Названия отдельных legacy полей сохранены. |
| Runtime | При неподключённом агенте question/run/checks показывают недоступность. Активный provider runtime не запускался. |
| Native controls | Select/file/multi-select сохраняют системную реализацию и клавиатурное поведение. Assignment mapping редактируется в строках таблицы; backend semantics прежние. |
| Настоящий профиль | Final dist проверен в synthetic service. Повторное управление существующей Chrome-вкладкой вернуло `Debugger unattached`; финальный reload этой вкладки не наблюдался. Для просмотра текущей сборки нужен reload по прежнему адресу `http://127.0.0.1:52961/`. Профиль не заменялся. |
| Производительность | Vite предупреждает о размере chunks: main716.04kB, CSS70.15kB, lazy Mermaid2852.57kB. Большие реальные проекты и длительное использование не измерялись. |

Статус UI-01–UI-12 в плане остаётся `in_progress` до отдельного решения по результату внедрения. Это не блокировка инженерных проверок и не заявление о незапущенных тестах: текущая реализация локально проверена, а полное соответствие ожиданиям владельца / UI-12 требует просмотра. Не объявляем все визуальные отличия автоматически принятыми.

## Синхронизация документов

PLAN/RUNLOG/TEST: обновить текущий срез и evidence pointer. REQUIREMENTS/EVALS: `no_change_needed` после уже внесённого в этом repair требования all-screen review, функциональные границы не расширены. `prod_test.md`: `not_applicable`, Batch39 не затрагивался. Документация API/architecture/source registry: `no_change_needed`, внешних продуктовых утверждений и контрактов этот repair не меняет. Старые отчёты ниже сохранены как исторические, их результаты не относятся к final build.

Документальные проверки текущего среза: docs unittest105 passed /14.747s до последнего root sync; check_docs OK. Matrix сначала выявил несогласованные статусы старых Completion Reports; после выравнивания на in_progress — ok (`.codex-tmp/v3-repair-matrix-final.txt`). Diff сначала выявил trailing whitespace в TaskManager.tsx; после удаления — exit0 (`.codex-tmp/v3-repair-diff-final.txt`). Изменение после сборки только whitespace, логика не менялась.

PLAN/RUNLOG/TEST применены через `sync_task_documents.py preview/apply` с проверенным digest `6878bf4da6dc19ee700c2ccf891824836f63dbf19c510bce5f807f4b80c45144`; receipt `.codex-tmp/v3-doc-sync-result-final.json`, status applied. Первая попытка apply получила Permission denied на локальном writer.lock; разрешённый escalated повтор прошёл. Старые receipts сохранены. Все три root файла ниже40000байт, предупреждения >32000 остаются.

Проверены340 локальных image links альбома и синтаксис его JavaScript (`node --check .codex-tmp/v3-gallery-script.js`, exit0). Все hashes final browser receipt совпали с файлами. Галерея отдельно не проверялась через браузер; интерактивность приложения проверена synthetic browser. Полный diff API/backend пуст. Финальное self-review: presentation-only changes, найденные ошибки исправлены; tester_verdict=partial_only для общей human parity acceptance, локальные automated gates passed.

Повтор mandatory docs gates после root sync: `PAOS_DOCS_SITE_DIR=.tmp/paos-m4-0030/site-final python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` — exit0,105 tests/12.645s/OK (`.codex-tmp/v3-repair-docs-postsync.txt`); `python tools/check_docs.py` — exit0/OK (`.codex-tmp/v3-repair-check-docs-postsync.txt`); `git diff --check` — exit0 (`.codex-tmp/v3-repair-diff-postsync.txt`). Использован существующий site fixture; свежесть MkDocs site не заявлена, nav/config/публикуемый site этот срез не менял.

## Исторические записи предыдущего внедрения и промежуточного repair

Source status: 13.11.2026; V3 parity repair in_progress. Предыдущая реализация возвращена на доработку; старые receipts ниже являются историческими, не доказательством текущего соответствия V3.


## Повторная доработка V3 — текущий незавершённый срез

Владелец потребовал строгое соответствие всех экранов, не CSS поверх старой структуры. UI-01–UI-12 reopened. Изменены сетки задач/редактора/overlay, внутренние вкладки, dashboard compositions, settings navigation, каталоги assets, sessions, документы, autonomy, decisions, import/backup и процесс master/detail. API/backend/contracts не менялись. Новые зависимости не устанавливались.

Текущие проверки (до полного визуального review):

- `npm run check:web-m1`: exit 0 после структурных правок.
- `npm run build:web`: exit 0; последняя сборка main 691.42 kB / gzip 211.72 kB, CSS 50.26 kB. Bundle warning сохраняется.
- `npm run test:web-m1`: sandbox attempt failed на создании symlink fixtures (EPERM); повтор с теми же тестами вне sandbox: 500 passed, 0 failed, 0 skipped, 50.704 s. Receipt `.codex-tmp/v3-parity-tests-unsandboxed.txt`.
- `m2c-browser-acceptance.mts --scenario ui-v3`: первый запуск sandbox завершился до браузера; второй дал 43 checks и timeout положения подсветки. Исправлены дробные координаты Sidebar. Повтор: 356 passed, `.tmp/paos-m2c/browser-evidence-fAceOh/result.json`. Этот прогон предшествует последним изменениям workflow/toolbar и не закрывает весь V3.
- `m2-task-manager-browser-acceptance.mts --scenario task-overlay`: RED на скрытом accordion noRisks после переноса формы; сценарий обновлён на явное раскрытие. Повтор выполняется; успех не заявлен.
- CUA: Chrome, существующий Neural_Flow, после reload наблюдается новая композиция overview в тёмной теме. Проектные данные не изменялись.

Визуально просмотрены текущие overview, tasks base, general settings и workflow baseline против соответствующих PNG прототипа. Найденные расхождения вызвали перенос toolbar в левую колонку, выравнивание navigation слева, удаление двойного overview heading и замену workflow accordion grid на master/detail. **Полное сравнение всех экранов и обеих тем ещё не завершено.**

Незакрытые проверки: current expanded capture run, all-state review, task/settings/team functional regression, документы/gates, финальная активация и пользовательская приёмка. Generated skill/recipe recovery и provider-dependent states требуют синтетических fixtures; вызовы провайдеров не разрешены и не нужны.

## Границы и baseline

Разрешён frontend presentation в apps/web и его проверки. Backend/API/schema/permissions/providers/queue semantics не меняются. Synthetic prototype figures не переносятся в actual app. TaskManager snapshot — источник task counts; teamMetrics даёт partial observed runs и null duration/token/cost; tool_use отсутствует. Graph — доступная revision-pinned page, не гарантированная полная карта репозитория.

Исходное дерево: React19.3.1, Vite8.3.8, TypeScript7.0.2; зависимости приложения только react/react-dom. Старые theme.css и app.css дают тёплую палитру и длинные панели. App содержит 14 sections, navigationEpoch, project registration fence, runtime polling и session anchors — сохранить. TaskManager имеет 8 вкладок, command guards и module navigation cache; Editor владеет drafts/preview/revision conflict. Новый overlay не должен создавать второй редактор.

Ownership: root — план, tokens/shell, integration и проверки. Read-only ui_impl_inventory — источники и команды; без edits. Чужие startup/settings/research hunks и foreign lifecycle marker сохраняются. Срезы и разрешённые файлы назначаются до делегирования. No Git/production/provider actions.

## Последовательность и критерии

UI-01 baseline → UI-02 tokens/primitives → UI-03 shell → UI-04 tasks → UI-05/06 settings/workflows → UI-07 sessions → UI-08 team/graph/artifacts → UI-09 dashboards/service surfaces → UI-10 motion/a11y → UI-11 combined checks → UI-12 implementation handoff и отдельная owner acceptance.

Утверждённый DESIGN имеет приоритет над Hallmark defaults: Sidebar width spring разрешён явно; desktop-only, реальные данные без invented metrics; no theme draw/reapproval. Chart family — zero-based bars/progress и node-link, React владеет data/state, D3 геометрией, Mermaid отдельным lazy renderer; table/list fallback сохраняется. Page-instance count bounded; renderer cleanup обязателен, new telemetry backend исключён.

## Проверки и результаты

Baseline команды и последующие receipts записываются здесь. Прототипные проверки V3 не считаются actual app verification.

## Code-change contract — UI-01–UI-12

- existing_capability: React refs/effects, native dialog, existing draft registry, complete taskManager snapshot, scheduler/teamMetrics and revision-pinned graph APIs. Existing client, policy and command handlers reused. Scope inventory above read before edits; this compact record consolidates those decisions during review.
- smallest_safe_patch: frontend adapters/components and styles around existing forms; API/server/contracts/storage excluded. One persistent task editor promoted with showModal; settings/workflow panels remain mounted.
- invariants: CAS/idempotency/preview/confirmation/navigationEpoch/polling and parent-task semantics unchanged; no fabricated telemetry, no remote data egress. Static graph coverage remains explicit.
- dependency_decision: approved local UI dependencies reused from the approved V3 set: D3 7.9.2 geometry, GSAP 3.15.1 lifecycle, Mermaid Tiny 12.3.0 lazy local renderer. Sidebar uses native rAF, task overlay native dialog; no new UI framework. package-lock pins versions; rollback removes these UI imports/package additions only. No global installation. Duoicons local SVG subset retains MIT notice.
- risk_selected_tests: task overlay and settings browser RED→GREEN, dashboard count/assignment invariants RED→GREEN, existing task/team/workflow/graph/artifact journeys, full web tests and typecheck/build; both locales/themes desktop screenshot/contrast/focus checks. Runtime synthetic, human acceptance separate.
- comment_decision: comments on animation physics/cleanup, async projection/cancellation, graph strict IDs, unique task workload, denominator and persistent editor; obvious event setters need no narration.
- performance_applicability: required; bounded three portfolio workers, stopped deterministic <=100-node force layout, local Mermaid lazy script, no idle sidebar frames. Bundle warning retained, no unsupported latency claim.
- evidence_and_gaps: proceed; installed Node/React/Vite and current dist receipts. No provider/host usage telemetry, no mass-data benchmark or human implementation acceptance. Owner root; source-owned implementation plan/evidence, no second state ledger.

## Текущее внедрение и проверка

Исходники: `apps/web/src/design/{theme,workspace}.css`, `ui/{App,Sidebar,Icon,Modal}.tsx`, `ui/settings-workspace.css`, `features/tasks/{TaskManager.tsx,task-detail.css}`, `features/workflows/{WorkflowManager.tsx,workflow-workbench.css}`, `features/dashboard/{Dashboard.tsx,model.ts}`, `features/graph/{GraphExplorer,GraphViews}.tsx`, `features/graph/diagram-source.ts`, `features/team/TeamManager.tsx`, `features/sessions/SessionsCatalog.tsx`, `main.tsx`; локальные package/lock и THIRD_PARTY_NOTICES. Backend/API/contracts/storage не изменены.

| Проверка | Результат текущей сессии | Receipt |
| --- | --- | --- |
| `npm run build:web` | exit 0; main 677.90 kB / gzip 208.82 kB; Mermaid lazy asset 2852.57 kB | implementation-build.txt |
| `npm run check:web-m1` | exit 0, повтор после review fixes 14:43 UTC | implementation-typecheck.txt; текущий terminal receipt |
| `npm run test:web-m1` | 500 passed, 0 failed, 0 skipped; 55.299 s | implementation-tests-final.txt |
| Task overlay | 19 passed | implementation-overlay.txt; .tmp/paos-m2/browser-evidence-mwwUmd |
| Task integration | 112 passed | implementation-integration.txt; .tmp/paos-m2/browser-evidence-hQObxR |
| Settings layout | 14 passed после исправления раскрытия | implementation-settings-final.txt; .tmp/paos-m2/browser-evidence-4MXMJk |
| M2b team/workflows | 51 passed | implementation-team-workflows.txt; .tmp/paos-m2b/browser-evidence-e9GHSr |
| M2c graph/artifacts | 37 passed | implementation-graph-artifacts-rerun.txt; .tmp/paos-m2c/browser-evidence-yrETwY |
| Accessibility core | 136 checks / 20 views passed | implementation-accessibility.txt; .tmp/paos-m4-0029/browser-evidence-pqJ4JN |
| Final V3 | 356 checks,120 views,70 captures; zero findings/pageErrors/externalRequests | implementation-v3-browser-final-verified.txt; implementation-browser-result.json |

Последний V3 run: 14:37:29–14:38:16 UTC, production build current, fixture cleaned. RU: 1280/1440/1920 × обе темы ×15 destinations; EN:1440 × обе темы ×15 destinations. Дополнительно все8 task tabs,6 settings tabs,7 workflow tabs, D3/Mermaid same module/nodes и специальные имена `$foo`, `#private`, Sidebar216↔64, route persistence, reduced motion и keyboard. [Галерея](implementation-gallery.html) содержит реальные captures этой сборки. Root визуально проверил final light overview и dark task overlay; независимый review проверял более ранний current-build набор L9fQVm. Автоматический RGB contrast audit не включает gradients/native widgets и не является WCAG-сертификацией или ручным screen-reader audit.

Воспроизведение browser checks: `node tests/web/single-window/m2-task-manager-browser-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path> --scenario task-overlay` (также settings-layout/integration); `node tests/web/single-window/m2b-browser-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path>`; M2c аналогично с `--scenario ui-v3` либо существующим full scenario. Accessibility: `node tests/web/accessibility/browser-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path> --screenshots <absolute-output> --scenario core`. Использованы Playwright core из npm cache `eb7983f9b02fb67f/node_modules/playwright-core` и Chromium1223 из local ms-playwright. Disposable profiles, loopback only; provider calls/real credentials отсутствуют.

## Review и исправления

Один independent fresh-context review `/root/ui_implementation_review`, verdict fix, две P2: inherited agent IDs ломали plain-object assignment map; Mermaid sanitizer терял часть исходных имён. Root исправил Map/Object.fromEntries + own-property access и decimal-entity encoding с synthetic IDs/strict security. Обе регрессии подтверждены assert RED → GREEN; итоговые500 тестов и356 browser checks выполнены после исправлений. Root self-review подтверждает repair disposition; повторный независимый review после repairs не заявляется. Builder `/root/task_ui_builder` отвечал за задачи, затем settings/workflows последовательно; `/root/ui_impl_inventory` — read-only inventory. Три agent spawns, непересекающееся владение.

Сохранены реальные неуспешные попытки: sandbox baseline486pass/6fail/3skip (symlink/profile filesystem restrictions), исходные contrast findings68humB и graph-test timing; последующие разрешённые synthetic runs прошли. После review HmySvl обнаружил неверное test innerText на SVG, vIYz2w — race сброса query в тесте; test исправлен на textContent и ожидание завершения query/module render. Исторические receipts не перезаписаны успешными результатами.

## Ограничения и handoff

- Tokens, cost, tool_use не измеряются доступными API и показаны unavailable. Нулевые или демонстрационные значения не подставляются; backend telemetry отдельно вне scope.
- Agent workload — число открытых назначений, observed runs — доступные события за7дней; ни один показатель не объявлен процентом фактической занятости.
- D3/Mermaid показывают одинаковые первые100 узлов доступной revision-pinned страницы; module filter применяется к ней. Полный список доступной страницы сохранён. Весь репозиторий без ограничения API не заявлен.
- Bundle >500kB warning сохранён; Mermaid lazy-loaded locally. Масштабное production performance измерение не проводилось.
- Обычная локальная сборка обновлена; пользовательский service/profile не перезапускался. Автоматическая проверка использовала synthetic fixtures. Git/публикация отсутствуют.
- UI-12: требуется просмотр реализации владельцем; утверждение V3 не заменяет её приёмку. Все изменения откатываются собственными frontend/dependency hunks, без DB migration.

## Control-plane sync

REQUIREMENTS: updated — approved presentation scope/non-goals. PLAN: updated — UI sequencing/status/rollback. TEST: updated — команды/current evidence pointer. EVALS: updated — numeric truth, render coverage и ceiling. RUNLOG: updated — current handoff. DESIGN, task matrix, app README, RU/EN source registry и notices updated. `prod_test.md`: not_applicable — Batch39 evidence не затронут. AGENTS/config/hooks/runtime instructions: no_change_needed. Все root-файлы ниже40000 UTF-8 bytes; TEST39508 bytes, warning accepted, переполнение отсутствует. Strict MkDocs not_applicable: nav/config/site Markdown rendering не менялись; app Mermaid — отдельная frontend поверхность. Подробные receipts остаются здесь; корневые документы содержат ссылки.

## Финальные документационные gates

`PAOS_DOCS_SITE_DIR=.tmp/paos-m4-0030/site-final python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`:105 tests,21.475s,OK (существующий site fixture; свежесть site build не заявлена). `python tools/check_docs.py`:OK. `python plugins/product-agent-os/scripts/validate_task_matrix.py design/2026-11-13-v3/implementation-plan.md`:ok. `git diff --check`:exit0; только Git CRLF conversion notices. Реализация UI-01–UI-11 закрывается локальными gates, UI-12 остаётся in_progress.

Матрица исторически находится под design/, который completion helper не принимает (разрешены docs/planning,docs/superpowers,research); она обновлена и валидирована на месте, без переименования/дубликата. Синхронизация финальных PLAN/RUNLOG выполняется reviewed section patch через sync_task_documents с CAS/recovery. Это локальный UI handoff, не новая инструкция и не runtime activation claim.

Финальный PLAN/RUNLOG section apply: applied digest `sha256:953ca50407bb77aa853f698840c3ea3ebad9ed4e80812ef92b4fbb478b8bbd4e`; before-images и CAS journal остаются в локальном recovery storage. Первый preview отказал из-за удаления исторического UI-10 identifier; identifier сохранён, следующий reviewed preview прошёл.

Sync apply initially received filesystem permission denial for the protected recovery lock; approved elevated local retry then detected a stale evidence revision. Regenerated proposal retained byte-identical reviewed PLAN/RUNLOG diffs; final apply returned applied/documentation_ready. No guard was bypassed or weakened.

После финального PLAN/RUNLOG apply docs suite повторён: 105 tests / 17.240s / OK (`implementation-docs-tests-final.txt`). Task matrix validator и diff check exit0; check_docs OK. SHA-256 исходников и dist из browser result совпадают с финальными файлами. Diff для apps/local-service и packages/contracts пуст. Root size gate: REQUIREMENTS31901, PLAN35265, TEST39508, EVALS29899, RUNLOG33438 bytes — все ниже40000. Combined evidence/marker patch отклонён lifecycle hook; записи разделены, marker меняется только для текущей сессии.

## UI-12 — запуск для приёмки 13.11.2026

По явному запросу владельца выполнен actual restart того же профиля `manual-review`, без изменения project data. CIM подтвердил launcher11440/service21204 и точный profile argument. Через Chrome Settings → Локальный сервис → подтверждение → Завершить запрошен штатный Quit. После него Get-Process не вернул оба прежних PID, endpoint.json отсутствовал (Test-Path=False). Start-Process node apps/launcher/main.mts с тем же --profile, Hidden, process-local PATH normalization:exit0, новый launcher14372. Новый endpoint имеет другую instance identity и порт52961. Chrome открыл `http://127.0.0.1:52961/`, виден Neural_Flow / Обзор, новая навигация и V3 dashboard. Пользовательский service оставлен работающим, вкладка markDeliverable.

Actual Sidebar check: reducedMotion=false; наблюдались промежуточные ширины и spring settling к64px при collapse и216px при expand. Root overflow=false; captured console errors=[]; final screenshot визуально просмотрен. Тема осталась системной (фактически тёмной), настройки не сохранялись. Задач в текущем проекте0, dashboard корректно показывает empty. Human acceptance по-прежнему pending; успешный перезапуск не закрывает UI-12.

Первоначальное browser-extension navigation /launch получило ORIGIN_REJECTED; штатный native Chrome navigation успешно открыл protected bootstrap без изменения guards. Несколько bootstrap-marker попыток отклонены hook из-за отсутствия shown field в точном patch/неподдержанного порядка Set-Content arguments; после чтения действующего parser использован документированный single-marker patch со scope_note_shown. Защиты не изменялись. Обычный CIM в sandbox был недоступен; elevated read-only CIM прошёл. Git/provider/forced termination отсутствуют. Control-plane sync: no_change_needed для REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG — scope и UI-12 pending сохраняются; только дополнительный actual restart receipt в owning evidence.
