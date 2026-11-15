# Product-Agent OS — функциональные доработки после V3

Source status: repository_source / static_audit / owner_requested_planning; implementation_not_started.
Дата планирования: 15.11.2026. Timezone: Europe/Moscow. Schema version: task_matrix_plan_v1.

## Объём и статус

План содержит **29 новых задач PAOS-FUNC-01–PAOS-FUNC-29**, все `planned`, и ссылки на **3 ранее запланированные задачи M5**. Итого в этой обзорной матрице 32 позиции; это не общее число задач проекта. Существующие 56 карточек M1–M5, их 53 implemented / 3 planned и оценки сохранены. Новые дефекты не переписывают исторические receipts: они требуют текущего воспроизведения и новой проверки.

Машинное состояние новой группы: [functional-remediation-2026-11-15.json](functional-remediation-2026-11-15.json). Этот MD владеет техническим и продуктовым обоснованием, acceptance и completion evidence. Ссылки M5 не создают второй владеющий статус: их владелец — [research/product-agent-os-web-task-manager-task-group-2026-11-09.json](../research/product-agent-os-web-task-manager-task-group-2026-11-09.json) и [research/product-agent-os-web-task-manager-plan-2026-11-09.md](../research/product-agent-os-web-task-manager-plan-2026-11-09.md).

Запрос владельца разрешает составление и запись плана. Все исправления, расширения и проверки ниже остаются будущими задачами. P1 — блокировка исполнения или проверка целостности/recovery; P2 — функциональная ценность, корректность информации и поддерживаемость; P3 — ограниченный дефект отображения. Приоритет проверочной задачи не означает, что отказ уже наблюдался.

## Основания и границы доказательств

- Статический аудит исходников 15.11.2026 выявил семь кандидатов в дефекты F01–F07. F01 подтверждён сравнением fingerprint: текущий `apps/web/package-lock.json` SHA-256 `f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac`, квалифицированный `d279009aa1dca2bd2d6ba0e18a77d085a67e872d0dce78dd360fb23d43975f38`; отказ native broker выводится из проверки контракта и должен быть воспроизведён. Runtime в этом планировании не запускался.
- F08–F10/F18/F24 относятся к устройству реализации и полноте пользовательского пути. Производительность не признана плохой без измерений: F20 предшествует F09.
- F11–F17 — отсутствующие расширения либо намеренно ограниченные возможности текущего local scope. Это не семь доказанных регрессий redesign. Перед build нужны доступные capabilities и решения о данных, записи, privacy или канале поставки.
- F19–F23 — недостающее текущее доказательство. Исторические Web/browser receipts из [design/2026-11-13-v3/implementation-evidence.md](../design/2026-11-13-v3/implementation-evidence.md) не выдаются за заново выполненные проверки.
- Предыдущий audit MD не был создан из-за запрета записи; первичные ссылки и наблюдения перенесены в Source каждой карточки. Чат и этот план не заменяют код и актуальные runtime результаты.
- Внешние API и OpenAI capabilities этим планом не утверждаются. Если задача опирается на новый host/provider contract, при её discovery нужно проверить текущую официальную документацию и фактически доступный интерфейс.

## Рекомендуемая последовательность

1. Независимые стартовые ветки: F01 — квалификация runtime; F28 — контракт инвентаризации и политики. F03–F07 можно выполнять в своём ownership. F02 теперь использует нормализацию F28.
2. После F28 реализовать F26 (дерево/reader) и F27 (scan jobs), последовательно в shared HTTP/API файлах. F26 не зависит от готовности графа, F09 или F14; просмотр директории должен работать до завершения анализа. F29 подключает core discovery после F27/F28.
3. Интегрировать F10 с выбранными file references; F18 — с актуальностью дерева и scan status; F24 — с независимыми состояниями регистрации, inventory/documents/code/analysis. Перед native проверками заново квалифицировать изменённый runtime tuple.
4. F20: baseline можно снять раньше; для закрытия нужны F26/F27/F29 и расширенный workload. После измерений выполнить F09 (также зависит от F08). Затем F14 может расширять семантику графа поверх F27/F28. F14 не является предварительным условием файлового браузера.
5. F19 закрывается после нового пути Add → дерево → scan → discovery → file reference и связанных core fixes; F21/F22 проверяют исполнение и данные отдельно. F23 после F19/F21/F22/F24 включает пользовательское понимание файлов и покрытия. F25 синхронизирует текущие claims по мере изменений.
6. Остальные F11–F17 сохраняют индивидуальные design gates. M5 остаётся отдельной дорожкой: PAOS-0047 опционален; PAOS-0052 → PAOS-0053 не зависит от Sign in with ChatGPT. Этот план не разрешает provider, hosting, auth, публикацию или реализацию.

Hard dependencies записаны в Depends on/JSON; Blocks пересчитаны как обратные связи. Execution order — одна допустимая топологическая последовательность, а не разрешение параллельных записей. Transitive зависимости F23 от F26–F29 проходят через F19/F24; искусственный цикл «benchmark → optimization → benchmark» не добавляется: F20 даёт протокол и исходные измерения, F09 повторяет тот же workload после своих изменений.

Оценки предварительные. Для F11–F17 оценён discovery/design; для F26–F29 — грубый implementation range, который нужно уточнить после указанного contract/design gate. Общая дата завершения не выводится из этих интервалов. F23 включает 14 дней наблюдения отдельно от трудозатрат.

## Полная обзорная матрица новых задач

F01 в сокращённых зависимостях означает PAOS-FUNC-01. Все строки имеют статус `planned`.

