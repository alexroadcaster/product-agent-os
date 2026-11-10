# Product-Agent OS Web — итоговый аудит перед M1

Source status: project-local static audit / current source snapshot / official OpenAI docs checked 2026-11-10. Аудит спецификаций, не runtime/security certification. Status: audit_complete / M1_contract_changes_required; documentation_partially_verified. Дата: 2026-11-10, Europe/Moscow. Task: PAOS-WEB-M1-FINAL-AUDIT-2026-11-10.

Текущее состояние после исправлений: см. §9; исходный аудит ниже сохранён как evidence.

## 1. Вывод и граница аудита

Направление согласовано: собственный интерфейс через Codex App Server, local SQLite + FTS5, PostgreSQL + pgvector для будущей командной версии. Оснований менять выбранные engines этот аудит не выявил. Документы пока не составляют однозначный implementation contract M1: часть acceptance требует более поздней модели, semantic dependencies расходятся с DAG, не закрыты runtime/security/data-policy решения.

Рекомендация: не передавать текущий пакет как полностью согласованное ТЗ на весь M1. Можно отдельно разрешить ограниченный M1a contract/compatibility spike после фиксации его scope; storage schema, migration и real-credential runtime следует начинать только после соответствующих решений ниже. Этот отчёт не разрешает даже такой spike — пользователь запросил аудит без реализации.

P0: не заявляются; действующий Web runtime не проверялся. P1 означает решение/исправление контракта до зависящего от него кода, а не найденную production уязвимость. P2 — закрыть в M1 planning/acceptance до приёмки соответствующего сценария. P3 — устранить неоднозначность документации. Есть разница между противоречием, пробелом и честно записанным pending decision; ниже они помечены отдельно.

Проверены PRD v0.6, архитектура §19–20, весь machine task plan, связанные auth/UX contracts. Базовый Git snapshot: cc9003e733f84c86a81633fafa37431f8c62e658; worktree на старте clean. Исходные спецификации и task JSON не исправляются в рамках аудита. Runtime, credentials, API inference, installation, browser и SQL migrations не запускались.


Итого: **13 замечаний — 8 P1, 4 P2, 1 P3**. Высокий приоритет не означает запрет любой M1a работы: каждому замечанию назначена конкретная граница, до которой решение должно быть закрыто.

## 2. Что согласовано и не требует повторного выбора

- Один пользовательский интерфейс; Codex App не обязательный runtime dependency.
- SQL entity revision + audit + outbox; отсутствие обещания exactly-once внешних side effects.
- Раздельные task status, run outcome, verification и owner acceptance.
- SQLite + FTS5 local; vector search не блокирует M1; team PostgreSQL/pgvector отложен.
- Нет автоматического MD→DB cutover при discovery; unknown provenance не выдумывается; исходники сохраняются.
- После restart/restore старое approval не проигрывается; uncertain run требует reconciliation.
- Task hierarchy, Linked Issues и code graph — разные отношения; target run не определяется одним task link.
- Будущие real-runtime проверки и commercial gates явно pending; это честный предел evidence.

## 3. Существенные замечания

### WA-01 — P1 / противоречие объёма: минимальный M1 против полного round-trip миграции

**Источники:** [PRD](product-agent-os-web-prd-2026-11-05.md) L627, L675, L683–700; [архитектура](product-agent-os-web-architecture-2026-11-05.md) L611–620, L667; [план](product-agent-os-web-task-manager-plan-2026-11-09.md) L17–20, карточки 0031–0034 (L1486–1661), 0050 (L2318).

M1 — минимальная task card и одна recipe; components/versions и полная модель отнесены к M2. Одновременно ST-03 и 0050 требуют round-trip всех полей §13–14, project task scope переносится целиком, ST-AC-01–07 обязательны для M1c. Для legacy проекта с versions, links и attachments это либо скрытая реализация M2 в M1, либо гарантированно blocked cutover. Сохранить исходный MD недостаточно, чтобы назвать все его поля рабочими SQL entities после переключения.

