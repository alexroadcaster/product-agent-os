# PAOS-0029 — Доступность, языки и темы

Source status: project-authored / bounded local technical verification, 2026-11-12; final receipts in companion results JSON.

## Scope и pre-edit plan

Baseline HEAD `668461ca77caad7955ff7f8346b944b04de1d799`, clean worktree; start15:54:48UTC /18:54:48MSK. PAOS-0029/M4/order52 depends0028 implemented. Acceptance:26screens S01–S26 плюс task tabs, RU/EN×Light/Dark, keyboard Kanban/workflow и длинные значения/narrow layout без потери actions. Остальные55cards/estimates/order/groups сохраняются. Root sole writer; bounded read-only `/root/accessibility_mapping` GPT-6 Astra/medium исследует blocker proposed-route/current-component mapping. One independent review window later. Provider/runtime/backend authority unchanged.

Canonical sources: task card, `research/product-agent-os-web-task-manager-screens-2026-11-09.md`, `apps/web/src/design/{theme,app}.css`, `apps/web/src/ui/App.tsx`, existing feature modules, locales и tests/web/single-window. Existing combined views are mapped to screen IDs; proposed `/p/:project/...` routes are not falsely tested as implemented URLs. Native input/select/button, native dialog, existing React/Playwright and project fixtures preferred; axe/browser plugin not installed, no new dependency/install. Audit uses rendered computed styles, native accessible tree/names and bounded keyboard interactions, with explicit coverage limits.

Owned tests `tests/web/accessibility/browser-acceptance.mts` and helpers, relevant tests/web regressions; frontend CSS/locales and affected component seams only; `docs/web/accessibility.md`, Web README, source registryRU/EN, control-plane five sections, own report/results and0029MD+JSON. Forbidden: backend authority, generic permission changes, providers/credentials/Git/install/publication, unrelated cards/source fixtures. Backend/native/model gates not_applicable absent source changes; current frontend/browser/docs gates mandatory. Reuse unchanged broader evidence only with original provenance, never call it newly run.

| Requirement / Given | When | Then / independent check | Owner |
| --- | --- | --- | --- |
| S01–S26 current UI | RU/EN×light/dark | Named actual state/entry; meaningful content, labeled enabled controls, no framework/page/console error | root/browser |
| Task tabs and Kanban | Keyboard only | Focus/selection semantics, same transition guard, no drag-only action | root/browser |
| Modal target choice | Open/Tab/Shift+Tab/Escape | Initial focus inside, bounded tab cycle, restore focus, no background action | root/browser |
| Workflow editor | Keyboard inputs/preview/error | Accessible names, preserved draft and actionable error; no stuck Loading after failure | root/browser |
| Long title/path/ID/paragraph | 320/390px and desktop/zoom-equivalent | No page-level horizontal overflow or lost controls; code/table/graph internal scroll explicit | root/browser |
| Light/dark rendered text | Compute foreground/background | 4.5normal/3large minimum, inactive/logotype exceptions explicit; no rounding pass | root/browser |
| Controls/focus/forced colors | Keyboard / high contrast | Visible non-obscured focus, identifiable controls, no color-only state | root/browser |
| Loading/empty/error/unavailable | bounded synthetic HTTP fault | Distinct localized state and recovery action, not success fabrication | root/browser |
| Screen reader semantics | Native roles/names/tree | Automated semantic checks + keyboard proof; no unsupported manual assistive-technology certification | root |

Compact code contract: existing_capability=existing CSS tokens/native HTML/React/accessibility semantics and installed Playwright1.63/Chromium1223; smallest_safe_patch=localized labels/focus/modal/overflow changes after RED; invariants=business guards, draft/retry envelopes, stable IDs and user-authored strings preserved; dependency_decision=no_new_dependency; risk_selected_tests=rendered behavior and keyboard/contrast oracles, focused Node contracts and full Web regressions; comment_decision=state/focus/scroll intent only; performance_applicability=no workload/SLO claim; evidence_and_gaps=current matrix required, genuine failures retained. Native dialog is preferred over a custom focus-trap framework if a modal defect is reproduced.