| ID | Приоритет / тип | Задача | Техническое значение | Продуктовое значение | Критерии приёмки | Зависимости |
| --- | --- | --- | --- | --- | --- | --- |
| PAOS-FUNC-01 | P1 · Дефект | Восстановить квалификацию native runtime после redesign | Согласовать lockfile, manifest и native broker без ослабления проверки fingerprint. | Запуск задачи из обновлённого интерфейса действительно приводит к выполнению. | 1) На текущем lockfile воспроизведён отказ package_lock_mismatch; исправление не подменяет квалификацию простой перезаписью хеша.<br>2) На заново квалифицированном tuple новый broker исполняет synthetic command внутри разрешённого root и отклоняет запись снаружи.<br>3) Отрицательные сценарии для изменённых binary, lockfile и adapter остаются fail-closed; повторный старт проходит. | — |
| PAOS-FUNC-02 | P2 · Дефект | Восстановить связи структурированных артефактов с задачами | Унифицировать нормализацию files, artifactReferences, artifacts и fileContexts. | Документ находится из задачи, а задача — из документа и поиска. | 1) Задача со ссылкой только в artifacts.reference находится фильтром каталога по taskId и отображается в связанных задачах документа.<br>2) Legacy artifactReferences/files сохраняют поведение; дубли и разделители путей нормализуются.<br>3) Внешний URL не принимается за локальный путь; stale revision и недоступный файл отображаются явно.<br>4) File references используют нормализацию и root identity F28; каталог, дерево и задачи ссылаются на один разрешённый relativePath/revision. Deleted/moved/excluded не превращаются в доступный документ или право чтения. | F28 |
| PAOS-FUNC-03 | P2 · Дефект | Полностью сбрасывать черновик новой задачи | Синхронизировать модель, rawInputs, estimate, preview и dirty-state при Discard. | После отмены пользователь не видит данные, которые уже отсутствуют в сохраняемой задаче. | 1) В новой задаче заполнить criteria/risks/references/estimate, нажать Discard: все поля и модель возвращаются к одному пустому состоянию.<br>2) Следующее сохранение не возвращает отменённые данные; dirty/preview/error не вводят в заблуждение.<br>3) Для существующей задачи Discard возвращает серверную revision и не уничтожает чужие изменения. | — |
| PAOS-FUNC-04 | P2 · Дефект | Сохранять черновик назначений workflow при навигации | Включить typeMapping и исходную CAS revision в общий жизненный цикл draft. | Пользователь не теряет несохранённые назначения процессов при переходе между разделами. | 1) Изменить mapping типа задачи, уйти из Settings и вернуться: черновик восстановлен либо уход заранее остановлен понятным выбором.<br>2) Save/Discard корректно снимают dirty-state; default workflow и mapping не перетирают друг друга.<br>3) Смена проекта не переносит черновик в другой проект; stale save возвращает conflict без потери введённого. | — |
| PAOS-FUNC-05 | P2 · Дефект | Обозначить неполное покрытие portfolio рядом с итогами | Провести partial/loaded/expected из агрегатора в отображение KPI и progress. | Частично загруженные проекты не выглядят как полный итог портфеля. | 1) При успехе1 проекта и ошибке1 проекта рядом с totals показано «1 из2; данные неполные».<br>2) Неизвестные значения не заменяются нулём; progress явно относится к доступной выборке.<br>3) Loading, retry, all-failed и восстановление полного покрытия проверены в RU/EN. | — |
| PAOS-FUNC-06 | P3 · Дефект | Исправить нумерацию очереди на dashboard | Единый 1-based контракт позиции между scheduler и frontend. | Одинаковый порядок задач на dashboard и в управлении очередью. | 1) Для backend positions1/2 dashboard показывает №1/№2.<br>2) Для null номер отсутствует; reorder отражается одинаково на обеих поверхностях. | — |
| PAOS-FUNC-07 | P3 · Дефект | Сортировать последние задачи по времени | Задать явную сортировку по updatedAt с устойчивым tie-breaker и unknown policy. | Блок последних задач ведёт к действительно недавней работе. | 1) UUID-порядок специально противоположен времени: отображаются3 последних по updatedAt.<br>2) Равные и отсутствующие timestamps обрабатываются детерминированно; подпись поясняет выбранную семантику.<br>3) Создание и изменение задачи обновляют состав блока после refresh. | — |
| PAOS-FUNC-08 | P2 · Архитектура | Разделить общие контракты и зависимости UI/backend | Убрать импорты backend→frontend и contracts→backend, сохранив публичное поведение. | Изменение оформления реже ломает серверные функции и выпуск. | 1) Preferences и task decoder имеют одного независимого владельца; contracts не импортируют apps.<br>2) Существующие payload/schema и отказные сценарии сохранены; frontend и service проходят typecheck и текущие тесты.<br>3) Проверка направления импортов предотвращает регрессию; runtime tuple повторно квалифицирован, если затронуты pinned sources. | F01 |
| PAOS-FUNC-09 | P2 · Архитектура | Оптимизировать чтение и жизненный цикл снимков | По измерениям устранить лишние полные сканы и добавить ограниченное освобождение cache. | Длительная работа и большие проекты не упираются в задержки и накопленные snapshots. | 1) Выбраны и реализованы только bottlenecks, воспроизведённые F20; before/after на одном workload.<br>2) Девятый проект не требует restart лишь из-за8 graph snapshots: eviction/rebuild сохраняет revision/cursor safety.<br>3) Нагрузка на task/artifact/history чтение ограничена; превышение бюджета даёт объяснимый partial/error и безопасное восстановление.<br>4) После F20 сравнить metadata listing, graph status и scanner на том же workload: повторный запрос статуса не должен безусловно перечитывать все содержимое файлов; bytes/read и scan count измерены.<br>5) Cache key/eviction учитывают root identity, policy version и scan revision F27/F28; eviction не скрывает файлы из дерева F26 и не смешивает разные проекты. | F08, F20 |
| PAOS-FUNC-10 | P2 · Доработка | Показывать ограничения файлового scope до запуска | Общий preflight для числа файлов, размеров, excluded paths и границ actual diff. | Пользователь заранее понимает, почему задача не стартует и как её разделить. | 1) 32/33 файла,64KiB/64KiB+1 и суммарные512KiB проверяются до dispatch с конкретным объяснением.<br>2) Sensitive/link/binary exclusions не раскрывают содержимое; blocked execution не выдаётся за стартовавший run.<br>3) Если расширение лимитов необходимо, оно проходит отдельный bounded performance/security gate; лимиты не снимаются безусловно.<br>4) Выбор file reference из дерева F26 проходит execution preflight повторно: видимость/читаемость/индексация файла не означают разрешение на dispatch. Policy F28 и реальные execution limits отображаются раздельно; stale path/root требует обновления. | F01, F26, F28 |
| PAOS-FUNC-11 | P2 · Расширение | Ввести измеряемую статистику runs и расхода | Versioned telemetry с provenance, дедупликацией и агрегацией session→run→task→agent. | Длительность и расход помогают сравнивать результат работы без выдуманных чисел. | 1) Сначала утверждены доступные источники duration/tokens/tool calls/cost, privacy и retention; unsupported поля остаются unknown.<br>2) Повтор события не увеличивает totals; partial streams, restart и связь нескольких агентов не приводят к double count.<br>3) Dashboard, задача и агент показывают согласованные значения, период и source; стоимость появляется только при известной модели расчёта. | F05, F08 |
| PAOS-FUNC-12 | P2 · Расширение | Спроектировать и подключить внешний поиск skills | Отдельный read-only discovery adapter с provenance, лицензией, pin и preview. | Нужный skill можно найти вне локального каталога и осознанно добавить. | 1) До build выбран разрешённый источник, network/privacy policy и формат результата.<br>2) Поиск показывает origin/license/revision; timeout/offline не ломают локальный каталог.<br>3) Поиск ничего не устанавливает; добавление проходит существующий preview/apply и проверяет drift и зависимости. | — |
| PAOS-FUNC-13 | P2 · Расширение | Добавить безопасное применение document proposals | Preview-bound compare-and-swap writer с сохранением пользовательских правок и recovery. | Согласованное предложение можно довести до изменения документа внутри приложения. | 1) До build утверждены writer authority, source-vs-SQL ownership и eligible documents.<br>2) Apply меняет только проверенный файл при совпавшей revision; внешний edit вызывает conflict без overwrite.<br>3) Повтор apply идемпотентен; crash/rollback и sensitive paths проверены; staged/applied/accepted показываются отдельно. | F02, F08 |
| PAOS-FUNC-14 | P2 · Расширение | Расширить полезность и устойчивость карты проекта | Выбрать поддержку языков/связей; durable revision index, imports resolution и честный coverage. | Карта помогает оценить влияние изменения, а не создаёт видимость полного анализа. | 1) До build утверждена матрица поддерживаемых языков и типов связей; unsupported semantics остаются явно отмеченными.<br>2) Для выбранного scope cross-file imports/aliases проверяются на эталонных fixtures; unresolved не становится ложным ребром.<br>3) Restart/rebuild сохраняет либо явно инвалидирует revision; D3/Mermaid/list и impact показывают один набор данных.<br>4) Graph consumer использует inventory F28 и этап code в F27; discovered/readable/indexed/unsupported/excluded/error различаются. Нулевой или успешный JS/TS индекс не означает полного анализа проекта.<br>5) Ready/stale/unavailable графа не блокирует дерево F26; restart/cancel/retry не публикуют устаревший результат, недоступный parser оставляет другие результаты сканирования доступными. | F02, F09, F27, F28 |
| PAOS-FUNC-15 | P2 · Расширение | Уточнить и расширить границы автономности | Capability-based file/operation/cost policy без обещаний ограничения всего App host. | Пользователь понимает и контролирует допустимую самостоятельность агента. | 1) До build документированы enforceable границы и невозможные обещания; narrow-path execution без enforcement отклоняется.<br>2) В разрешённом маршруте выход за scope/лимит останавливает новые dispatch; unknown outcome остаётся fenced.<br>3) Денежный лимит допускается только при достаточном metering/reservation изF11; иначе UI явно сообщает недоступность. | F01, F10, F11 |
| PAOS-FUNC-16 | P2 · Расширение | Подтверждать доступную историю и реально загруженные профили | Развести configured/pinned/observed model, effort и asset version; capability-based history adapter. | Пользователь знает, какой агент фактически работал и какая часть истории доступна. | 1) До build проверен поддерживаемый host contract; недоступная история не извлекается обходом приватных хранилищ.<br>2) UI различает configured/pinned/observed; loadedVersion появляется только из подтверждённого события.<br>3) Reconnect/profile switch не смешивают историю и identity; partial coverage и отсутствие attestation объясняются. | F01 |
| PAOS-FUNC-17 | P2 · Расширение | Подготовить удобную установку, обновление и rollback | Поверх переносимого package задать version/digest/signing, compatibility и recovery UX. | Обновление не требует ручного подбора каталогов и не ставит данные под угрозу. | 1) До build выбраны канал доставки, формат installer, signing и AUTH/licensing gates; публикация отдельно.<br>2) Synthetic install/update/rollback сохраняют профиль; incompatible schema/tuple блокируют запуск с понятным восстановлением.<br>3) Не удаляются пользовательские профили и старые версии без отдельного решения; новый чистый Windows-профиль проходит согласованный сценарий. | F01, F22 |
| PAOS-FUNC-18 | P2 · Доработка | Согласовать обновление снимков задач и dashboard | Определить refresh/invalidation contract при фоне, мутациях и смене проекта. | После выполнения пользователь видит актуальный статус без угадывания, какой экран обновить. | 1) Изменение задачи/очереди в другом разрешённом канале либо обновляет экран, либо явно делает snapshot устаревшим.<br>2) Поздний ответ предыдущего проекта не заменяет текущие данные; dirty editor не перезаписывается refresh.<br>3) Polling/subscription останавливаются при unmount и не создают неограниченную нагрузку.<br>4) Create/modify/rename/delete и изменение policy/root инвалидируют затронутые directory/document/graph/analysis snapshots; выбран watcher либо bounded rescan/refresh с явной свежестью, без обещания невыбранного live watcher.<br>5) Scan events имеют scanId/revision; позднее событие отменённого задания или другого проекта не меняет UI. После возврата/restart отображается сохранённый scan status без перезаписи черновиков. | F05, F07, F26, F27 |
| PAOS-FUNC-19 | P1 · Проверка | Проверить сквозной функционал на текущей сборке | Связать real UI/API/storage/native receipts с одним revision без подмены execution mock-данными. | Пользователь проходит весь рабочий путь и получает проверяемый результат. | 1) Synthetic путь task→assignment→run→approval→command→diff/checks→owner acceptance проходит на текущем build.<br>2) Формы, custom workflow, RU/EN, обе темы, keyboard, links и partial/error состояния проверены послеF02–F07/F10/F18.<br>3) Actual App/model roundtrip и генерация agent/skill проверяются только при отдельном разрешении; без него фиксируется live gap, synthetic pass его не закрывает.<br>4) На synthetic fixture пройден путь Add → немедленно доступное дерево → этапы сканирования → preview допустимого файла → file reference задачи; карта и discovery не подменяют полноту файлового дерева.<br>5) Проверены empty/no-Control-plane/Python-only/mixed проекты, Unicode/пробелы, unreadable/oversized/binary/invalid-encoding, ignore/sensitive/link/traversal, rename/delete/root drift во время scan, cancel/restart/retry и два проекта. Ошибка отдельного файла сохраняет разрешённую часть, root violation блокируется; до/после target hashes совпадают.<br>6) RU/EN, две темы, keyboard/focus, pagination, явная неполнота поиска и отсутствие false-ready проверены; fixtures не используют реальные профили/credentials и не запускают target scripts. | F01, F02, F03, F04, F05, F06, F07, F10, F18, F24, F26, F27, F29 |
| PAOS-FUNC-20 | P2 · Проверка | Измерить масштабирование и длительную работу | Воспроизводимый workload с hardware/cache profile, latency/RSS/queue-depth и error budgets. | Большой проект и длительная сессия остаются управляемыми. | 1) Зафиксированы hardware/cache и объёмы:10k задач,100k сообщений,1k файлов; границы1001 файлов и9 проектов проверены отдельно.<br>2) Измерены cold startup, search/list/event-visible latency, RSS и снимки в повторяемом длительном прогоне; нет скрытой потери данных.<br>3) Результаты сравнены с WEB-NFR и согласованными порогами; deviations заведены вF09, неподдерживаемые объёмы явно ограничены.<br>4) До замеров фиксируются budgets и dataset: большой monorepo, широкая/глубокая директория, пустые папки, generated/vendor/ignored, binary/large, mixed languages. Измеряются registration-to-tree, раскрытие/поиск, scan phases, cancellation latency, restart recovery, RSS, количество обходов и прочитанных bytes.<br>5) Границы старых лимитов 1000/1001 файлов, 10000/10001 записей, depth32/33, 512KiB и 8MiB проверяются как корректный partial/bounded outcome, а не требование снять guards. Metadata listing не обязано читать содержимое всего проекта.<br>6) Baseline допускается до F26–F29; окончательное закрытие F20 требует их версии и сравнения с baseline. F09 использует этот протокол для before/after; benchmark не меняет user workspace. | F01, F26, F27, F29 |
| PAOS-FUNC-21 | P1 · Проверка | Перепроверить очередь, Stop и crash recovery | Проверить identity/CAS/lease/ownership fences и отсутствие replay в отказах. | Потеря соединения не запускает задачу дважды и не теряет результат. | 1) Crash до dispatch, после dispatch до receipt и после terminal receipt покрыты отдельными сценариями.<br>2) Stop без ACK не освобождает ownership; lost consumer/timeout требуют корректной сверки.<br>3) В разных roots разрешённая параллельность сохраняется, overlapping roots блокируются; selective Stop не отменяет чужой run. | F01 |
| PAOS-FUNC-22 | P1 · Проверка | Перепроверить импорт, backup и restore | Проверить source authority, freeze/CAS, counts/hashes/FK, blobs и идемпотентность. | Задачи, история и вложения сохраняются при переносе и восстановлении. | 1) Source drift и неизвестный writer останавливают cutover; две writable authority не появляются.<br>2) Corrupt/missing blob, прерванный import и повтор запроса дают безопасный результат без дублей.<br>3) Restore в новый synthetic profile сохраняет данные и ссылки; старый профиль неизменён; credentials/pending operations не воспроизводятся. | F01 |
| PAOS-FUNC-23 | P2 · Проверка | Провести продуктовую приёмку ключевых сценариев | Связать acceptance с наблюдаемой корректностью решений, а не числом кликов. | Пользователь без подсказки понимает статус, blocker, evidence и следующий шаг. | 1) До пилота согласованы участники, сценарии, opt-in/retention и baseline MD/chat; production data не обязательны.<br>2) Пройдены первое открытие, возвращение, конфликт, partial evidence и приёмка; ошибки понимания фиксируются вместе с успехами.<br>3) Цели4/5 за3мин и3/5 повторное использование за14дней изPRD проверяются как гипотезы; ноль ложных трактовок verified и потерь данных; owner принимает результат отдельно.<br>4) В пилот добавлены выбор папки, поиск обычного файла вне Control-plane, объяснение excluded/unsupported/partial, отмена/повтор и возвращение после restart. Наблюдатель проверяет, что участник не путает видимость файла, успешную индексацию и разрешение на исполнение. | F19, F21, F22, F24 |
| PAOS-FUNC-24 | P2 · Доработка | Объяснять доступность функций в момент действия | Единый capability vocabulary для staged/unsupported/partial/connected/qualified/accepted. | Пользователь отличает доступную функцию от экрана с будущей возможностью. | 1) Для usage, graph, proposals, skills discovery, history, autonomy и runtime рядом с действием показаны реальный scope и причина недоступности.<br>2) Есть конкретный следующий шаг; unsupported не выглядит как loading, connected не называется execution-qualified.<br>3) RU/EN и accessibility состояния проверены; нет повторного запроса уже действующей bounded authority.<br>4) В onboarding и проекте показаны независимые registration/tree/inventory/documents/code/analysis состояния F26–F29, время и scope наблюдения; counts.files не называется indexed без соответствующего покрытия.<br>5) Empty/no-supported-code не получает ложный «проект полностью проанализирован»; excluded/error/unsupported объясняют причину и действие. Недоступный parser/core adapter не скрывает доступное дерево, контрольный список Control-plane явно назван отдельным фильтром. | F05, F10, F26, F27, F29 |
| PAOS-FUNC-25 | P2 · Документация | Согласовать текущие продуктовые статусы и критерии | Один актуальный указатель PRD/architecture/plan/registry с сохранённой историей. | План и документация ясно показывают, что работает, ограничено и ждёт проверки. | 1) Текущие scope/status/acceptance не противоречат историческим implementation_not_started/API-only блокам: история явно помечена и маршрутизирована.<br>2) Для F01–F29 и M5 есть единый owner/status/source; implemented не подменяет human/live acceptance.<br>3) Синхронизированы только изменённые claims и RU/EN registry; validators/docs tests проходят, старые56cards сохранены.<br>4) Текущая проверка docs-site больше не сообщает missing web/accessibility.html и web/pilot.html в RU/EN; search/sitemap/switcher parity подтверждён на явно выбранном build. Публикация и promotion сайта отдельно.<br>5) Документы различают «Источники», файловое дерево F26, сканирование F27, inventory policy F28 и discovery F29; версии API/coverage, recovery и ограничения описаны в existing PRD/architecture, без заявления об автоматическом ремонте или полной семантике. | — |
| PAOS-FUNC-26 | P2 · Расширение | Добавить файловый браузер проекта | Независимый от графа API директорий и безопасного чтения с ленивой загрузкой, стабильными ссылками и ограниченными ответами. | Пользователь видит структуру выбранной папки и открывает доступные файлы, даже когда индекс не готов или язык не поддерживается. | 1) После регистрации раздел «Файлы» доступен без графа и завершённого сканирования; видны вложенные и пустые каталоги, исходники, конфигурации и бинарные файлы как метаданные, в пределах разрешённой политики F28.<br>2) Раскрытие каталога загружает только нужную ветку; pagination и фильтры показывают границы выборки; поиск по имени/пути явно сообщает scope. Метаданные содержат relativePath, тип, размер, modifiedAt и состояние доступа.<br>3) Текст читается по отдельному запросу с проверкой root identity, revision, размера и кодировки; binary/oversized/unreadable получают объяснение. Неподдерживаемое индексатором расширение не скрывает файл. HTML/скрипты не исполняются при просмотре.<br>4) Нет чтения за пределами корня через traversal, symlink/junction/hardlink и подмену каталога; sensitive content не раскрывается. Выбор файла не передаёт весь проект модели и не выдаёт разрешение на выполнение.<br>5) Выбранный путь можно скопировать и использовать как file reference; Control-plane — фильтр над реальными путями. Смена проекта и поздний ответ не смешивают дерево; RU/EN, keyboard, focus, empty/error/loading проверены. | F28 |
| PAOS-FUNC-27 | P2 · Расширение | Сделать сканирование управляемым фоновым заданием | Сохраняемые scan ID и этапы, bounded worker, идемпотентность, отмена, повтор и восстановление отдельно от регистрации проекта. | Проект доступен сразу после регистрации; пользователь видит ход сканирования, частичный результат и способ продолжить после сбоя. | 1) Регистрация сохраняется один раз и возвращает доступный проект без ожидания полного обхода; scan status содержит scanId, root identity, policy version, этап inventory/documents/code/analysis, начало/обновление, счётчики и причины partial/error.<br>2) Повтор Add/retry в том числе после restart не создаёт новый проект или дублирующую работу; конкурентные запросы одной revision объединяются либо получают объяснимый conflict. Изменившийся root не продолжает старое задание.<br>3) Cancel останавливает дальнейшую работу и позднюю публикацию; повтор запускается с явно определённой revision. Restart восстанавливает либо переводит задание в recovery_required/interrupted; незавершённое не становится completed.<br>4) Заданы budgets времени/памяти/записей и concurrency; failure одного анализатора сохраняет допустимые результаты других этапов. Ready одного индекса не означает полный анализ проекта; неподключённый analysis adapter отображается как unavailable.<br>5) Состояние и последнее успешное покрытие доступны после открытия Settings/проекта и restart; events или bounded polling не перезаписывают более новую revision. Scan bookkeeping остаётся в профиле PAOS, target workspace не изменяется. | F28 |
| PAOS-FUNC-28 | P2 · Архитектура | Унифицировать инвентаризацию, покрытие и исключения | Общий контракт путей, revision и coverage для directory/document/code consumers при раздельных правах listing, reading и indexing. | Файлы не исчезают из обзора из-за отсутствия языкового анализатора; пользователь понимает, что найдено, пропущено или недоступно. | 1) Контракт различает discovered, readable, indexed, unsupported, excluded и error; счётчики определяют разные стадии и не суммируют пересекающиеся множества как общее число файлов. Empty и unknown отличаются; отсутствие подходящего кода не означает полный анализ.<br>2) Файловое дерево независимо от набора расширений индексатора. .gitignore и project include/exclude имеют явную precedence и разные правила видимости/индексации; ignore не выдаёт права доступа. Sensitive paths/content защищены даже при include override.<br>3) Отчёт показывает применённую policy version, причины пропуска, лимиты и partial coverage. Тяжёлые generated/vendor каталоги не читаются без необходимости; разрешённое раскрытие метаданных не снимает ограничений чтения содержимого.<br>4) Ошибка, превышение размера или unsupported encoding отдельного файла сохраняет другие разрешённые записи; directory-level denial помечает неполноту. При root identity drift, попытке выхода за корень или недостоверной revision публикация небезопасного результата блокируется.<br>5) Bounded/paged inventory поддерживает normalised relative paths, Unicode/пробелы и Windows case semantics; ссылки и race conditions не расширяют root. Одинаковые policy/root/revision дают согласованные ссылки и причины во всех consumers.<br>6) Изменение политики инвалидирует затронутые snapshots; file metadata не требует полного чтения всех исходников. Позитивные/отрицательные сценарии и нагрузочные границы проверены; исходники проекта не меняются. | — |
| PAOS-FUNC-29 | P2 · Расширение | Подключить core discovery к добавлению проекта | Версионированный read-only adapter к существующему discovery/first-run analysis с provenance, ограничениями и invalidation. | После добавления проекта видны стек, структура, Control-plane gaps и обоснованные следующие шаги, а не только количество узлов графа. | 1) До build выбран способ reuse существующих core discovery/first-run модулей и deployment/runtime contract. Недоступный Python/adapter/version даёт явный unavailable; установка зависимостей и альтернативный полный scanner автоматически не запускаются.<br>2) Analysis запускается как отдельный этап F27, использует согласованную inventory policy F28 и возвращает schema version, source revision, stack/components, control-plane coverage, findings с источниками/confidence/limitations.<br>3) Обнаруженные scripts/configs только анализируются как данные: не исполняются команды проекта, tests, hooks, модели или провайдеры; target files не создаются и не исправляются. Предложения Control-plane остаются предложениями.<br>4) Пустой проект, проект без Control-plane, Python-only, mixed stack и unsupported language получают объяснимые результаты без выдуманной полноты; timeout/error сохраняют доступное дерево и уже полученное покрытие.<br>5) Изменения файлов, root или inventory policy делают прежние выводы stale; повтор и restart не смешивают revisions. Выводы доступны из выбранного проекта в RU/EN, связаны с разрешёнными file references и не раскрывают secrets. | F27, F28 |