**Закрытие:** product+architect выбирают один поддерживаемый M1 import profile. Рекомендация: минимальная SQL task модель + точные schema versions существующего PAOS JSON/MD, неподдержанный проект остаётся legacy read-only; либо полная storage schema M2 реализуется заранее, UI остаётся минимальным и это явно оценивается. Нельзя молча сократить принятое пользователем поле или объявить arbitrary MD поддержанным. Нужны field-level matrix, перечень allowlisted source formats и fixtures с accepted/rejected imports. Владельцы: 0002/0048/0050; до schema/import code.

### WA-02 — P1 / семантическая зависимость: backup готов после использующей его миграции

**Источники:** архитектура L684, L708, L712–714; план L19, 0050 L2318–2360, 0051 L2361–2403; JSON depends_on 0051 → 0050.

Cutover требует согласованного backup и test restore до переключения. Однако 0050 реализует freeze/backup/promote, а 0051 с backup/restore зависит от законченной 0050. DAG синтаксически корректен, но не представляет dependency обязательного защитного механизма. Это не математический цикл существующего DAG.

**Закрытие:** разделить 0050 на preview/staging и promote либо выделить backup primitive из 0051. Порядок: core storage → import preview и backup primitive → restore rehearsal → cutover → post-cutover/reverse-transfer tests. Не добавлять обратную зависимость 0050→0051 без декомпозиции: получится цикл. Владельцы: architect/storage/tester; до реального cutover.

### WA-03 — P1 / пробел: канал записи агента и legacy consumer compatibility

**Источники:** архитектура L568–572, L593, L690; план 0001 L196, 0042 L1969, 0048 L2232, 0050 L2318. Дополнительный read-only code check: [task_plan_lifecycle.py](../plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py) L228–291 — new/complete формируют Markdown и _write_validated пишет файл.

После cutover агент/CLI/Python должны писать через typed commands, raw SQL запрещён. Но не выбран transport агента к domain service (MCP, tool adapter или другой scoped route), не определены identity/capability token, idempotency/revision envelope для этих вызовов и список существующих writers, которые нужно адаптировать. Acceptance «current consumers используют adapter» есть, конкретной migration inventory и ownership plugin-path изменений нет. Текущий файловый writer подтверждает реальность интеграционной работы, а не доказывает дефект ещё не созданной Web системы.

**Закрытие:** составить producer/consumer inventory; выбрать один M1 command channel с проверяемым run identity и узкими actions; определить, какие legacy entrypoints отключаются/адаптируются при DB authority. Не давать агенту browser cookie или произвольный SQL. Preview/deny для unsupported writers и negative tests нужны до cutover. Owners 0001/0042/0048/0050, отдельные plugin-file scopes в плане; не предполагать, что папка apps/local-service/src/adapters автоматически покрывает Python callers.

### WA-04 — P1 / противоречие: workspace и project как граница событий и выполнения

**Источники:** архитектура L160–183 (workspace endpoints и sequence), L483/L500/L544/L558 (writer scope), L607–610 (workspace содержит проекты), L638 (UNIQUE(project,seq)); PRD L603.

API/SSE используют монотонную workspace sequence; SQL events имеют per-project seq. В одном workspace теперь несколько projects. Простое число cursor не объясняет replay двух проектов с одинаковым seq, а workspaceId не заменяет projectId при проверке task/session links. Дополнительно «один writer на workspace» и «один mutating run на проект» не эквивалентны в новой tenancy модели.

**Закрытие:** выбрать единый glossary: tenant/workspace/project/canonical repository root/runtime profile. Рекомендация: project event stream с cursor(project_id,sequence,generation), auth check project membership; physical writer lease по canonical root независимо от alias project. Если нужен workspace stream — отдельная глобальная sequence/merge contract. Зафиксировать envelope и lease scope, сценарии двух проектов/alias roots/expired cursors. Owners 0001/0003/0042/0048; до shared contracts.

### WA-05 — P1 / открытое решение: режим UX ещё не описывает исполняемую policy