Plan quality: exact commands `node tests/web/accessibility/browser-acceptance.mts --synthetic-browser --playwright-core <verified existing absolute path> --chromium <verified existing absolute path> --screenshots <permitted visualization directory>`; `node --test tests/web/*.test.mts`, `npm run check:web-m1`, `npm run build:web`; docs105/lifecycle251, check_docs, hooks/matrix/compatibility/eval as TEST routes, strict MkDocs if nav changes. Expected exit0/no unresolved required findings; source-bound artifacts and fixture cleanup. Rollback only current hunks. New ADR/DDD/FSD scaffold/CI/analytics/product-discovery/model-evals/release promotion not_applicable: existing UI boundary and technical accessibility task. Relevant design/API/quality/privacy/claim gates live here and existing tests, no duplicate methodology-only artifacts. Root evidence owner, no placeholder readiness claims.

Applied skills: canonical implementation-planner, frontend-testing-debugging (Browser plugin absent→existing Playwright), React best-practices advisory. Source policy/complexity frontend/testing routing and coding-standard compact contract reused from current checked workspace. Official [WCAG2.2](https://www.w3.org/TR/WCAG22/) informs contrast4.5/3 and reflow320CSSpx; this is a bounded technical evaluation, not full WCAG conformance certification. Context7 `/microsoft/playwright/v1.63.0` [roles and accessible names](https://github.com/microsoft/playwright/blob/v1.63.0/docs/src/locators.md) / ARIA snapshots / forced-colors testing. No secrets/raw private logs in reports; synthetic data only. Human acceptance separately owned.

## Реализация и соответствие acceptance

`apps/web/src/design/theme.css` отделяет декоративный rule от границ активных полей: новый control-rule проходит3:1 на обеих темах. `app.css` сохраняет accent фон primary при hover; задаёт min-width:0/max-width:100% и перенос длинных значений в существующих grid/flex контейнерах. Header сохраняет кнопки, сокращая длинный breadcrumb с полным title. Внутренняя горизонтальная прокрутка Kanban/графа остаётся доступной; глобальный overflow:hidden не используется для сокрытия actions.

`ui/Modal.tsx` использует native dialog/showModal: модальность, Escape/cancel, исходный opener и его восстановление; граничные Tab/Shift+Tab не уходят в browser chrome. TaskManager использует этот компонент вместо div role=dialog и даёт доске focusable region с локализованным именем. `App.tsx` даёт transcript имя/tabIndex, связывает Menu с navigation, закрывает mobile disclosure по Escape и при выходе фокуса; при выборе раздела с мобильного меню фокус переходит к main. Бизнес-переходы и guards сохранены.

`WorkflowManager.tsx` именует recipes textarea, отличает загрузку от unavailable после ошибки. `TeamManager.tsx` также устраняет stuck Loading; значения asset-action сохраняют schema values при локализованных подписях. `ArtifactExplorer.tsx` локализует типы фильтра с явным value. Пользовательские тексты и machine identifiers не переводятся. Новых npm/Python dependencies нет.

| Screen | Реальный entry/state production UI |
| --- | --- |
| S01 | Shell, project selector и мобильная навигация |
| S02 | Settings: создание/подключение проекта |
| S03 | Overview: реальные heading и Task details после загрузки |
| S04 | TaskManager: список |
| S05 | TaskManager: Kanban, keyboard scrolling и карточки |
| S06 | Выбранная задача и панель деталей |
| S07 | TaskEditor существующей задачи |
| S08 | SessionsCatalog с синтетической сессией |
| S09 | Открытая сессия, composer и длинный transcript |
| S10 | Каталог агентов с управляемым профилем |
| S11 | Профиль агента, source/content/dependencies |
| S12 | Редактор управляемого агента |
| S13 | Agent generator, description form; provider не вызывается |
| S14 | Каталог skills |
| S15 | Профиль и редактор skill |
| S16 | Skill discovery, source path form; install не выполняется |
| S17 | Skill generator, description mode; provider не вызывается |
| S18 | GraphExplorer с реально перестроенным lexical индексом |
| S19 | ArtifactExplorer: документы |
| S20 | Выбранный синтетический PLAN.md в reader |
| S21 | Check details с явно синтетическим evidence, не execution receipt |
| S22 | Выбранное product decision и детали |
| S23 | Загруженная autonomy policy на паузе, selected allowed task |
| S24 | Settings: preferences/project/connection |
| S25 | Settings: WorkflowManager catalog |
| S26 | Settings: workflow editor, открытые advanced recipes |

Каждая строка и восемь вкладок summary/files/acceptance/comments/history/attachments/links/sessions проверены в4парах RU/EN×Light/Dark при1440/320CSSpx:272views. Ещё8modal views дают280matrix views. S01–S26 — функциональные состояния, а не вымышленные26URL. S15 включает существующий combined editor; S25/S26 принадлежат Settings. Content-waits S03 и S23 исключают ложный pass по одному skeleton/container.

`audit.mts` проверяет computed RGB contrast без округления, границы полей, duplicate IDs, page reflow; Chromium Accessibility Tree даёт независимые accessible names для интерактивных ролей. Дополнительный audit переводит native focus по доступным controls и проверяет видимую область/hit target с учётом clipping ancestors. Для SVG group проверяется painted circle, а не пустой центр bbox. Native focus, а не scrollIntoView, должен раскрывать действие. Неактивные элементы и закрытые details исключены; modal audit ограничен active dialog. Browser runner фиксирует SHA-25649frontend/build/harness files до запуска и сравнивает после cleanup.

## Текущие browser receipts

Общая команда, из корня репозитория, с установленными ранее зависимостями:

```powershell
node tests/web/accessibility/browser-acceptance.mts --synthetic-browser --playwright-core C:/Users/user/AppData/Local/npm-cache/_npx/eb7983f9b02fb67f/node_modules/playwright-core --chromium C:/Users/user/AppData/Local/ms-playwright/chromium-1223/chrome-win64/chrome.exe --screenshots C:/Users/user/.codex/visualizations/2026/11/12/01a1cedc-5a90-7a23-bb27-6f755c6885ce --scenario matrix
```

Для других сценариев последний аргумент — `core` или `states`. Browser plugin отсутствует; fallback на имеющийся Playwright1.63.0/Chromium1223. Каждый run имеет отдельные loopback service, workspace/profile/browser home; pairing/CSRF находятся только в памяти. Browser external origin requests блокируются. Provider0, credential operations0, real workspace mutations0. Подготовка управляемых синтетических agent/skill проходит существующий preview/apply, не installation. Autonomy сохраняется на паузе. Синтетический check явно не является выполненной командой.

| Scenario | Наблюдаемый результат | Receipt под `.tmp/paos-m4-0029/` |
| --- | --- | --- |
| matrix | exit0;1311checks/280views, все passed;45964text,8784field-boundary,19620focus samples | `browser-evidence-Z6WkiC/result.json`, `matrix-verified.log` |
| core | exit0;136checks/20views; modal Tab/Shift+Tab/background inert/Escape/restore, настоящий primary hover, mobile Escape | `browser-evidence-ZpVad3/result.json`, `core-verified.log` |
| states | exit0;289checks/60views; keyboard task Ready→in_progress и workflow draft save во всех4парах; loading/503/unavailable/recovery agents/workflow; empty tasks/sessions/agents/skills/documents/decisions/autonomy; System follows both media values; forced colors/reduced motion focus | `browser-evidence-DAdmsd/result.json`, `states-verified.log` |

Все3receipts: fixtureCleaned=true; sourceHashMismatches=[]; pageErrors=[], consoleErrors=[], externalRequests=[]. Samples повторяются между состояниями и не объявлены уникальными controls. В matrix272основныхviews нет findings по RGB/names/page overflow/focus exposure. Task tabs Home/End и Kanban ArrowRight проверены в8вариантах. Keyboard transition реально сохранён сервисом, workflow — как draft, без publish/run. Modal background control не может принять focus; после Escape opener восстановлен. System и forced colors не заменяют четыре explicit theme pairs.

Root визуально открыл текущие screenshot `paos-0029-en-dark-320-workflow.png` и `paos-0029-ru-light-1440-workflow.png`: labels читаемы, recipes и кнопки видны, narrow actions переносятся. Остальные screenshot сохранены runner в разрешённой visualization директории; они не все просмотрены вручную. Root не утверждает ручную26-screen проверку или screen-reader acceptance.

## RED, неуспешные попытки и исправления стенда

- `core-red.log` / `browser-evidence-LWydzz`: ошибочный setup keyPrefix/длина project name; не behavior RED.
- `core-baseline.log` / `browser-evidence-1XnZMw`: валидный baseline88checks/16views failed — modal focus/Escape/restore, unlabeled recipes, длинный header и границы полей light≈1.33/1.44, dark≈1.75/1.99. Первичный oracle также включал закрытые details; это исправлено, видимые contrast findings остаются действительными.
- `core-green-first.log` / `browser-evidence-x8ufkJ`: остались header intrinsic overflow и выход native Tab в browser chrome; исправлены. `core-green.log` / `browser-evidence-TlC93a` —88checks/16views passed на промежуточном состоянии, не final source proof.
- `matrix-first.log` / `browser-evidence-ECvtLi`:983checks/272views failed, отсутствовал keyboard region у доски/transcript; длинные данные растягивали session/team/artifact/decision layouts. Исправлены min-width/wrapping и focusability.
- `matrix-second.log` / `browser-evidence-y7kvhS`:991checks/272views, только8ArrowRight assertions failed. Native scroll анимируется: моментальное чтение scrollLeft было неверным oracle; теперь bounded wait20s после известного нулевого начала, не removal проверки.
- `matrix-focus.log` / `browser-evidence-cuoOH6`: исправленный S03 heading оказался неуникальным; scope first heading + реальная unique Task details button. Это locator setup failure.
- `matrix-focus2.log` / `browser-evidence-e9QYBl`:1311checks/280views,12focus failures. SVG group bbox центр не painted hit area — oracle исправлен на circle. На S01 mobile действительно перекрывал focused content.
- `mobile-red.log` / `browser-evidence-F0HD33`:136checks/20views failed — mobile Escape/restore. Добавлены Escape/ref/aria-controls и disclosure close при уходе фокуса. `matrix-final.log` / `browser-evidence-7h0jpL` оставил4S01failures: aside onBlur не покрывал переход через header/Menu. App focus capture закрывает disclosure при выходе из nav; audit ждёт React frame перед hit test. Финальные136/1311passed.
- `states-first.log` / `browser-evidence-KiwDhE`: новый empty project создан через API, но selector ещё не перечитан. Добавлен reload до проверки empty data. Это fixture setup, не product regression.
- `build-final.log`: TS2367 из narrow React event.target type в новом focus handler; явный Element type устраняет конфликт. `build-final-green.log` exit0.
- `web-full.log`: restricted sandbox не разрешил hardlink/symlink fixtures:473tests,458pass,10fail,5cancel. Сохранён исходный отказ. Тот же suite с разрешённым local escalation прошёл473/473; финальный `web-final.log` также473/473 skip0/12.990s.
- `doc-sync-apply-sandbox-denied.json`: sandbox отказал writer.lock внутри `.codex`. Exact preview digest повторён с local escalation; `doc-sync-apply.json` status=applied, recovery journal сохранён. Это не automatic approval rejection и не обход политики.
- `mkdocs-first.log`: strict build отказал на research links, отсутствующих в publishable docs tree, включая прежние registry ссылки.24существующих ссылок registryRU/EN превращены в явные repository-root code paths с сохранением labels/targets; новые Web docs ссылаются на evidence таким же образом. `navigation-link-repairs.json` хранит точный перечень. Финальный strict build exit0/18.12s, warning0. Лимиты/валидаторы не ослаблены.
- `docs-lifecycle.log`:251tests/13fail — новая RU/EN страница требует актуализации inventory161→162/151→152; `docs-lifecycle-green.log`:9fail — site-promoted count143→144. `docs-lifecycle-final.log`:4fail — hardcoded canonical site snapshot не содержит новую страницу. Счётчики обновляют фактический инвентарь, assertions не удалены.
- `mkdocs-canonical.log`: ошибочная попытка обновить canonical tracked `site/` завершилась OSError22 на search index; это не успешная сборка. Она затронула322tracked files и создала28generated copies. Canonical site восстановлен к clean HEAD: первый bounded restore вернул39files до sandbox OSError22, разрешённый повтор вернул283оставшихся и удалил28новых файлов, сверив их с isolated build. `generated-site-restoration.json` / `site-restoration.log`:site_source_diff=[], новый untracked site отсутствует. Пользовательские source файлы и Git history не менялись. Canonical snapshot не promoted и не объявлен свежим.
- Для проверки текущего build `tests/product_agent_os/test_product_agent_os_docs.py` поддерживает необязательный `PAOS_DOCS_SITE_DIR`, default остаётся `site`. Это выбор реального проверяемого артефакта, не пропуск checks. `docs-isolated-final.log`:1fail на10English-original pages с абсолютным `/en/`; выполнен существующий `tools/fix_site_i18n_links.ps1 -SiteDir .tmp/paos-m4-0029/site-final`, updated_files318. Итоговый251-test run проверяет весь свежий isolated tree после стандартного postprocess, включая новую RU/EN страницу, search/sitemap/file links; не использует stale canonical output.

Primary hover и локализованные option labels проверены final matrix/core; отдельный исторический RED по каждой строке перевода не заявлен. Все failed receipts сохранены, последующий pass не переименовывает setup rejection в product test.

## Review и Control-Plane Sync

Два bounded GPT-6 Astra/medium read-only workstreams: `/root/accessibility_mapping` — current-screen mapping и blockers; `/root/accessibility_review` — единственное independent assurance окно, context_mode=separate_reused_context. Review нашёл2P2: S03 не assert-ил реальный entry (`count()` без проверки), source hashes снимались только после run и пропускали часть файлов. Исправлены meaningful content waits и before/after всех49files; final receipts mismatch0. Дополнительные замечания по focus clipping, Shift+Tab/background/dialog coverage закрыты browser scenarios. Поздний mobile focus patch и document fallback проверены root self_review; повторного независимого окна не было. Tester verdict=closed_allowed для bounded local technical slice после final gates; human acceptance не выдаётся агентом.

Пять information classes обновлены через `sync_task_documents.py . preview/apply` без изменения plugin: REQUIREMENTS(scope), PLAN(sequence), TEST(commands), EVALS(thresholds/ceiling), RUNLOG(handoff). Exact reviewed digest `sha256:99bad7643621a86a89daf115fa763ebaa494f040d0381f5ed6a8d6a447f70859`; journal `.codex/product-agent-os/compaction/99bad7643621a86a89daf115fa763ebaa494f040d0381f5ed6a8d6a447f70859.json`. Исторические paragraphs/links сохранены. PLAN32531bytes/TEST36289bytes предупреждают32k, но остаются ниже40k; lossless compaction не требуется. `prod_test.md`:not_applicable (Batch39 не изменён); AGENTS/config/hooks/instructions:not_applicable; existing diagram atlas не меняется — нет нового product workflow/runtime boundary. Web README, RU/EN accessibility docs/nav/source registries обновлены.

В пределах того же sync исправлен TEST route для обнаруженного isolated docs target/postprocess, reviewed digest `sha256:3333068bdf99903163c5fb86be71e6b4ca224c7f0f3f300f06ef7a66001f313d`; `doc-sync-route-apply.json` и соответствующий recovery journal. TEST остаётся ниже40000bytes. Другие4секции не переписаны повторно.

Совместимость closure tooling: active workflow требует coordinated completion packet, но существующая research матрица не поддержана этой реализацией: case-sensitive writer ждёт lowercase Completion Report, research matrix превышает40000bytes, PLAN не имеет её source pin, writer не обновляет machine JSON. Повторный read-only research подтвердил это по `documentation_sync.py:_completion`, `task_plan_lifecycle.py:_replace_field`, `control_plane_documents.py:is_detailed_planning_matrix`. Миграция/разделение матрицы и изменение лимитов/плагина существенно расширили бы a11y task. В пределах текущей авторизации локальной реализации выбран точечный compatibility fallback: section-only штатный docs sync + exact task-card/JSON recovery before-images + независимые preservation/matrix/state/diff/source checks. Это не называется coordinated completion receipt и не полагается на legacy card-only как единственное доказательство синхронизации. Статус меняется только у0029;55other cards/JSON values,56tasks/12groups/estimates/order сохраняются. Existing PLAN pins других owner families не меняются. Неразрешённого source/doc handoff по0029нет; tooling limitation остаётся отдельно в этом evidence owner, plugin/runtime scope не расширен.

## Проверки, ограничения и следующий маршрут

Current `npm run check:web-m1` exit0; `npm run build:web` exit0, bundle518.44kB/gzip150.73kB и существующий >500kB warning. Это не performance/SLO measurement. `node --test tests/web/*.test.mts` —473pass/0fail/0skip. Strict MkDocs использует имеющуюся `.venv-docs`, isolated `.tmp/paos-m4-0029/site-final`, root site/ не объявлен свежим. Docs105 входят в combined251 gate. Exact final docs command:

```powershell
.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .tmp/paos-m4-0029/site-final
./tools/fix_site_i18n_links.ps1 -SiteDir .tmp/paos-m4-0029/site-final
$env:PAOS_DOCS_SITE_DIR='.tmp/paos-m4-0029/site-final'
python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_infrastructure_templates -v
```

`docs-verified.log` и final hooks/matrix/state/check_docs/diff hashes фиксируются в companion [results JSON](product-agent-os-web-m4-0029-results-2026-11-12.json); результаты не выводятся из hook advisory. Default canonical site tests требуют его актуальной сборки; в этом slice используется явно выбранный isolated output. Существующие historical snapshot claims не повышены до новой promotion.

| Финальный gate | Наблюдаемый результат | Log под `.tmp/paos-m4-0029/` |
| --- | --- | --- |
| Web regression |473tests/473pass/0skip,12.990s,exit0 | `web-final.log` |
| TypeScript / production build |exit0 / exit0;518.44kB bundle warning сохранён | `types-final.log`, `build-final-green.log` |
| Strict MkDocs / file-link postprocess |exit0/18.12s, warning0;318generated files normalized в isolated output | `mkdocs-final.log`, `mkdocs-file-links.log` |
| Docs + lifecycle + infrastructure |251tests/29.728s,OK,exit0 на isolated output | `docs-verified.log` |
| Final docs module |105tests/13.611s,OK,exit0 после TEST route update | `docs-final.log` |
| Docs structure / diff / matrix / state / hooks / compatibility |exit0, явные ok/compatible, без unresolved gap | `check-docs-final.log`, `diff-check.log`, `matrix-final-validation.log`, `state-final-validation.log`, `hooks-json.log`, `hooks-dir.log`, `compatibility.log` |
| Adapter pin |`67d6ced8b371be3dcf433637a3df7a8ed5ad3140c7a412e40178ad05abbe5869`,matches=true | `final-adapter.log` |

Final explicit self-review сверил все production hunks и новый Modal/auditor, current49-file hashes, absence of source diff у backend/contracts/plugin/AGENTS/config/hooks и canonical site, сохранение остальных55MD/JSONcard values и source-bound receipts. Три canonical JSON могут отображаться `M` из-за рабочего metadata/filter status, но raw bytes равны HEAD и `git diff -- site` пуст; новых untracked site files нет. Это не source change и не claim о fresh canonical build. Recovery journal и исходные неуспешные receipts оставлены для воспроизводимости. Новые screenshot и site-final — synthetic/local generated evidence.

Backend/plugin/runtime source и qualified manifest не менялись: runtime activation/provider/model selection/fallback proof not_applicable. Прежний PAOS-0028 full Python1450(skip1)/fixtures91/transcripts26/native/actual App receipts имеют прежний provenance и не объявлены заново выполненными; frozen source domains сверяются с baseline. В этой задаче native binary/provider/live App не запускались, credentials/install/Git/publication/release действий нет.

Limits: computed RGB audit не покрывает весь native paint, placeholder/pseudo/gradient cases и все assistive technologies; desktop text zoom200% отдельно не измерен (320CSSpx viewport — reflow sample, не заявление о полном zoom эквиваленте). Не заявлены manual screen-reader/full WCAG certification, model quality, token/cost/SLO, коммерческий выпуск или human acceptance. Нет axe dependency; роль/имя/contrast/focus проверяются описанным bounded oracle. Никакие реальные секреты/данные проекта не используются. Rollback — только текущие hunks/files с проверкой текущего hash и before-images, без destructive Git и удаления user changes.

Следующая PAOS-0030 «Упаковка и пилот»: dependencies0029 и0046implemented в матрице после closure. Пилот согласуется отдельно; перед коммерческим выпуском повторная актуализация AUTH-G1–G6 и применимых gaps обязательна. Это не заранее выданное разрешение на публикацию, provider, реальный проект или установку. Active duration не инструментирован; start/end wall time и null active metrics сохраняются в results/card.