## Существующие M5: ссылки без дублирования состояния

Состояние на момент чтения владельца: `planned`. Текущий статус всегда читать в исходной группе M1–M5.

| ID | Задача | Техническое значение | Продуктовое значение | Критерии приёмки исходной карточки | Зависимости |
| --- | --- | --- | --- | --- | --- |
| PAOS-0047 | Опциональный Sign in with ChatGPT | После допуска реализовать отдельный SIWC route, consent, PKCE/scopes, refresh/restart/resume и preview capability matrix | Eligible пользователь может использовать разрешённый ChatGPT plan без второго рабочего приложения. | Только после подтверждённого admission exact paid/local route: identity и plan scope проверены, refresh/resume не дублирует работу, unsupported tools скрыты с причиной; API route не зависит от этой задачи. | PAOS-0039, PAOS-0044, PAOS-0046 |
| PAOS-0052 | Командный профиль PostgreSQL и pgvector | После отдельного M5 team design/start решения реализовать server repository, dialect migrations, tenancy/RLS, lexical и versioned vector index; hosting/auth/runtime design gate до кода | Команда работает с общим актуальным состоянием и поиском в пределах своих прав. | ST-10: domain parity, negative tenant/pool tests, filtered search; embedding model/privacy approved; lexical fallback; hosting/auth/runtime placement согласованы; local M4 не зависит от M5 | PAOS-0048, PAOS-0049, PAOS-0051, PAOS-0030 |
| PAOS-0053 | Перенос local проекта в team workspace | Versioned logical export/import, actor/tenant mapping, blob checks, final delta и one-authority handover | Пользователь переносит проект команде с прежними задачами и историей без конфликтующих writable копий. | ST-11/ST-AC-08: UUID/key collisions, identity mapping, counts/hashes/FK, final delta, rollback; credentials/pending approvals/commands исключены; local read-only после switch; без bidirectional sync | PAOS-0056, PAOS-0052 |

## Общий контракт исполнения и приёмки

- Ошибка сначала воспроизводится на текущем revision; RED из broken setup не принимается. Ограничение признаётся дефектом только относительно принятого контракта.
- Проверки должны указывать исходники/dependencies, среду, synthetic dataset, наблюдаемый результат и границы доказательства. Mock UI, подключённый App и full execution — разные состояния.
- Никаких tokens, secrets, raw private chat или настоящих customer данных в отчётах. Pairing material остаётся в памяти; provider calls и реальные профили за пределами synthetic проверки требуют точного разрешения.
- Design-approved, implemented, technically verified и human accepted — разные факты. Задачи расширения F11–F17 нельзя завершить только дизайном; для implemented нужны все поведенческие AC и checks.
- Технические и продуктовые поля обязательны для каждой новой карточки; completion получает фактическую дату только после выполнения. Все будущие commands ниже — план, а не журнал выполненных проверок.
- Rollback каждой задачи сохраняет пользовательские файлы и чужую работу. Планирование не создаёт branch/commit/PR и не меняет приложение, hook/trust или permissions.

## Готовность к запуску задач

Статус пакета: `proposal_staged`; это полный backlog, а не утверждение `plan_ready` для всей реализации. Проверка структуры плана не закрывает следующие gates.

| Gate / задачи | Статус | Владелец и требуемое доказательство | Риск до закрытия |
| --- | --- | --- | --- |
| Воспроизведение F01–F07 | present_unverified | tester: RED и конкретный исходный revision; AC и Source в карточках | статическое предположение может отличаться от runtime |
| Архитектура F08/F09 | proposal_staged | architect: boundary/contract review в существующей architecture и измерения F20; existing-capability scan до нового кода | излишний рефакторинг, изменение публичного поведения |
| Telemetry F11 | applicable_missing | architect/product-manager: tracking sources, ownership, privacy/retention, unknown policy | выдуманные метрики и double count |
| Расширения F12–F17 | approval_required | владелец + architect: индивидуальный design gate из карточки, поддерживаемые capabilities, оценка build | недоступный API, нарушение write/enforcement/distribution границ |
| Сценарии F19–F22 | proposal_staged | tester: protocol → checks → receipts в Completion Report; ожидается exit0 и прохождение всех scoped AC без подмены native исполнения | synthetic и live доказательства могут быть ошибочно смешаны |
| Human pilot F23 | applicable_missing | product-manager + владелец: согласованный protocol, участники/consent, baseline, наблюдаемые результаты за 14 дней | продуктовая ценность пока гипотеза |
| Docs tooling текущей планировки | not_applicable | existing Python docs checks и Markdown достаточны; сайт, CI и новые зависимости не меняются | rendered-site freshness не заявляется |
| Coding standard текущей планировки | not_applicable | код не меняется; при старте implementation использовать действующий coding-standards workflow | план не заменяет source review конкретного slice |
| M5 | approval_required | исходные карточки владеют admission/team design и migration gates | нельзя начать team/provider работу из ссылки в этой матрице |

Business/product hypothesis: корректное сохранение состояния и понятный scope должны уменьшить ошибки работы; подтверждение F23, а не факт из числа тестов. Outcome scope — local App-active продукт; наблюдение repeat use — 14 дней; delivery metrics и пользовательская ценность разделены. Для расширений с новыми domain/API/storage boundaries необходимы актуализация existing architecture/ADR и согласование invariants до build; принудительная новая методология, портал или набор шаблонов сейчас не создаются.

## Дополнение: файлы и сканирование — 15.11.2026

Владелец разрешил только обновление плана. Добавлены F26–F29; уточнены AC десяти существующих задач F02/F09/F10/F14/F18/F19/F20/F23/F24/F25 и hard dependencies семи из них. Все 29 задач группы остаются planned; три M5 — ссылки на прежний источник состояния.

Выбранная граница: регистрация проекта → доступное файловое дерево и read-on-demand → управляемое сканирование → отдельные inventory/documents/code/analysis результаты. «Файл видим», «файл разрешено читать», «файл проиндексирован» и «можно выполнить команду» — разные факты. Unsupported язык не скрывает директорию. Контекст модели формируется отдельно, без автоматической отправки всего проекта.

Source-backed основание: [Sources](../apps/local-service/src/adapters/project-sources.ts) перечисляет шесть Control-plane файлов; [регистрация](../apps/local-service/src/http/application.mts) сохраняет проект, затем ждёт source/code scan; [inventory](../apps/local-service/src/code-index/sources.mts) использует фиксированные исключения и лимиты; [core discovery](../plugins/product-agent-os/scripts/product_agent_os/discovery.py) и [first-run](../plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) существуют отдельно от проверенного Web onboarding. Это статический вывод, не новый runtime receipt.

| Design gate | Статус / владелец | Что требуется перед build |
| --- | --- | --- |
| F28 inventory policy | proposal_staged; architect + security reviewer | Общие root/path/revision/coverage semantics; listing/read/index separation; precedence ignores; budgets; fail-closed boundary |
| F26 directory API/UI | proposal_staged; builder + product-manager | Read-only дерево и preview, pagination, empty/error/keyboard/RU/EN; файл не зависит от языка индексатора |
| F27 scan lifecycle | proposal_staged; architect + tester | Durable state machine, recovery/idempotency/cancel, profile storage и migration/rollback contract; bounded workload |
| F29 core adapter | proposal_staged; architect + plugin-runtime-builder | Reuse вместо независимого scanner; versioned structured result, runtime availability, read-only invocation и stale policy |
| F19/F20/F23 coverage | proposal_staged; tester/product-manager | Расширенные fixtures, измеряемые budgets до benchmark и отдельная human acceptance |