**Источники:** PRD L566–568/L618; [wireframes](product-agent-os-web-m1-wireframes-2026-11-09.md) L154–162; архитектура L453/L484/L496; [официальный App Server](https://learn.chatgpt.com/docs/app-server), проверен 2026-11-10.

Discussion/Planning запрещают target writes, Execution меняет режим только для следующего run. Не задано точное mapping mode → sandbox/read roots/network/tools/approval settings для pinned build. Официальная документация указывает, что turn overrides могут стать defaults последующих turns; следовательно, возврат Execution→Discussion в том же thread нельзя реализовать только изменением label. Read-only filesystem также не определяет допустимость side effects внешних tools/MCP.

**Закрытие:** capability/policy matrix для каждого режима, обязательная повторная передача policy либо отдельные runtime profiles; запрет неподдержанного downgrade без доказанного ограничения. Tests: execution→discussion, resume с прежними defaults, network/MCP side effect, instruction, пытающаяся расширить scope. Отдельно различить планируемые файлы и технически enforceable write roots. Owners 0042/0043; до mutating runtime path. Отсутствие реализации само по себе не finding; finding — незаполненный конкретный контракт enforcement.

### WA-06 — P1 / открытое решение: local bootstrap и credential transport

**Источники:** архитектура L189–197/L550–552; [auth](product-agent-os-web-auth-commercial-2026-11-09.md) L60–68; план 0040 L1881 и 0041 L1925.

Правильные запреты уже перечислены, но bootstrap channel/cookie flags, Windows secure store и способ передать credential runtime без копий в tool environment остаются unresolved. Указание «один процесс/изолированный profile» не является доказательством изоляции. Без выбранного механизма нельзя проверить real-key path и launch без терминала воспроизводимо.

**Закрытие:** небольшой security ADR: bootstrap transport/lifetime, Host/Origin/CSRF/SSE auth, token storage/persistence, account isolation, runtime credential injection и redaction limits. Synthetic canary для env/args/logs/runtime files до настоящих secrets; explicit gate перед paid inference. Owners 0040/0041/0042 и security; до пилота с credentials. Не требовать commercial SIWC для локального API пути.

### WA-07 — P1 / открытое решение: pinned runtime и event-to-state mapping

**Источники:** архитектура L453/L484/L534–538; auth L79/L98; план 0042 L1969–2012. [App Server](https://learn.chatgpt.com/docs/app-server) checked 2026-11-10.

Build/schemaHash названы, но конкретный поддерживаемый build, его schema artifact, список request kinds и mapping к UI ACK/outcome не выбраны. В документации runtime generate schema зависит от версии; serverRequest/resolved означает answered или cleared, не обязательно Allow/успешное действие. Generic «ACK принят» без request-kind mapping может дать ложный success после cancel/cleanup. Это предупреждение к будущей реализации, не наблюдаемый runtime failure.

**Закрытие:** M1 protocol manifest с version/schema digest, supported requests/notifications, unknown event policy, decision-sent/request-resolved/action-outcome как разными состояниями. Recovery cases включают resolved by interruption и request without enough fields. Owners 0001/0042/0044; до protocol adapter. Нынешние capabilities pending допустимы для design draft, но не для contract-ready handoff.

### WA-08 — P1 / пробел решения: retention и доступность собственной истории

**Источники:** архитектура L498/L632/L642/L671/L712–714; auth L62–68/L98; PRD L646/L655–656/L688/L694.

История runtime authoritative, SQL cache может быть redacted/retained по ещё не выбранной policy. FTS ищет message projections, backup не включает runtime transcript автоматически. Поэтому ещё неизвестно, что пользователь потеряет/увидит после удаления runtime profile, retention expiry или восстановления только PAOS DB. Поле coverage объясняет пробел, но не задаёт минимальную гарантию сохранности собственных PAOS conversations. Проект явно признаёт retention pending — это незакрытое решение, а не сокрытая несогласованность.

**Закрытие:** data-class matrix (draft, final message, tool output, audit, checks, attachment, FTS, backup): owner, cache policy, default TTL/size, delete/export/restore outcome. Выбрать минимальную M1 history guarantee и предупреждение backup scope. Redaction диагностических логов не должна молча уничтожать пользовательский текст в основной истории. Owners 0043/0044/0049/0051; до persistence/search с пользовательскими данными.

### WA-09 — P2 / пробел трассировки: финальная карточка M1 не собирает весь новый DoD

**Источники:** план L19/L29; 0045 L2101–2144; 0048 L2232; wireframes L475–496; PRD L683–696.

Верхняя очередь уже требует ST-AC-01–07, но acceptance самой 0045 и её JSON по-прежнему только SW-AC-01–10. UX criteria ссылаются на 0008/0010/0012/0024/0029, находящиеся вне M1 closure. Нельзя утверждать, что storage/UX вообще отсутствуют в плане: они присутствуют, но не определён минимальный M1 owner/gate для каждой части. Аналогично 0048 обещает ST-09 с agent/skill UI, editors которого позже.

**Закрытие:** одна M1 acceptance matrix: requirement → минимальное поведение → owner task → fixture/browser/runtime evidence → blocking/deferred with reason. 0045 агрегирует SW + local ST + применимые UX; расширенные catalogs/editor/statistics явно M2/M3. Не добавлять в M1 все поздние задачи только ради совпадения ссылок. Owners product/tester, 0043/0045/0048; до M1 acceptance и до оценки scope.

### WA-10 — P2 / пробел UX: v0.6 storage flow отсутствует в актуальных wireframes

**Источники:** PRD L668–675; plan 0050/0051; [экраны](product-agent-os-web-task-manager-screens-2026-11-09.md) L5–24/L355–363; wireframes L437–451/L496. В текущих UX документах source direction v0.4/47 tasks; полнотекстовый поиск по migration/backup/restore проверен с отделением workflow migration от data migration.

Есть словесный путь переноса в PRD и future app paths в плане, но нет его screen/route ownership, mapping/conflict preview, backup destination/restore wizard, cutover progress/recovery и partial import receipt в screen catalog. Workflow migration S25/S26 решает другую задачу. S24 имеет retention, но не определяет backup/restore journey.

**Закрытие:** добавить layouts/states в S02/S24 либо отдельные routes с Back/cancel/resume/focus поведением; указать целевые страницы search, authority badge и external MD conflict. Обновить UX pointers до v0.6 без перерисовки всех прежних изображений. Owners product/frontend, 0049/0050/0051; до их UI implementation.

### WA-11 — P2 / неоднозначность degraded mode: отсутствие runtime блокирует только execution или весь CRUD

**Источники:** архитектура L542/L546; PRD L559/L643–647, ST-01 L683; auth L52.

При missing/incompatible Codex архитектура обещает локальный read-only режим. Новый storage contract обещает локальные создание задач, поиск и экспорт без provider connection. Missing runtime и missing provider — разные состояния, поэтому прямого логического опровержения здесь нет; не определена продуктовая матрица, должен ли task CRUD зависеть от установленного Codex. Для автономного Task Manager эта разница заметна пользователю.

**Закрытие:** capabilities matrix для no runtime / incompatible runtime / disconnected / no network / DB read-only / DB corrupt. Рекомендация: task CRUD/drafts/search/export доступны при здоровой local DB без runtime; только execution отключён. DB corruption — отдельный recovery state. Выбор владельца до acceptance 0040/0043/0045; не выдавать рекомендацию за уже принятое решение.

### WA-12 — P2 / открытые решения: воспроизводимая поставка и reference workload

**Источники:** PRD L213–220/L635/L702; архитектура §4 и L591/L595/L722; план 0040 и 0048, исторический packaging 0030.

Версии Node/Python/Codex, SQLite driver/native dependency, FTS5 availability, OS support matrix, app-data root, update compatibility и минимальный delivery package для первого запуска пока не зафиксированы. NFR latency targets существуют, но hardware/corpus/cache условия не выбраны; отсутствие измерений до реализации нормально, отсутствие тестового профиля делает future acceptance неоднозначной. Full installer можно оставить M4, но launcher M1 требует согласованного dev/pilot package.

**Закрытие:** M1a dependency/runtime manifest + Windows reference profile + fixture datasets/limits. Не надо сейчас выбирать все future team libraries. Владельцы architect/0040/0048/tester; версии до packaging code, workload до performance acceptance. Оценки остаются rough до этой проверки.

### WA-13 — P3 / документационный drift: актуальные фрагменты перемешаны с историческими

**Источники:** PRD L157–178/L610; архитектура L120–151/L405–425/L534; wireframes L496; plan L68–82. В PRD/архитектуре также есть повторяющиеся номера разделов 13/17/18.

Прежние FR/stage mappings явно переопределены поздними разделами, поэтому не все старые противоречия являются текущими требованиями. Однако диаграмма tasks→files/journal ещё выглядит общей, run enum starting/succeeded расходится с dispatching/completed без canonical mapping, UX оставляет 47 задач. Потребитель, прочитавший отдельный раздел, может получить устаревший contract.

**Закрытие:** один current-contract entry point и canonical enum mapping, старые диаграммы/таблицы явно historical; уникальные anchors/нумерация. Исторические receipts не переписывать. До parallel implementation handoff; owner docs/architect. Это не основание повторять прежний аудит с нуля.

## 4. Открытые решения по моменту закрытия

| Решение | Что необходимо выбрать | Владелец / момент | Связь |
| --- | --- | --- | --- |
| D-M1-01 | Minimal new-project/import profile и поля первого SQL schema | Product + architect, до 0002/0048/0050 | WA-01 |
| D-M1-02 | Agent command channel и legacy consumer inventory | Runtime + plugin owner, до 0042/0048/cutover | WA-03 |
| D-M1-03 | Project/workspace/root glossary, cursor и lease scope | Architect, до shared contracts | WA-04 |
| D-M1-04 | Fixed M1 recipe, mode policy matrix, allowed tool/network actions | Product/security/runtime, до execution | WA-05 |
| D-M1-05 | Runtime build/schema и ACK/outcome mapping | Runtime/tester, M1a contract phase | WA-07 |
| D-M1-06 | Bootstrap, secure store, credential transport | Security/runtime, до real credentials | WA-06 |
| D-M1-07 | Transcript/cache/FTS/backup retention и restore guarantee | Product/privacy/storage, до пользовательских данных | WA-08 |
| D-M1-08 | Backup-before-promote и reverse transfer scope | Storage/tester, до cutover | WA-02 |
| D-M1-09 | Local degraded-mode capabilities | Product, до UI acceptance | WA-11 |
| D-M1-10 | M1 acceptance matrix и reference workload | Product/tester, до final M1 gate | WA-09/12 |
| D-REL-01 | Paid local/OSS-first, exact API route и commercial qualification | Owner + release/legal, до соответствующего распространения | Auth AUTH-G1–G6 |
| D-T1-01 | Team hosting/RBAC/runtime placement/model | Отдельный будущий team scope | Не блокирует local M1 |

Commercial uncertainty не открыта впервые этим аудитом: она уже записана в auth contract L9–39/L81–98 и PAOS-0039/0046. [Официальная App Server auth page](https://learn.chatgpt.com/docs/app-server#auth-endpoints) содержит ограничение commercial/hosted authentication; считать API BYOK автоматически допустимым commercial route нельзя. [SIWC client ID](https://developers.openai.com/siwc/request-client-id) описывает отдельный admission. Аудит не даёт юридического заключения и не меняет выбранный runtime. Отличать личный технический prototype, пилот с чужими данными и платный выпуск; каждому нужен свой evidence/authority gate. SIWC, team vector search и полный workflow editor не становятся обязательными для local M1.

## 5. Проверка плана и реалистичность последовательности

Синтаксическая проверка: 53 unique tasks / 12 groups, все planned, actual timestamps/durations null. Closure dependencies PAOS-0045 содержит 15 задач: PAOS-0001–0004, PAOS-0039–0045, PAOS-0048–0051. Сумма текущих estimates — **202 engineering hours**, арифметика плановых значений, не календарная оценка, не измеренное время и не гарантированный бюджет. DAG cycle-free и обратные Blocks должны быть согласованы; конкретный результат текущего check в §8.

Эти 202 часа не учитывают автоматически весь дополнительный scope закрытия решений; import profile/runtime/security packaging могут изменить оценки. Отдельно подтверждённая проблема WA-02 не видна обычному DAG validator: он не знает, что cutover семантически требует backup/restore.

Рекомендуемая корректировка очереди для последующего согласования (не применена):

1. **Contract baseline:** WA-01/03/04/05/07, ownership и M1 field/capability/acceptance matrix. Остальные future product requirements сохранить с явными milestones.
2. **Local foundation:** reproducible runtime/package choices, bootstrap/credential design, SQLite transactions и fake-runtime contract checks; no production/user credentials до security gate.
3. **New-project vertical slice:** task → session → scoped run → decision → diff/checks → restart; одна seed recipe, минимальный M1 task workflow; late editors не требуются.
4. **Search и legacy preview:** выбранные source schemas, no-loss mapping, RU/EN corpus, history policy; unsupported projects остаются readable.
5. **Backup/restore primitive → cutover → post-cutover recovery:** порядок соответствует WA-02; миграция на реальном проекте только отдельно разрешённая.
6. **M1 acceptance:** единый SW/ST/UX ledger; actual runtime/browser evidence отдельно от fixture и документационных тестов. T1 и optional SIWC не входят в этот gate.

Критерии завершения будущей доработки документации: каждый P1 имеет принятое решение или явное сокращение/отложение scope владельцем; ссылки/карточки/JSON/UX согласованы; новые dependency edges не цикличны; M1 DoD однозначен; коммерческий допуск не подменён фактом сохранения документов. Сейчас эти критерии не закрыты аудитом.

## 6. Что не было объявлено дефектом

- Не выполненные runtime/browser/migration tests до разработки — ожидаемый pending evidence, не failing implementation.
- §20 явно заменяет file authority после cutover; старый §6 не доказывает наличие двух работающих masters.
- Есть explicit connection verification action в WF-16 (wireframes L448–451); deadlock «ready требует inference, Send требует ready» не подтверждён.
- Правила diff уже различают IDE changes, unknown authorship и actual/proposed (WF-07 L233–246); не заявляется отсутствие provenance contract.
- Нет оснований переносить T1/RBAC/pgvector/SIWC/editor gates в local M1 только из-за полноты продуктового каталога.
- Не найден циклический task DAG; semantic backup issue описан отдельно.

## 7. Источники и воспроизводимость

Ссылки и номера строк относятся к зафиксированным файлам этого запуска, до каких-либо изменений спецификаций. Полный source inventory с SHA256 ниже. Узкий code read legacy writer не является аудитом всего plugin/runtime.

Официальные источники перечитаны 2026-11-10: [App Server](https://learn.chatgpt.com/docs/app-server), [SIWC app-server integration](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server), [SIWC client ID](https://developers.openai.com/siwc/request-client-id). Использованы только релевантные protocol/auth ограничения; заявления прежних DB/GitHub исследований в этом аудите заново не сертифицируются. API/schema генерация не запускалась. Причина обращения к official docs: локальная targeted inventory не нашла Web pinned app-server schema artifact; source package не является реализацией нового Web adapter.

Review mode: explicit self_review, контекст предыдущего authoring сохранён; independent/fresh-context review не проводился. Проверены counterevidence и precedence, severity относится к будущему M1 contract. User/product acceptance не выдумывается.

| Source snapshot | SHA256 |
| --- | --- |
| `product-agent-os-web-prd-2026-11-05.md` | `381ccceb4ca5513a2780614c2b9d3c52348889e739287477d8aac720469f2d7c` |
| `product-agent-os-web-architecture-2026-11-05.md` | `17c109f2b57388ce7d66c9fd00fc31b23865554385b2e578bfcca485a10d3670` |
| `product-agent-os-web-task-manager-plan-2026-11-09.md` | `707911a75efbee0497dae04c9139480ccc35eefcb5645c1a5c0a27ae130e3469` |
| `product-agent-os-web-task-manager-task-group-2026-11-09.json` | `cab8920a747f68e6152426017a7c6555294f68e3981e6ab40b552b32050691fb` |
| `product-agent-os-web-auth-commercial-2026-11-09.md` | `d888d2189400aaadffeb027d4f649657237ec3af2fe5bbcf046e97ae74cbbcb2` |
| `product-agent-os-web-task-manager-screens-2026-11-09.md` | `ff005626b481f074345262dc770e69113aea8dabfaddab2c1d861eb86dd97a53` |
| `product-agent-os-web-m1-wireframes-2026-11-09.md` | `b4b0b245d7e92ac9129f4da109ee565c34b62089d0d151da19d652741c37c6f1` |

## 8. Текущие проверки, scope и завершение

| Проверка | Наблюдаемый результат текущего запуска |
| --- | --- |
| `git status --short` до правок | Exit 0, worktree clean |
| `git rev-parse HEAD` | Exit 0, cc9003e733f84c86a81633fafa37431f8c62e658 |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0, ok=true, errors=[] |
| Inline Node read-only plan audit | errors=[]; 53 unique tasks / 12 groups; DAG acyclic, MD Depends on/Blocks совпадают с JSON; all planned/actual null; M1 dependency closure 15 tasks, estimates sum 202 h |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0, 105 tests OK, 8.331 s; process-local TEMP/TMP=.docs-tools/reports/web-task-manager/test-temp |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| `git diff --check` | Exit 0; только CRLF normalization warnings |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-m1-final-audit/site` | Exit 1, Aborted with 10 warnings in strict mode: прежние G6/G7 links в coding-standards/control-plane-current-state/registries вне docs index. Собственные audit pointers используют source-path notation |
| Inline report/source check | errors=[]; 8 P1 / 4 P2 / 1 P3; 7 local Markdown links разрешаются; UTF-8 без replacement characters; SHA256 семи проверяемых документов unchanged |

Проверки формата не опровергают semantic findings. Strict site gate failed не является Web runtime failure и не закрыт этим аудитом. Render новой research страницы не подтверждается MkDocs: research вне docs_dir; browser не запускался. Исходные specs, task JSON, UX/auth, code/hooks и выбранные engines не изменены. Новая запись: этот отчёт; RUNLOG и registry RU/EN — только compact audit pointers; свой lifecycle marker — reporting metadata.

Control-plane sync: RUNLOG updated; REQUIREMENTS/PLAN/TEST/EVALS not_applicable для изменения scope/очереди/проверок/рубрик — аудит предлагает последующую доработку и не принимает её за владельца. Existing verification commands сохранены. prod_test not_applicable. Source registries RU/EN updated. Handoff_required: владельцы Web contracts разбирают WA-01–13; owners G6/G7 исправляют свои strict site links. Root compaction не нужна для этой короткой записи. Findings не являются accepted gaps.

Closure level: audit_complete / documentation_partially_verified. Review mode self_review; ранее созданные агентские проверки UX не выдаются за независимый review этого аудита. Runtime/product/owner acceptance остаются not_verified/pending. Следующий рекомендуемый scope — согласование решений и узкая корректировка PRD/architecture/plan/UX по WA, затем отдельное разрешение реализации. В этой задаче новая очередь не применялась и программирование не начиналось.

## 9. Устранение замечаний в документации — 2026-11-10

Task: PAOS-WEB-M1-CONTRACT-ALIGNMENT-2026-11-10. Sections 1–8 — неизменённый исторический аудит исходного snapshot v0.6; их hashes/line refs и receipts относятся к нему. Текущая baseline v0.7 заменяет статус M1_contract_changes_required для проектных решений, но не означает implementation/runtime acceptance.

| Finding | Конкретное решение / owning artifact | Статус и следующая проверка |
| --- | --- | --- |
| WA-01 | PRD §17.1–17.2: flat Task и строгий M1 import profile; full hierarchy/versions/attachments round-trip M2, significant unsupported data блокирует cutover | addressed_in_design; 0050/0056 fixtures |
| WA-02 | 0050 preview, 0051 independent backup/restore, новая 0056 после обоих и 0055/0044 | addressed_in_design; DAG/static + будущий crash test |
| WA-03 | Architecture §21.3: scoped dynamic tools→domain service; legacy consumer inventory/adapter gate в 0055 | addressed_in_design; experimental capability gate 0054 |
| WA-04 | §21.2: project stream/cursor/generation, system stream отдельно, canonical root lease/fencing, local concurrency=1 | addressed_in_design; alias/cross-project/restart tests |
| WA-05 | §21.4: explicit per-turn policy, no external tools; mode change → fresh runtime binding/context preview | addressed_in_design; negative runtime policy proof pending |
| WA-06 | Auth §7: launcher pairing POST, cookie/CSRF/Origin; Credential Manager + ephemeral stdio auth, no fallback | addressed_in_design; Windows/browser/secret canary gate |
| WA-07 | §21.5 и 0054: candidate versions, schema manifest, answered_or_cleared отдельно от item/turn outcomes | addressed_in_design; generated schema и real runtime pending |
| WA-08 | §21.6: durable visible messages/coverage, retention/purge/FTS и backup exclusions | addressed_in_design; restore/deletion checks pending |
| WA-09 | Plan v0.7 DoD: все SW/ST/UX M1 slices + DATA-AC и owners; 0045 acceptance обновлён | addressed_in_design; no M2 dependency for M1 minimum |
| WA-10 | UX §15: WF-17–21; S29 import, S30 backup/restore, S31 search; conflict flow | addressed_in_design; browser/owner UX acceptance pending |
| WA-11 | PRD §17.3: no-provider healthy SQL сохраняет CRUD; corrupt/disk-full/recovery отдельны | addressed_in_design; offline/negative checks pending |
| WA-12 | ADR-W10/§21.5/§21.8: exact candidate tuple, built-in driver/Worker, packaging, workload/targets; 0054 freezes validated manifest | addressed_in_design; no claim certified versions/performance |
| WA-13 | Current entrypoints v0.7, revised FR stages/run states/module diagram, unique PRD/architecture headings и явно исторические receipts | addressed_in_design; static consistency review |

Решения предложены и включены в спецификации в пределах поручения пользователя; ещё не приняты как доказанные runtime свойства. Выбранный experimental dynamic tools и release-candidate node:sqlite — осознанные риски compatibility gate. Если 0054 их не подтверждает, это явный re-entry в ADR, не молчаливый обход ограничений.

### 9.1. Что изменилось в плане

56 planned tasks / 12 groups. Новые 0054/0055/0056, 0050 только preview. Транзитивный M1 scope 18 задач, rough sum 234 h; actual timestamps/durations null. T1 действительно зависит от local M4 (0052→0030). Следующий шаг только после отдельного разрешения реализации: 0001/0054. Коммерческий выпуск сохраняет AUTH-G1–G6.

### 9.2. Текущие проверки согласования

| Проверка текущего согласования | Результат |
| --- | --- |
| Docs unittest: python -m unittest tests.product_agent_os.test_product_agent_os_docs -v; финальный повтор без -v | 105 tests OK; финальный запуск 9.975 s, exit 0. TEMP/TMP process-local .docs-tools/reports/web-task-manager/test-temp |
| python tools/check_docs.py | Exit 0, documentation structure checks passed |
| python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md | Exit 0, ok=true, errors=[] |
| Inline Node read-only consistency | 56 unique tasks / 12 groups; DAG acyclic; MD Depends on/Blocks/title/estimate совпадают с JSON; все planned и actual null; M1 18 tasks / rough 234 h |
| Inline source/text checks | 97 local file links разрешаются; UTF-8/fences без ошибок; 31 screen sections, 21 WF; numbered PRD/architecture headings unique; WA-01–13 mapping complete; root files ≤50 KiB |
| git diff --check | Первоначально найден extra blank line at plan EOF; исправлен, финальный exit 0. CRLF normalization warnings не выдаются за whitespace errors |
| .venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-m1-contract-alignment/site | Exit 1: Aborted with 10 warnings in strict mode. Прежние G6/G7 links в coding-standards, control-plane-current-state и registries; новые source pointers не добавили предупреждений |

Strict site gate не пройден и не waived. Research pages находятся вне docs_dir: build не доказывает их rendering, Mermaid и wireframes проверены только как source/структура. Новые изображения, browser/SQL/provider/runtime проверки не выполнялись.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG updated короткими pointers; registry RU/EN synced. EVALS not_applicable: рубрики AI/eval thresholds действующего продукта не менялись; новый workload — future Web acceptance в owning architecture. prod_test not_applicable: исторический production ledger не затрагивается. Overflow не требуется, roots ниже 50 KiB. Handoff_required: G6/G7 owners для существующих site links; Web 0054/0045 owners для будущих compatibility/runtime evidence после отдельного старта.

Self-review: context_mode=self_review, tester_verdict=partial_only из-за strict site failure и отсутствия runtime evidence. Проверены scope separation, DAG/MD-JSON parity, schema names, mode/approval semantics, retention, field/milestone mapping и evidence ceiling. В ходе самопроверки устранены workspace/project API naming, дублирование названий SQL entities, старые FR stages и прежние UX owners. Исходные audit observations/hashes §1–8 сохранены историческими; unrelated dirty work не отменялось.

Closure level: contract_alignment_complete / documentation_partially_verified. Все 13 замечаний получили проектное решение и проверяемый следующий gate; это не 13 пройденных runtime tests. Записаны только Markdown/planning JSON и собственные reporting metadata. Код приложения, DB/schema migrations, hooks и credentials не менялись; Git history/publication не выполнялись.