Shared ownership: F28 владеет inventory contract; F26 — directory API/reader; F27 — orchestration/profile state; F29 — core adapter/result. Изменения общих application.mts, client.ts, storage и onboarding сериализовать. F18/F24 интегрируют завершённые contracts, F19/F20 проверяют их вместе. Новые имена work locations — план, файлы реализации сейчас не создаются.

Обязательная проверочная матрица: empty/no-Control-plane, Python-only/mixed stack, большой monorepo, Unicode/пробелы, wide/deep directories, ignored/generated/vendor, binary/large/invalid-encoding/unreadable, symlink/junction/hardlink/traversal, root replacement, file rename/delete во время scan, два проекта, cancel/restart/retry. Для F20 сначала фиксируются budgets и hardware/cache; лимит не снимается ради прохождения теста. Существующие guarded source helpers переиспользуются после проверки контракта.

## Подробные карточки

### Task `PAOS-FUNC-01`

- Task: PAOS-FUNC-01 — Восстановить квалификацию native runtime после redesign
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: `PAOS-FUNC-08`, `PAOS-FUNC-10`, `PAOS-FUNC-15`, `PAOS-FUNC-16`, `PAOS-FUNC-17`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-21`, `PAOS-FUNC-22`
- Source: Lock SHA-256 d279009a… в manifest и f126e4dc… текущего файла не совпали; adapter99 совпал в аудите15.11. [packages/contracts/runtime/manifest.mts](../packages/contracts/runtime/manifest.mts), [apps/local-service/src/runtime/sandbox-broker.mts](../apps/local-service/src/runtime/sandbox-broker.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Восстановить квалификацию native runtime после redesign.
- Technical value: Согласовать lockfile, manifest и native broker без ослабления проверки fingerprint.
- Product value: Запуск задачи из обновлённого интерфейса действительно приводит к выполнению.
- Scope: `packages/contracts/runtime/manifest.mts`; `packages/contracts/runtime/qualified-manifest.json`; `apps/local-service/src/runtime/sandbox-broker.mts`; `tests/web/runtime-manifest.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Запуск задачи из обновлённого интерфейса действительно приводит к выполнению. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: На текущем lockfile воспроизведён отказ package_lock_mismatch; исправление не подменяет квалификацию простой перезаписью хеша. AC2: На заново квалифицированном tuple новый broker исполняет synthetic command внутри разрешённого root и отклоняет запись снаружи. AC3: Отрицательные сценарии для изменённых binary, lockfile и adapter остаются fail-closed; повторный старт проходит.
- Verification gates: `node --test tests/web/runtime-manifest.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: native_synthetic_acceptance_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: plugin-runtime-builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: native_synthetic_acceptance_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-02`

- Task: PAOS-FUNC-02 — Восстановить связи структурированных артефактов с задачами
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-13`, `PAOS-FUNC-14`, `PAOS-FUNC-19`
- Source: taskPaths читает files/artifactReferences; Editor отдельно сохраняет artifacts. [apps/local-service/src/artifacts/service.mts](../apps/local-service/src/artifacts/service.mts), [apps/web/src/features/tasks/Editor.tsx](../apps/web/src/features/tasks/Editor.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Восстановить связи структурированных артефактов с задачами.
- Technical value: Унифицировать нормализацию files, artifactReferences, artifacts и fileContexts.
- Product value: Документ находится из задачи, а задача — из документа и поиска.
- Scope: `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/impact/service.mts`; `tests/web/skill-generation-artifacts.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Документ находится из задачи, а задача — из документа и поиска. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Задача со ссылкой только в artifacts.reference находится фильтром каталога по taskId и отображается в связанных задачах документа. AC2: Legacy artifactReferences/files сохраняют поведение; дубли и разделители путей нормализуются. AC3: Внешний URL не принимается за локальный путь; stale revision и недоступный файл отображаются явно. AC4: File references используют нормализацию и root identity F28; каталог, дерево и задачи ссылаются на один разрешённый relativePath/revision. Deleted/moved/excluded не превращаются в доступный документ или право чтения.
- Verification gates: `node --test tests/web/skill-generation-artifacts.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 4–8 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: reproduce_then_fix; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-03`

- Task: PAOS-FUNC-03 — Полностью сбрасывать черновик новой задачи
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: `PAOS-FUNC-19`
- Source: Reset не сбрасывает rawInputs; эффект очистки требует entity. [apps/web/src/features/tasks/Editor.tsx](../apps/web/src/features/tasks/Editor.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Полностью сбрасывать черновик новой задачи.
- Technical value: Синхронизировать модель, rawInputs, estimate, preview и dirty-state при Discard.
- Product value: После отмены пользователь не видит данные, которые уже отсутствуют в сохраняемой задаче.
- Scope: `apps/web/src/features/tasks/Editor.tsx`; `tests/web/single-window/m2-task-manager-browser-acceptance.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: После отмены пользователь не видит данные, которые уже отсутствуют в сохраняемой задаче. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: В новой задаче заполнить criteria/risks/references/estimate, нажать Discard: все поля и модель возвращаются к одному пустому состоянию. AC2: Следующее сохранение не возвращает отменённые данные; dirty/preview/error не вводят в заблуждение. AC3: Для существующей задачи Discard возвращает серверную revision и не уничтожает чужие изменения.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: browser_reproduction_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 3–6 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: browser_reproduction_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-04`

- Task: PAOS-FUNC-04 — Сохранять черновик назначений workflow при навигации
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: `PAOS-FUNC-19`
- Source: Draft cache не включает typeMapping/mappingDirty. [apps/web/src/features/workflows/WorkflowManager.tsx](../apps/web/src/features/workflows/WorkflowManager.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Сохранять черновик назначений workflow при навигации.
- Technical value: Включить typeMapping и исходную CAS revision в общий жизненный цикл draft.
- Product value: Пользователь не теряет несохранённые назначения процессов при переходе между разделами.
- Scope: `apps/web/src/features/workflows/WorkflowManager.tsx`; `tests/web/single-window/m2b-browser-acceptance.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь не теряет несохранённые назначения процессов при переходе между разделами. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Изменить mapping типа задачи, уйти из Settings и вернуться: черновик восстановлен либо уход заранее остановлен понятным выбором. AC2: Save/Discard корректно снимают dirty-state; default workflow и mapping не перетирают друг друга. AC3: Смена проекта не переносит черновик в другой проект; stale save возвращает conflict без потери введённого.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: browser_reproduction_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 4–8 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: browser_reproduction_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-05`

- Task: PAOS-FUNC-05 — Обозначить неполное покрытие portfolio рядом с итогами
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: `PAOS-FUNC-11`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: aggregateSnapshots возвращает partial; dashboard totals его не показывает. [apps/web/src/features/dashboard/model.ts](../apps/web/src/features/dashboard/model.ts), [apps/web/src/features/dashboard/Dashboard.tsx](../apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Обозначить неполное покрытие portfolio рядом с итогами.
- Technical value: Провести partial/loaded/expected из агрегатора в отображение KPI и progress.
- Product value: Частично загруженные проекты не выглядят как полный итог портфеля.
- Scope: `apps/web/src/features/dashboard/model.ts`; `apps/web/src/features/dashboard/Dashboard.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Частично загруженные проекты не выглядят как полный итог портфеля. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: При успехе1 проекта и ошибке1 проекта рядом с totals показано «1 из2; данные неполные». AC2: Неизвестные значения не заменяются нулём; progress явно относится к доступной выборке. AC3: Loading, retry, all-failed и восстановление полного покрытия проверены в RU/EN.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 3–6 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: reproduce_then_fix; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-06`

- Task: PAOS-FUNC-06 — Исправить нумерацию очереди на dashboard
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P3
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: `PAOS-FUNC-19`
- Source: Backend indexOf+1, dashboard position+1. [apps/local-service/src/scheduler/service.mts](../apps/local-service/src/scheduler/service.mts), [apps/web/src/features/dashboard/Dashboard.tsx](../apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Исправить нумерацию очереди на dashboard.
- Technical value: Единый 1-based контракт позиции между scheduler и frontend.
- Product value: Одинаковый порядок задач на dashboard и в управлении очередью.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Одинаковый порядок задач на dashboard и в управлении очередью. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Для backend positions1/2 dashboard показывает №1/№2. AC2: Для null номер отсутствует; reorder отражается одинаково на обеих поверхностях.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 1–3 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: reproduce_then_fix; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-07`

- Task: PAOS-FUNC-07 — Сортировать последние задачи по времени
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P3
- Evidence level: static_finding_reproduction_required
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: `PAOS-FUNC-18`, `PAOS-FUNC-19`
- Source: Dashboard slice(-3), storage ORDER BY id. [apps/web/src/features/dashboard/Dashboard.tsx](../apps/web/src/features/dashboard/Dashboard.tsx), [apps/local-service/src/storage/sqlite-worker.mts](../apps/local-service/src/storage/sqlite-worker.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Сортировать последние задачи по времени.
- Technical value: Задать явную сортировку по updatedAt с устойчивым tie-breaker и unknown policy.
- Product value: Блок последних задач ведёт к действительно недавней работе.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `tests/web/ui-v3-dashboard.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Блок последних задач ведёт к действительно недавней работе. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: UUID-порядок специально противоположен времени: отображаются3 последних по updatedAt. AC2: Равные и отсутствующие timestamps обрабатываются детерминированно; подпись поясняет выбранную семантику. AC3: Создание и изменение задачи обновляют состав блока после refresh.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 2–4 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: reproduce_then_fix; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-08`

- Task: PAOS-FUNC-08 — Разделить общие контракты и зависимости UI/backend
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Архитектура; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-09`, `PAOS-FUNC-11`, `PAOS-FUNC-13`
- Source: HTTP imports web/preferences; contracts imports local-service/task-profile. [apps/local-service/src/http/application.mts](../apps/local-service/src/http/application.mts), [packages/contracts/issues/task-profile.ts](../packages/contracts/issues/task-profile.ts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Разделить общие контракты и зависимости UI/backend.
- Technical value: Убрать импорты backend→frontend и contracts→backend, сохранив публичное поведение.
- Product value: Изменение оформления реже ломает серверные функции и выпуск.
- Scope: `apps/local-service/src/http/application.mts`; `apps/web/src/design/preferences.ts`; `packages/contracts/issues/task-profile.ts`; `apps/local-service/src/tasks/task-profile.ts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Изменение оформления реже ломает серверные функции и выпуск. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Preferences и task decoder имеют одного независимого владельца; contracts не импортируют apps. AC2: Существующие payload/schema и отказные сценарии сохранены; frontend и service проходят typecheck и текущие тесты. AC3: Проверка направления импортов предотвращает регрессию; runtime tuple повторно квалифицирован, если затронуты pinned sources.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Сохранение текущих контрактов, регрессии и сравнение before/after. Общие docs gates применяются при изменении документации.
- Risks / approval gates: architecture_review_before_refactor; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: architecture_review_before_refactor; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-09`

- Task: PAOS-FUNC-09 — Оптимизировать чтение и жизненный цикл снимков
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Архитектура; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-08`, `PAOS-FUNC-20`
- Blocks: `PAOS-FUNC-14`
- Source: Полные projectEntities; graph memory cap8; catalog snapshot limits. [apps/local-service/src/code-index/service.mts](../apps/local-service/src/code-index/service.mts), [apps/local-service/src/artifacts/service.mts](../apps/local-service/src/artifacts/service.mts), [apps/local-service/src/task-manager/service.mts](../apps/local-service/src/task-manager/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Оптимизировать чтение и жизненный цикл снимков.
- Technical value: По измерениям устранить лишние полные сканы и добавить ограниченное освобождение cache.
- Product value: Длительная работа и большие проекты не упираются в задержки и накопленные snapshots.
- Scope: `apps/local-service/src/task-manager/service.mts`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/sessions/service.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Длительная работа и большие проекты не упираются в задержки и накопленные snapshots. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Выбраны и реализованы только bottlenecks, воспроизведённые F20; before/after на одном workload. AC2: Девятый проект не требует restart лишь из-за8 graph snapshots: eviction/rebuild сохраняет revision/cursor safety. AC3: Нагрузка на task/artifact/history чтение ограничена; превышение бюджета даёт объяснимый partial/error и безопасное восстановление. AC4: После F20 сравнить metadata listing, graph status и scanner на том же workload: повторный запрос статуса не должен безусловно перечитывать все содержимое файлов; bytes/read и scan count измерены. AC5: Cache key/eviction учитывают root identity, policy version и scan revision F27/F28; eviction не скрывает файлы из дерева F26 и не смешивает разные проекты.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Сохранение текущих контрактов, регрессии и сравнение before/after. Общие docs gates применяются при изменении документации.
- Risks / approval gates: measured_bottleneck_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 12–24 ч после benchmark; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: measured_bottleneck_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-10`

- Task: PAOS-FUNC-10 — Показывать ограничения файлового scope до запуска
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Доработка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-26`, `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-15`, `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: Capture ограничен32 файлами,64KiB/файл,512KiB суммарно. [apps/local-service/src/runtime/app-agent-files.mts](../apps/local-service/src/runtime/app-agent-files.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Показывать ограничения файлового scope до запуска.
- Technical value: Общий preflight для числа файлов, размеров, excluded paths и границ actual diff.
- Product value: Пользователь заранее понимает, почему задача не стартует и как её разделить.
- Scope: `apps/local-service/src/runtime/app-agent-files.mts`; `apps/local-service/src/runtime/app-agent-gateway.mts`; `apps/web/src/ui/SessionContext.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл). Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь заранее понимает, почему задача не стартует и как её разделить. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: 32/33 файла,64KiB/64KiB+1 и суммарные512KiB проверяются до dispatch с конкретным объяснением. AC2: Sensitive/link/binary exclusions не раскрывают содержимое; blocked execution не выдаётся за стартовавший run. AC3: Если расширение лимитов необходимо, оно проходит отдельный bounded performance/security gate; лимиты не снимаются безусловно. AC4: Выбор file reference из дерева F26 проходит execution preflight повторно: видимость/читаемость/индексация файла не означают разрешение на dispatch. Policy F28 и реальные execution limits отображаются раздельно; stale path/root требует обновления.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: shared_preflight_contract_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: shared_preflight_contract_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-11`

- Task: PAOS-FUNC-11 — Ввести измеряемую статистику runs и расхода
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-08`
- Blocks: `PAOS-FUNC-15`
- Source: Metrics durationSeconds/tokenCount/cost=null; tool_use не измеряется. [apps/local-service/src/team/service.mts](../apps/local-service/src/team/service.mts), [apps/web/src/features/dashboard/Dashboard.tsx](../apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Ввести измеряемую статистику runs и расхода.
- Technical value: Versioned telemetry с provenance, дедупликацией и агрегацией session→run→task→agent.
- Product value: Длительность и расход помогают сравнивать результат работы без выдуманных чисел.
- Scope: `apps/local-service/src/team/service.mts`; `apps/local-service/src/events/task-time.ts`; `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/team/TeamManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Длительность и расход помогают сравнивать результат работы без выдуманных чисел. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Сначала утверждены доступные источники duration/tokens/tool calls/cost, privacy и retention; unsupported поля остаются unknown. AC2: Повтор события не увеличивает totals; partial streams, restart и связь нескольких агентов не приводят к double count. AC3: Dashboard, задача и агент показывают согласованные значения, период и source; стоимость появляется только при известной модели расчёта.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/task-time.test.mts tests/web/ui-v3-dashboard.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: telemetry_source_privacy_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч discovery/design; build после выбора источников; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: telemetry_source_privacy_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-12`

- Task: PAOS-FUNC-12 — Спроектировать и подключить внешний поиск skills
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: нет
- Source: remote_discovery_adapter_not_configured. [apps/local-service/src/team/service.mts](../apps/local-service/src/team/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Спроектировать и подключить внешний поиск skills.
- Technical value: Отдельный read-only discovery adapter с provenance, лицензией, pin и preview.
- Product value: Нужный skill можно найти вне локального каталога и осознанно добавить.
- Scope: `apps/local-service/src/team/service.mts`; `apps/local-service/src/team/sources.mts`; `apps/web/src/features/team/TeamManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Нужный skill можно найти вне локального каталога и осознанно добавить. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build выбран разрешённый источник, network/privacy policy и формат результата. AC2: Поиск показывает origin/license/revision; timeout/offline не ломают локальный каталог. AC3: Поиск ничего не устанавливает; добавление проходит существующий preview/apply и проверяет drift и зависимости.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/team-review-repair.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: external_source_design_and_authority_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 4–8 ч design; build после выбора адаптера; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: external_source_design_and_authority_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-13`

- Task: PAOS-FUNC-13 — Добавить безопасное применение document proposals
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-02`, `PAOS-FUNC-08`
- Blocks: нет
- Source: Текущая политика staged_only, applied:false. [apps/local-service/src/artifacts/service.mts](../apps/local-service/src/artifacts/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Добавить безопасное применение document proposals.
- Technical value: Preview-bound compare-and-swap writer с сохранением пользовательских правок и recovery.
- Product value: Согласованное предложение можно довести до изменения документа внутри приложения.
- Scope: `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/http/application.mts`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Согласованное предложение можно довести до изменения документа внутри приложения. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build утверждены writer authority, source-vs-SQL ownership и eligible documents. AC2: Apply меняет только проверенный файл при совпавшей revision; внешний edit вызывает conflict без overwrite. AC3: Повтор apply идемпотентен; crash/rollback и sensitive paths проверены; staged/applied/accepted показываются отдельно.
- Verification gates: `node --test tests/web/skill-generation-artifacts.test.mts`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: document_write_authority_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после утверждения write contract; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: document_write_authority_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-14`

- Task: PAOS-FUNC-14 — Расширить полезность и устойчивость карты проекта
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-02`, `PAOS-FUNC-09`, `PAOS-FUNC-27`, `PAOS-FUNC-28`
- Blocks: нет
- Source: lexical_subset_only, imports unresolved, memory-only index. [apps/local-service/src/code-index/service.mts](../apps/local-service/src/code-index/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Расширить полезность и устойчивость карты проекта.
- Technical value: Выбрать поддержку языков/связей; durable revision index, imports resolution и честный coverage.
- Product value: Карта помогает оценить влияние изменения, а не создаёт видимость полного анализа.
- Scope: `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/code-index/lexical.mts`; `apps/local-service/src/impact/service.mts`; `apps/web/src/features/graph/GraphExplorer.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Карта помогает оценить влияние изменения, а не создаёт видимость полного анализа. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build утверждена матрица поддерживаемых языков и типов связей; unsupported semantics остаются явно отмеченными. AC2: Для выбранного scope cross-file imports/aliases проверяются на эталонных fixtures; unresolved не становится ложным ребром. AC3: Restart/rebuild сохраняет либо явно инвалидирует revision; D3/Mermaid/list и impact показывают один набор данных. AC4: Graph consumer использует inventory F28 и этап code в F27; discovered/readable/indexed/unsupported/excluded/error различаются. Нулевой или успешный JS/TS индекс не означает полного анализа проекта. AC5: Ready/stale/unavailable графа не блокирует дерево F26; restart/cancel/retry не публикуют устаревший результат, недоступный parser оставляет другие результаты сканирования доступными.
- Verification gates: `npm run test:web-m1`; `node --test tests/web/ui-v3-diagram.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: language_semantics_storage_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после выбора языков; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + graph-cockpit-engineer + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: language_semantics_storage_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-15`

- Task: PAOS-FUNC-15 — Уточнить и расширить границы автономности
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-10`, `PAOS-FUNC-11`
- Blocks: нет
- Source: Scope executable только '.', hostToolsConstrained=false, tokenCostMetering unavailable. [apps/local-service/src/autonomy-policy/service.mts](../apps/local-service/src/autonomy-policy/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Уточнить и расширить границы автономности.
- Technical value: Capability-based file/operation/cost policy без обещаний ограничения всего App host.
- Product value: Пользователь понимает и контролирует допустимую самостоятельность агента.
- Scope: `apps/local-service/src/autonomy-policy/service.mts`; `packages/contracts/autonomy/policy.ts`; `apps/local-service/src/runtime/sandbox-broker.mts`; `apps/web/src/features/autonomy/AutonomyManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Пользователь понимает и контролирует допустимую самостоятельность агента. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build документированы enforceable границы и невозможные обещания; narrow-path execution без enforcement отклоняется. AC2: В разрешённом маршруте выход за scope/лимит останавливает новые dispatch; unknown outcome остаётся fenced. AC3: Денежный лимит допускается только при достаточном metering/reservation изF11; иначе UI явно сообщает недоступность.
- Verification gates: `node --test tests/web/autonomy-policy.test.mts tests/web/autonomy-runtime.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: enforcement_capability_and_owner_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после подтверждения enforcement; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + security-privacy-supply-chain-reviewer + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: enforcement_capability_and_owner_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-16`

- Task: PAOS-FUNC-16 — Подтверждать доступную историю и реально загруженные профили
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`
- Blocks: нет
- Source: host_history_not_exposed; loadedVersion/observedModel/observedEffort unknown. [apps/local-service/src/sessions/service.mts](../apps/local-service/src/sessions/service.mts), [apps/local-service/src/team/service.mts](../apps/local-service/src/team/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Подтверждать доступную историю и реально загруженные профили.
- Technical value: Развести configured/pinned/observed model, effort и asset version; capability-based history adapter.
- Product value: Пользователь знает, какой агент фактически работал и какая часть истории доступна.
- Scope: `apps/local-service/src/sessions/service.mts`; `apps/local-service/src/team/service.mts`; `packages/contracts/team/assets.ts`; `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/team/TeamManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Пользователь знает, какой агент фактически работал и какая часть истории доступна. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build проверен поддерживаемый host contract; недоступная история не извлекается обходом приватных хранилищ. AC2: UI различает configured/pinned/observed; loadedVersion появляется только из подтверждённого события. AC3: Reconnect/profile switch не смешивают историю и identity; partial coverage и отсутствие attestation объясняются.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/team-run-navigation.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: supported_host_capability_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 6–12 ч capability review; build после подтверждения API; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: supported_host_capability_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-17`

- Task: PAOS-FUNC-17 — Подготовить удобную установку, обновление и rollback
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-22`
- Blocks: нет
- Source: Portable CLI есть; signed installer/auto-update не заявлены. [apps/desktop-local/README.md](../apps/desktop-local/README.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Подготовить удобную установку, обновление и rollback.
- Technical value: Поверх переносимого package задать version/digest/signing, compatibility и recovery UX.
- Product value: Обновление не требует ручного подбора каталогов и не ставит данные под угрозу.
- Scope: `apps/desktop-local/distribution.mts`; `apps/desktop-local/main.mts`; `apps/desktop-local/README.md`; `apps/launcher/launcher.ts`; `tests/web/desktop-local.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Обновление не требует ручного подбора каталогов и не ставит данные под угрозу. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build выбраны канал доставки, формат installer, signing и AUTH/licensing gates; публикация отдельно. AC2: Synthetic install/update/rollback сохраняют профиль; incompatible schema/tuple блокируют запуск с понятным восстановлением. AC3: Не удаляются пользовательские профили и старые версии без отдельного решения; новый чистый Windows-профиль проходит согласованный сценарий.
- Verification gates: `node --test tests/web/desktop-local.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: distribution_signing_commercial_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после выбора канала; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: release-operator + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: distribution_signing_commercial_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-18`

- Task: PAOS-FUNC-18 — Согласовать обновление снимков задач и dashboard
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Доработка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-07`, `PAOS-FUNC-26`, `PAOS-FUNC-27`
- Blocks: `PAOS-FUNC-19`
- Source: Task/dashboard преимущественно initial/manual snapshots, queue polling отдельно. [apps/web/src/features/tasks/TaskManager.tsx](../apps/web/src/features/tasks/TaskManager.tsx), [apps/web/src/features/dashboard/Dashboard.tsx](../apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Согласовать обновление снимков задач и dashboard.
- Technical value: Определить refresh/invalidation contract при фоне, мутациях и смене проекта.
- Product value: После выполнения пользователь видит актуальный статус без угадывания, какой экран обновить.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/api/latest-request.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/local-service/src/project-scans/service.mts` (новый планируемый файл). Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: После выполнения пользователь видит актуальный статус без угадывания, какой экран обновить. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Изменение задачи/очереди в другом разрешённом канале либо обновляет экран, либо явно делает snapshot устаревшим. AC2: Поздний ответ предыдущего проекта не заменяет текущие данные; dirty editor не перезаписывается refresh. AC3: Polling/subscription останавливаются при unmount и не создают неограниченную нагрузку. AC4: Create/modify/rename/delete и изменение policy/root инвалидируют затронутые directory/document/graph/analysis snapshots; выбран watcher либо bounded rescan/refresh с явной свежестью, без обещания невыбранного live watcher. AC5: Scan events имеют scanId/revision; позднее событие отменённого задания или другого проекта не меняет UI. После возврата/restart отображается сохранённый scan status без перезаписи черновиков.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: freshness_contract_before_build; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: freshness_contract_before_build; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-19`

- Task: PAOS-FUNC-19 — Проверить сквозной функционал на текущей сборке
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-02`, `PAOS-FUNC-03`, `PAOS-FUNC-04`, `PAOS-FUNC-05`, `PAOS-FUNC-06`, `PAOS-FUNC-07`, `PAOS-FUNC-10`, `PAOS-FUNC-18`, `PAOS-FUNC-24`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`
- Blocks: `PAOS-FUNC-23`
- Source: Redesign receipts visual/synthetic не доказывают новый native full path. [design/2026-11-13-v3/implementation-evidence.md](../design/2026-11-13-v3/implementation-evidence.md), [TEST.md](../TEST.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Проверить сквозной функционал на текущей сборке.
- Technical value: Связать real UI/API/storage/native receipts с одним revision без подмены execution mock-данными.
- Product value: Пользователь проходит весь рабочий путь и получает проверяемый результат.
- Scope: `tests/web/single-window/m4-integration-acceptance.mts`; `tests/web/single-window/m2-task-manager-browser-acceptance.mts`; `tests/web/single-window/m2b-browser-acceptance.mts`; `tests/web/single-window/m2c-browser-acceptance.mts`; `tests/web/single-window/project-files-browser-acceptance.mts` (новый планируемый файл); `tests/web/project-files.test.mts` (новый планируемый файл); `tests/web/project-scans.test.mts` (новый планируемый файл); `tests/web/project-analysis.test.mts` (новый планируемый файл). Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь проходит весь рабочий путь и получает проверяемый результат. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Synthetic путь task→assignment→run→approval→command→diff/checks→owner acceptance проходит на текущем build. AC2: Формы, custom workflow, RU/EN, обе темы, keyboard, links и partial/error состояния проверены послеF02–F07/F10/F18. AC3: Actual App/model roundtrip и генерация agent/skill проверяются только при отдельном разрешении; без него фиксируется live gap, synthetic pass его не закрывает. AC4: На synthetic fixture пройден путь Add → немедленно доступное дерево → этапы сканирования → preview допустимого файла → file reference задачи; карта и discovery не подменяют полноту файлового дерева. AC5: Проверены empty/no-Control-plane/Python-only/mixed проекты, Unicode/пробелы, unreadable/oversized/binary/invalid-encoding, ignore/sensitive/link/traversal, rename/delete/root drift во время scan, cancel/restart/retry и два проекта. Ошибка отдельного файла сохраняет разрешённую часть, root violation блокируется; до/после target hashes совпадают. AC6: RU/EN, две темы, keyboard/focus, pagination, явная неполнота поиска и отсутствие false-ready проверены; fixtures не используют реальные профили/credentials и не запускают target scripts.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1`; `npm run build:web` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: separate_synthetic_and_actual_runtime_receipts; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч без ожидания live approval; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + reviewer; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: separate_synthetic_and_actual_runtime_receipts; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-20`

- Task: PAOS-FUNC-20 — Измерить масштабирование и длительную работу
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`
- Blocks: `PAOS-FUNC-09`
- Source: Большие проекты/long-running после redesign не измерены; runtime index/cache caps. [research/product-agent-os-web-prd-2026-11-05.md](../research/product-agent-os-web-prd-2026-11-05.md), [apps/local-service/src/code-index/service.mts](../apps/local-service/src/code-index/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Измерить масштабирование и длительную работу.
- Technical value: Воспроизводимый workload с hardware/cache profile, latency/RSS/queue-depth и error budgets.
- Product value: Большой проект и длительная сессия остаются управляемыми.
- Scope: `tests/web/storage.test.mts`; `tests/web/code-index.test.mts`; `tests/web/ui-stream-search.test.mts`; `tests/web/single-window/functional-scale-acceptance.mts` (новый планируемый файл); `research/product-agent-os-web-prd-2026-11-05.md`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/project-inventory/service.mts` (новый планируемый файл); `apps/local-service/src/project-scans/service.mts` (новый планируемый файл); `apps/local-service/src/project-analysis/service.mts` (новый планируемый файл). Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Большой проект и длительная сессия остаются управляемыми. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Зафиксированы hardware/cache и объёмы:10k задач,100k сообщений,1k файлов; границы1001 файлов и9 проектов проверены отдельно. AC2: Измерены cold startup, search/list/event-visible latency, RSS и снимки в повторяемом длительном прогоне; нет скрытой потери данных. AC3: Результаты сравнены с WEB-NFR и согласованными порогами; deviations заведены вF09, неподдерживаемые объёмы явно ограничены. AC4: До замеров фиксируются budgets и dataset: большой monorepo, широкая/глубокая директория, пустые папки, generated/vendor/ignored, binary/large, mixed languages. Измеряются registration-to-tree, раскрытие/поиск, scan phases, cancellation latency, restart recovery, RSS, количество обходов и прочитанных bytes. AC5: Границы старых лимитов 1000/1001 файлов, 10000/10001 записей, depth32/33, 512KiB и 8MiB проверяются как корректный partial/bounded outcome, а не требование снять guards. Metadata listing не обязано читать содержимое всего проекта. AC6: Baseline допускается до F26–F29; окончательное закрытие F20 требует их версии и сравнения с baseline. F09 использует этот протокол для before/after; benchmark не меняет user workspace.
- Verification gates: `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: benchmark_protocol_and_thresholds_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + architect; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: benchmark_protocol_and_thresholds_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-21`

- Task: PAOS-FUNC-21 — Перепроверить очередь, Stop и crash recovery
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-23`
- Source: Recovery/ownership implemented; необходим current-run regression. [apps/local-service/src/recovery/recipe-checkpoint.mts](../apps/local-service/src/recovery/recipe-checkpoint.mts), [apps/local-service/src/scheduler/service.mts](../apps/local-service/src/scheduler/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Перепроверить очередь, Stop и crash recovery.
- Technical value: Проверить identity/CAS/lease/ownership fences и отсутствие replay в отказах.
- Product value: Потеря соединения не запускает задачу дважды и не теряет результат.
- Scope: `tests/web/recipe-recovery.test.mts`; `tests/web/recipe-crash.test.mts`; `tests/web/scheduler-runtime.test.mts`; `tests/web/parallel-workspaces.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Потеря соединения не запускает задачу дважды и не теряет результат. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Crash до dispatch, после dispatch до receipt и после terminal receipt покрыты отдельными сценариями. AC2: Stop без ACK не освобождает ownership; lost consumer/timeout требуют корректной сверки. AC3: В разных roots разрешённая параллельность сохраняется, overlapping roots блокируются; selective Stop не отменяет чужой run.
- Verification gates: `node --test tests/web/recipe-recovery.test.mts tests/web/recipe-crash.test.mts tests/web/scheduler-runtime.test.mts tests/web/parallel-workspaces.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: disposable_profiles_only; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + reviewer; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: disposable_profiles_only; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-22`

- Task: PAOS-FUNC-22 — Перепроверить импорт, backup и restore
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-17`, `PAOS-FUNC-23`
- Source: Import/backup контракты есть; current combined verification отсутствует. [apps/local-service/src/import-export/migration.mts](../apps/local-service/src/import-export/migration.mts), [apps/desktop-local/README.md](../apps/desktop-local/README.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Перепроверить импорт, backup и restore.
- Technical value: Проверить source authority, freeze/CAS, counts/hashes/FK, blobs и идемпотентность.
- Product value: Задачи, история и вложения сохраняются при переносе и восстановлении.
- Scope: `tests/web/domain-migration.test.mts`; `tests/web/storage-backup.test.mts`; `apps/local-service/src/import-export/migration.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Задачи, история и вложения сохраняются при переносе и восстановлении. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Source drift и неизвестный writer останавливают cutover; две writable authority не появляются. AC2: Corrupt/missing blob, прерванный import и повтор запроса дают безопасный результат без дублей. AC3: Restore в новый synthetic profile сохраняет данные и ссылки; старый профиль неизменён; credentials/pending operations не воспроизводятся.
- Verification gates: `node --test tests/web/domain-migration.test.mts tests/web/storage-backup.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: synthetic_data_no_real_profile_mutation; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + reviewer; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: synthetic_data_no_real_profile_mutation; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-23`

- Task: PAOS-FUNC-23 — Провести продуктовую приёмку ключевых сценариев
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-19`, `PAOS-FUNC-21`, `PAOS-FUNC-22`, `PAOS-FUNC-24`
- Blocks: нет
- Source: PRD pilot metrics и UI-12 acceptance остаются отдельными gates. [research/product-agent-os-web-prd-2026-11-05.md](../research/product-agent-os-web-prd-2026-11-05.md), [design/2026-11-13-v3/implementation-plan.md](../design/2026-11-13-v3/implementation-plan.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Провести продуктовую приёмку ключевых сценариев.
- Technical value: Связать acceptance с наблюдаемой корректностью решений, а не числом кликов.
- Product value: Пользователь без подсказки понимает статус, blocker, evidence и следующий шаг.
- Scope: `research/product-agent-os-web-prd-2026-11-05.md`; `design/2026-11-13-v3/implementation-plan.md`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь без подсказки понимает статус, blocker, evidence и следующий шаг. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До пилота согласованы участники, сценарии, opt-in/retention и baseline MD/chat; production data не обязательны. AC2: Пройдены первое открытие, возвращение, конфликт, partial evidence и приёмка; ошибки понимания фиксируются вместе с успехами. AC3: Цели4/5 за3мин и3/5 повторное использование за14дней изPRD проверяются как гипотезы; ноль ложных трактовок verified и потерь данных; owner принимает результат отдельно. AC4: В пилот добавлены выбор папки, поиск обычного файла вне Control-plane, объяснение excluded/unsupported/partial, отмена/повтор и возвращение после restart. Наблюдатель проверяет, что участник не путает видимость файла, успешную индексацию и разрешение на исполнение.
- Verification gates: Наблюдаемый пилот по согласованному протоколу; автоматического эквивалента human acceptance нет. Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: human_pilot_protocol_and_consent_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч подготовки/анализа плюс14дней наблюдения, не срок разработки; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: product-manager + tester; human acceptance — владелец; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: human_pilot_protocol_and_consent_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-24`

- Task: PAOS-FUNC-24 — Объяснять доступность функций в момент действия
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Доработка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-10`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-23`
- Source: Ряд экранов уже отображает unknown/staged; нужна единая journey-проверка. [apps/web/src/ui/ConnectionControls.tsx](../apps/web/src/ui/ConnectionControls.tsx), [apps/web/src/features/artifacts/ArtifactExplorer.tsx](../apps/web/src/features/artifacts/ArtifactExplorer.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Объяснять доступность функций в момент действия.
- Technical value: Единый capability vocabulary для staged/unsupported/partial/connected/qualified/accepted.
- Product value: Пользователь отличает доступную функцию от экрана с будущей возможностью.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/ui/ConnectionControls.tsx`; `apps/web/src/locales/app.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/web/src/features/projects/ProjectAnalysis.tsx` (новый планируемый файл). Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь отличает доступную функцию от экрана с будущей возможностью. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Для usage, graph, proposals, skills discovery, history, autonomy и runtime рядом с действием показаны реальный scope и причина недоступности. AC2: Есть конкретный следующий шаг; unsupported не выглядит как loading, connected не называется execution-qualified. AC3: RU/EN и accessibility состояния проверены; нет повторного запроса уже действующей bounded authority. AC4: В onboarding и проекте показаны независимые registration/tree/inventory/documents/code/analysis состояния F26–F29, время и scope наблюдения; counts.files не называется indexed без соответствующего покрытия. AC5: Empty/no-supported-code не получает ложный «проект полностью проанализирован»; excluded/error/unsupported объясняют причину и действие. Недоступный parser/core adapter не скрывает доступное дерево, контрольный список Control-plane явно назван отдельным фильтром.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: capability_wording_review_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: product-manager + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить зависимости и актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: capability_wording_review_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-25`

- Task: PAOS-FUNC-25 — Согласовать текущие продуктовые статусы и критерии
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Документация; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: нет
- Source: Датированные addenda сосуществуют с ранними status blocks; нужен current-state entry. Текущий docs unittest: 4 failures из-за отсутствующих rendered accessibility/pilot RU/EN и search/sitemap parity. [research/product-agent-os-web-prd-2026-11-05.md](../research/product-agent-os-web-prd-2026-11-05.md), [PLAN.md](../PLAN.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Согласовать текущие продуктовые статусы и критерии.
- Technical value: Один актуальный указатель PRD/architecture/plan/registry с сохранённой историей.
- Product value: План и документация ясно показывают, что работает, ограничено и ждёт проверки.
- Scope: `research/product-agent-os-web-prd-2026-11-05.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `research/product-agent-os-web-task-manager-plan-2026-11-09.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/web/accessibility.md`; `docs/web/accessibility.en.md`; `docs/web/pilot.md`; `docs/web/pilot.en.md`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: План и документация ясно показывают, что работает, ограничено и ждёт проверки. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Текущие scope/status/acceptance не противоречат историческим implementation_not_started/API-only блокам: история явно помечена и маршрутизирована. AC2: Для F01–F29 и M5 есть единый owner/status/source; implemented не подменяет human/live acceptance. AC3: Синхронизированы только изменённые claims и RU/EN registry; validators/docs tests проходят, старые56cards сохранены. AC4: Текущая проверка docs-site больше не сообщает missing web/accessibility.html и web/pilot.html в RU/EN; search/sitemap/switcher parity подтверждён на явно выбранном build. Публикация и promotion сайта отдельно. AC5: Документы различают «Источники», файловое дерево F26, сканирование F27, inventory policy F28 и discovery F29; версии API/coverage, recovery и ограничения описаны в existing PRD/architecture, без заявления об автоматическом ремонте или полной семантике.
- Verification gates: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`; `python tools/check_docs.py`; `git diff --check` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: source_reconciliation_not_history_deletion; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 4–8 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: docs-maintainer + product-manager; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: source_reconciliation_not_history_deletion; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.


### Task `PAOS-FUNC-26`

- Task: PAOS-FUNC-26 — Добавить файловый браузер проекта
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; разрешена запись плана, build не начат.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-10`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`
- Source: Sources показывает шесть фиксированных Control-plane файлов; catalog читает .md/.txt, graph — отобранные исходники. Общего дерева и независимого directory API в проверенном onboarding нет. [apps/local-service/src/adapters/project-sources.ts](../apps/local-service/src/adapters/project-sources.ts), [apps/web/src/ui/Operations.tsx](../apps/web/src/ui/Operations.tsx), [apps/local-service/src/artifacts/service.mts](../apps/local-service/src/artifacts/service.mts), [apps/web/src/features/graph/GraphExplorer.tsx](../apps/web/src/features/graph/GraphExplorer.tsx). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Добавить файловый браузер проекта.
- Technical value: Независимый от графа API директорий и безопасного чтения с ленивой загрузкой, стабильными ссылками и ограниченными ответами.
- Product value: Пользователь видит структуру выбранной папки и открывает доступные файлы, даже когда индекс не готов или язык не поддерживается.
- Scope: `packages/contracts/project-files.ts` (новый планируемый файл); `apps/local-service/src/project-files/service.mts` (новый планируемый файл); `apps/local-service/src/http/application.mts`; `apps/web/src/api/client.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл); `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/locales/app.ts`; `tests/web/project-files.test.mts` (новый планируемый файл); `tests/web/single-window/project-files-browser-acceptance.mts` (новый планируемый файл). Названия новых файлов — проектный scope, сейчас они не создаются.
- Architecture boundary: project-files API → checked filesystem metadata/read → ProjectFiles UI; graph readiness не является precondition.
- Non-goals: Редактирование, удаление и перемещение файлов; terminal; выполнение preview-кода; автоматическая передача содержимого модели.
- Expected result: Проверяемое дерево и read-only reader, typed API, focused/browser receipts в этой карточке.
- Acceptance criteria: AC1: После регистрации раздел «Файлы» доступен без графа и завершённого сканирования; видны вложенные и пустые каталоги, исходники, конфигурации и бинарные файлы как метаданные, в пределах разрешённой политики F28. AC2: Раскрытие каталога загружает только нужную ветку; pagination и фильтры показывают границы выборки; поиск по имени/пути явно сообщает scope. Метаданные содержат relativePath, тип, размер, modifiedAt и состояние доступа. AC3: Текст читается по отдельному запросу с проверкой root identity, revision, размера и кодировки; binary/oversized/unreadable получают объяснение. Неподдерживаемое индексатором расширение не скрывает файл. HTML/скрипты не исполняются при просмотре. AC4: Нет чтения за пределами корня через traversal, symlink/junction/hardlink и подмену каталога; sensitive content не раскрывается. Выбор файла не передаёт весь проект модели и не выдаёт разрешение на выполнение. AC5: Выбранный путь можно скопировать и использовать как file reference; Control-plane — фильтр над реальными путями. Смена проекта и поздний ответ не смешивают дерево; RU/EN, keyboard, focus, empty/error/loading проверены.
- Verification gates: `node --test tests/web/project-files.test.mts tests/web/project-inventory.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`; `npm run build:web`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: directory_api_ui_contract_review_required; status=proposal_staged, владелец design gate — builder + tester; product-manager принимает сценарий просмотра. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 24–40 ч, rough planning range; уточнить после API/UI контракта; не обязательство по сроку.
- Agents: builder + tester; product-manager принимает сценарий просмотра; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Проверяемое дерево и read-only reader, typed API, focused/browser receipts в этой карточке. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Next step: проверить зависимости, актуальный source и directory_api_ui_contract_review_required; согласовать минимальный slice и бюджеты, затем воспроизводимые проверки.

#### Completion Report

- status: planned
- what was done: задача и критерии добавлены в план; реализация не начата.
- files touched / work locations: implementation none; будущие work locations указаны в Scope.
- technical value delivered: результат реализации пока не получен.
- product value delivered: пользовательский сценарий ещё не реализован и не принят.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: исходный статический анализ; команды из Verification gates являются будущими проверками, не receipts.
- residual risks: directory_api_ui_contract_review_required; scanner completeness, data safety и runtime требуют реализации и текущего evidence.
- follow-up: Next step выше; не закрывать задачу одним design review.
- Documentation impact: при изменении contracts/coverage/recovery синхронизировать existing PRD/architecture, план, registry и только затронутые control-plane owners; текущий scope planning_only.

### Task `PAOS-FUNC-27`

- Task: PAOS-FUNC-27 — Сделать сканирование управляемым фоновым заданием
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; разрешена запись плана, build не начат.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-14`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`, `PAOS-FUNC-29`
- Source: POST /projects коммитит регистрацию, затем ожидает inspectProjectSources/codeIndex.rebuild. Scan summary не является durable job; once receipts находятся в памяти и истекают через 10 минут. [apps/local-service/src/http/application.mts](../apps/local-service/src/http/application.mts), [apps/local-service/src/storage/sqlite-worker.mts](../apps/local-service/src/storage/sqlite-worker.mts), [apps/web/src/features/projects/ProjectOnboarding.tsx](../apps/web/src/features/projects/ProjectOnboarding.tsx), [tests/web/settings-desktop.test.mts](../tests/web/settings-desktop.test.mts). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Сделать сканирование управляемым фоновым заданием.
- Technical value: Сохраняемые scan ID и этапы, bounded worker, идемпотентность, отмена, повтор и восстановление отдельно от регистрации проекта.
- Product value: Проект доступен сразу после регистрации; пользователь видит ход сканирования, частичный результат и способ продолжить после сбоя.
- Scope: `packages/contracts/project-scan.ts` (новый планируемый файл); `apps/local-service/src/project-scans/service.mts` (новый планируемый файл); `apps/local-service/src/http/application.mts`; `apps/local-service/src/storage/local-store.mts`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/storage/migrations/schema.mts`; `apps/local-service/src/code-index/service.mts`; `apps/web/src/api/client.ts`; `apps/web/src/features/projects/ProjectOnboarding.tsx`; `tests/web/project-scans.test.mts` (новый планируемый файл); `tests/web/settings-desktop.test.mts`. Названия новых файлов — проектный scope, сейчас они не создаются.
- Architecture boundary: project registration → profile-owned scan job → bounded analyzers; независимые lifecycle и source authority.
- Non-goals: Запуск задач/агентов, provider calls, автоматическое выполнение команд проекта и изменение target-файлов; бесконечный watchdog.
- Expected result: Durable scan lifecycle и UI прогресса; schema compatibility/rollback и crash/cancel/retry receipts.
- Acceptance criteria: AC1: Регистрация сохраняется один раз и возвращает доступный проект без ожидания полного обхода; scan status содержит scanId, root identity, policy version, этап inventory/documents/code/analysis, начало/обновление, счётчики и причины partial/error. AC2: Повтор Add/retry в том числе после restart не создаёт новый проект или дублирующую работу; конкурентные запросы одной revision объединяются либо получают объяснимый conflict. Изменившийся root не продолжает старое задание. AC3: Cancel останавливает дальнейшую работу и позднюю публикацию; повтор запускается с явно определённой revision. Restart восстанавливает либо переводит задание в recovery_required/interrupted; незавершённое не становится completed. AC4: Заданы budgets времени/памяти/записей и concurrency; failure одного анализатора сохраняет допустимые результаты других этапов. Ready одного индекса не означает полный анализ проекта; неподключённый analysis adapter отображается как unavailable. AC5: Состояние и последнее успешное покрытие доступны после открытия Settings/проекта и restart; events или bounded polling не перезаписывают более новую revision. Scan bookkeeping остаётся в профиле PAOS, target workspace не изменяется.
- Verification gates: `node --test tests/web/project-scans.test.mts tests/web/settings-desktop.test.mts tests/web/code-index.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: persisted_scan_state_recovery_schema_design_required; status=proposal_staged, владелец design gate — architect + builder + tester. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 24–40 ч, rough planning range; storage/recovery design до build; не обязательство по сроку.
- Agents: architect + builder + tester; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Durable scan lifecycle и UI прогресса; schema compatibility/rollback и crash/cancel/retry receipts. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Next step: проверить зависимости, актуальный source и persisted_scan_state_recovery_schema_design_required; согласовать минимальный slice и бюджеты, затем воспроизводимые проверки.

#### Completion Report

- status: planned
- what was done: задача и критерии добавлены в план; реализация не начата.
- files touched / work locations: implementation none; будущие work locations указаны в Scope.
- technical value delivered: результат реализации пока не получен.
- product value delivered: пользовательский сценарий ещё не реализован и не принят.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: исходный статический анализ; команды из Verification gates являются будущими проверками, не receipts.
- residual risks: persisted_scan_state_recovery_schema_design_required; scanner completeness, data safety и runtime требуют реализации и текущего evidence.
- follow-up: Next step выше; не закрывать задачу одним design review.
- Documentation impact: при изменении contracts/coverage/recovery синхронизировать existing PRD/architecture, план, registry и только затронутые control-plane owners; текущий scope planning_only.

### Task `PAOS-FUNC-28`

- Task: PAOS-FUNC-28 — Унифицировать инвентаризацию, покрытие и исключения
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; разрешена запись плана, build не начат.
- Depends on: нет
- Blocks: `PAOS-FUNC-02`, `PAOS-FUNC-10`, `PAOS-FUNC-14`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`
- Source: scanCheckedSources использует жёсткий denylist и extension filter, не возвращает все пропуски и не читает .gitignore; лимит подходящих файлов может оборвать обход. Metadata, read и indexing coverage требуют раздельного контракта. [apps/local-service/src/code-index/sources.mts](../apps/local-service/src/code-index/sources.mts), [apps/local-service/src/code-index/service.mts](../apps/local-service/src/code-index/service.mts), [apps/local-service/src/artifacts/service.mts](../apps/local-service/src/artifacts/service.mts), [apps/local-service/src/adapters/project-sources.ts](../apps/local-service/src/adapters/project-sources.ts). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Унифицировать инвентаризацию, покрытие и исключения.
- Technical value: Общий контракт путей, revision и coverage для directory/document/code consumers при раздельных правах listing, reading и indexing.
- Product value: Файлы не исчезают из обзора из-за отсутствия языкового анализатора; пользователь понимает, что найдено, пропущено или недоступно.
- Scope: `packages/contracts/project-inventory.ts` (новый планируемый файл); `apps/local-service/src/project-inventory/service.mts` (новый планируемый файл); `apps/local-service/src/code-index/sources.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/adapters/project-sources.ts`; `tests/web/project-inventory.test.mts` (новый планируемый файл); `tests/web/code-index.test.mts`; `tests/web/skill-generation-artifacts.test.mts`. Названия новых файлов — проектный scope, сейчас они не создаются.
- Architecture boundary: checked filesystem inventory → per-consumer visibility/read/index policy; source root остаётся владельцем файлов.
- Non-goals: Безусловное снятие существующих лимитов или denylist; полный обход excluded directories; секреты в индексах; новый независимый scanner без оценки reuse.
- Expected result: Общий inventory/coverage contract и миграция потребителей без ослабления guards; fixture evidence.
- Acceptance criteria: AC1: Контракт различает discovered, readable, indexed, unsupported, excluded и error; счётчики определяют разные стадии и не суммируют пересекающиеся множества как общее число файлов. Empty и unknown отличаются; отсутствие подходящего кода не означает полный анализ. AC2: Файловое дерево независимо от набора расширений индексатора. .gitignore и project include/exclude имеют явную precedence и разные правила видимости/индексации; ignore не выдаёт права доступа. Sensitive paths/content защищены даже при include override. AC3: Отчёт показывает применённую policy version, причины пропуска, лимиты и partial coverage. Тяжёлые generated/vendor каталоги не читаются без необходимости; разрешённое раскрытие метаданных не снимает ограничений чтения содержимого. AC4: Ошибка, превышение размера или unsupported encoding отдельного файла сохраняет другие разрешённые записи; directory-level denial помечает неполноту. При root identity drift, попытке выхода за корень или недостоверной revision публикация небезопасного результата блокируется. AC5: Bounded/paged inventory поддерживает normalised relative paths, Unicode/пробелы и Windows case semantics; ссылки и race conditions не расширяют root. Одинаковые policy/root/revision дают согласованные ссылки и причины во всех consumers. AC6: Изменение политики инвалидирует затронутые snapshots; file metadata не требует полного чтения всех исходников. Позитивные/отрицательные сценарии и нагрузочные границы проверены; исходники проекта не меняются.
- Verification gates: `node --test tests/web/project-inventory.test.mts tests/web/code-index.test.mts tests/web/skill-generation-artifacts.test.mts tests/web/settings-desktop.test.mts`; `npm run check:web-m1`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: inventory_policy_security_boundary_design_required; status=proposal_staged, владелец design gate — architect + builder + security-privacy-supply-chain-reviewer + tester. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 12–20 ч, rough planning range; выбрать reuse/adapter до build; не обязательство по сроку.
- Agents: architect + builder + security-privacy-supply-chain-reviewer + tester; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Общий inventory/coverage contract и миграция потребителей без ослабления guards; fixture evidence. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Next step: проверить зависимости, актуальный source и inventory_policy_security_boundary_design_required; согласовать минимальный slice и бюджеты, затем воспроизводимые проверки.

#### Completion Report

- status: planned
- what was done: задача и критерии добавлены в план; реализация не начата.
- files touched / work locations: implementation none; будущие work locations указаны в Scope.
- technical value delivered: результат реализации пока не получен.
- product value delivered: пользовательский сценарий ещё не реализован и не принят.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: исходный статический анализ; команды из Verification gates являются будущими проверками, не receipts.
- residual risks: inventory_policy_security_boundary_design_required; scanner completeness, data safety и runtime требуют реализации и текущего evidence.
- follow-up: Next step выше; не закрывать задачу одним design review.
- Documentation impact: при изменении contracts/coverage/recovery синхронизировать existing PRD/architecture, план, registry и только затронутые control-plane owners; текущий scope planning_only.

### Task `PAOS-FUNC-29`

- Task: PAOS-FUNC-29 — Подключить core discovery к добавлению проекта
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; разрешена запись плана, build не начат.
- Depends on: `PAOS-FUNC-27`, `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`
- Source: Core analyze_workspace и run_first_project_analysis умеют discovery/first-run composition. Проверенный POST /projects не вызывает их: сейчас это только source inventory и code graph. [apps/local-service/src/http/application.mts](../apps/local-service/src/http/application.mts), [plugins/product-agent-os/scripts/product_agent_os/discovery.py](../plugins/product-agent-os/scripts/product_agent_os/discovery.py), [plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py](../plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Подключить core discovery к добавлению проекта.
- Technical value: Версионированный read-only adapter к существующему discovery/first-run analysis с provenance, ограничениями и invalidation.
- Product value: После добавления проекта видны стек, структура, Control-plane gaps и обоснованные следующие шаги, а не только количество узлов графа.
- Scope: `apps/local-service/src/project-analysis/service.mts` (новый планируемый файл); `packages/contracts/project-analysis.ts` (новый планируемый файл); `apps/local-service/src/project-scans/service.mts` (новый планируемый файл); `apps/local-service/src/http/application.mts`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`; `apps/web/src/features/projects/ProjectAnalysis.tsx` (новый планируемый файл); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/web/src/api/client.ts`; `tests/web/project-analysis.test.mts` (новый планируемый файл); `tests/web/single-window/project-files-browser-acceptance.mts` (новый планируемый файл). Названия новых файлов — проектный scope, сейчас они не создаются.
- Architecture boundary: profile scan stage → bounded structured core adapter → project analysis view; analysis не расширяет execution authority.
- Non-goals: Автоматический ремонт проекта, создание Control-plane, LLM-аудит, сборка/тесты target и публикация; неподтверждённые обещания полноты.
- Expected result: Read-only discovery integration и source-backed summary, capability/timeout/stale fixtures; reuse contract в существующей architecture.
- Acceptance criteria: AC1: До build выбран способ reuse существующих core discovery/first-run модулей и deployment/runtime contract. Недоступный Python/adapter/version даёт явный unavailable; установка зависимостей и альтернативный полный scanner автоматически не запускаются. AC2: Analysis запускается как отдельный этап F27, использует согласованную inventory policy F28 и возвращает schema version, source revision, stack/components, control-plane coverage, findings с источниками/confidence/limitations. AC3: Обнаруженные scripts/configs только анализируются как данные: не исполняются команды проекта, tests, hooks, модели или провайдеры; target files не создаются и не исправляются. Предложения Control-plane остаются предложениями. AC4: Пустой проект, проект без Control-plane, Python-only, mixed stack и unsupported language получают объяснимые результаты без выдуманной полноты; timeout/error сохраняют доступное дерево и уже полученное покрытие. AC5: Изменения файлов, root или inventory policy делают прежние выводы stale; повтор и restart не смешивают revisions. Выводы доступны из выбранного проекта в RU/EN, связаны с разрешёнными file references и не раскрывают secrets.
- Verification gates: `node --test tests/web/project-analysis.test.mts tests/web/project-scans.test.mts tests/web/settings-desktop.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: core_adapter_capability_contract_and_readonly_review_required; status=proposal_staged, владелец design gate — architect + plugin-runtime-builder + builder + tester. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 16–32 ч, rough planning range; integration/packaging выбор до build; не обязательство по сроку.
- Agents: architect + plugin-runtime-builder + builder + tester; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Read-only discovery integration и source-backed summary, capability/timeout/stale fixtures; reuse contract в существующей architecture. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Next step: проверить зависимости, актуальный source и core_adapter_capability_contract_and_readonly_review_required; согласовать минимальный slice и бюджеты, затем воспроизводимые проверки.

#### Completion Report

- status: planned
- what was done: задача и критерии добавлены в план; реализация не начата.
- files touched / work locations: implementation none; будущие work locations указаны в Scope.
- technical value delivered: результат реализации пока не получен.
- product value delivered: пользовательский сценарий ещё не реализован и не принят.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: исходный статический анализ; команды из Verification gates являются будущими проверками, не receipts.
- residual risks: core_adapter_capability_contract_and_readonly_review_required; scanner completeness, data safety и runtime требуют реализации и текущего evidence.
- follow-up: Next step выше; не закрывать задачу одним design review.
- Documentation impact: при изменении contracts/coverage/recovery синхронизировать existing PRD/architecture, план, registry и только затронутые control-plane owners; текущий scope planning_only.

## Предыдущая проверка планировки — исходные 25 задач

План записан 15.11.2026. Проверки относятся к планировке, не к выполнению PAOS-FUNC задач. Исходный Git HEAD: `8d556bf38f1398081032523785da224807948136`; worktree содержит сохранённые изменения других чатов. Context mode: `self_review`; внешняя независимая проверка не заявляется.

Первичная запись в docs/planning добавила страницу в docs-site inventory. Первый текущий прогон: matrix validator exit0; check_docs exit0; git diff --check exit0; docs unittest exit1, 105 tests / 13 failures (page counts / missing EN sibling / site parity). Это реальный неуспешный receipt. Матрица перенесена в research рядом с существующим Web-планом; тесты, navigation и generated site этой задачей не изменялись. Подробные карточки сохранены полностью, root/control-plane хранит только краткие указатели.

| Текущая проверка | Результат и предел |
| --- | --- |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/functional-remediation-2026-11-15.md` | exit0, errors=[]; 25 detailed cards |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | exit1; 105 tests, 101 passed, 4 failures; 9 ошибок размещения устранены |
| `python tools/check_docs.py` | exit0, documentation structure checks passed |
| `git diff --check` | exit0; только предупреждения CRLF→LF, не ошибки whitespace |
| Read-only Node consistency check | 25 unique IDs / 25 planned; 3 reference-only M5; DAG без циклов; AC присутствуют в MD и JSON; source/work paths и ссылки существуют, новый benchmark harness явно planned |
| Preservation check | исходный JSON M1–M5 байт-в-байт сохранён, SHA-256 `23b013be2f01f088a2de53c1748693820aa8210ed382cd22fe65ce46f3a27ef1`; исходные 56 MD-карточек и весь прежний текст 7 дополненных документов сохранены после нормализации CRLF/LF |
| Fingerprint read | текущий frontend lock SHA-256 повторно совпал с исходным наблюдением F01; manifest не менялся |

Оставшиеся четыре failures:
1. `test_track10_task26_batch34e_full_site_parity_red_gate`: отсутствуют `en/web/accessibility.html`, `en/web/pilot.html`.
2. `test_track10_task26_batch34e_m46_language_switcher_parity_is_recorded`: отсутствуют обе страницы в RU и EN.
3. `test_track10_task26_batch34e_m47_search_sitemap_parity_is_recorded`: этих RU-страниц нет в search; остальные проверки после этого assertion не доказаны.
4. `test_track10_task26_batch34e_m48_m49_final_closure_is_recorded`: те же четыре rendered artifacts отсутствуют.

Пробел передан в F25; полный docs suite не объявляется прошедшим. До изменений текущего плана baseline suite не запускался, поэтому прежний статус suite не реконструируется. Существующий site этой задачей не генерировался и свежим не объявляется. Strict MkDocs не запускался: навигация, Mermaid, extensions и source pages сайта не менялись; новый план находится вне docs-tree. Runtime/browser/native/provider/human acceptance не выполнялись.

Control-plane sync: REQUIREMENTS — scope planning only; PLAN — ссылка и порядок; TEST — компактная ссылка на проверки плана; RUNLOG — результат и ограничения; registry RU/EN — локальный источник и частичная документационная проверка. EVALS — no_change_needed, eval policy и thresholds не меняются; prod_test — not_applicable, Batch39 не затронут. Прежние разделы и чужие правки сохранены. Root control-plane после добавлений остаётся в пределах 40 000 UTF-8 bytes; TEST близок к границе и не получает подробный журнал.

Итог: `planning_recorded`, `docs_partially_verified`; backlog сформирован, ни одна новая задача не реализована. Перед началом конкретной задачи нужен её актуальный scope/reproduction/design gate. Отдельного `plan_ready` для всех расширений или product readiness нет.

## Проверка обновления F26–F29 — текущий проход

Статус: planning_recorded / docs_partially_verified. В этом проходе добавлены F26–F29, изменены AC десяти прежних задач и hard dependencies семи; Blocks и execution_order согласованы для всех 29. Все задачи planned, implementation timestamps pending_execution_timestamp. Context mode: self_review; отдельный reviewer/subagent не запускался.

| Команда / проверка текущего прохода | Наблюдаемый результат |
| --- | --- |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/functional-remediation-2026-11-15.md` | exit0, ok=true, errors=[]; 29 карточек |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | exit1; 105 tests за 12.518s, 101 passed / 4 failures |
| `python tools/check_docs.py` | exit0, documentation structure checks passed |
| `git diff --check` | exit0; CRLF/LF warnings, ошибок whitespace нет |
| Read-only consistency / preservation | 29 unique planned IDs, 3 M5 refs, DAG без циклов; Depends on/Blocks/AC каждого MD-блока совпадают с JSON; execution_order соблюдает зависимости; исходные title/status/value/estimate/date сохранены |
| Sources / work locations | Source и Markdown links существуют; новые code/test paths явно planned и не созданы. Schema/protocol design остаётся gate перед build |
| Старый Web-план | JSON группы M1–M5 байт-в-байт сохранён; исходные 56 MD-карточек и текст после изменённого верхнего указателя сохранены, включая исходные line endings |
| Ownership | Изменены только 8 документов/JSON и свой lifecycle marker. Прежние и параллельные report/read разделы сохранены; CAS остановил первую попытку записи при concurrent drift, затем внесён только собственный раздел |
| Control-plane budget | PLAN/REQUIREMENTS/RUNLOG/TEST/EVALS ниже 40 000 UTF-8 bytes; TEST.md остался без изменений, 39 985 bytes |

Четыре текущих отказа совпадают по сценарию с предыдущим прогоном: full_site_parity_red_gate, m46_language_switcher, m47_search_sitemap и m48_m49_final_closure. Причина — отсутствующие rendered `web/accessibility.html` и `web/pilot.html` в RU/EN и связанные записи поиска. Точные полные имена и missing paths сохранены выше; текущий failure не объявляется pass и не закрывает F25. Generated site, tests и приложения этой задачей не менялись; build/site promotion не выполнялись.

Перед записью собственного marker автоматический review потребовал отдельный reopening approval; владелец дал его для этой задачи документирования. Предыдущий результат marker сохранён; hook/trust/permissions не изменялись. Это процедурный receipt, не proof реализации. Приложение, будущие fixtures и новые API не реализованы.

Control-plane sync: REQUIREMENTS/PLAN/RUNLOG и RU/EN registry обновляются в существующих разделах. TEST.md no_change_needed: команды проверки и ссылка на эту матрицу уже существуют; EVALS no_change_needed: рубрики и thresholds не меняются; prod_test not_applicable: Batch39 не затронут. Application tests, browser/native/provider и human acceptance в этом planning-only проходе не запускаются.
