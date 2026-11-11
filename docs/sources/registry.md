# Реестр источников

WEB-M1-APP-09 (2026-11-11): PAOS App-agent pull route без отдельного API key реализован; production UI → явно подключённый настоящий Codex App worker → durable result → browser проверены 16/16 в `.tmp/paos-m1/app-agent-evidence-9TDdwj/app-agent-result.json` (cleanup завершён). Ответ синтетический, worker выполнил reasoning roundtrip через capability-authenticated claim/report; это не App Server turn. Независимое source review подтвердило исправления queued Send ACK, очистки capability/lease secrets перед public write, сериализации selector и global foreign-run fence. [Official queue](https://learn.chatgpt.com/docs/developer-commands#codex-queue) и [App Server protocol](https://learn.chatgpt.com/docs/app-server#protocol) подтверждают наличие документированных интерфейсов, но native proxy/daemon probes здесь завершились `WSA10050`; Desktop-host activation не квалифицирован. Сохранены failed receipts `ZhBqrb` (binding disabled) и `dpIayh` (lease expiry). Worker report завершён exit 0; heartbeat helper позднее exit 1 после закрытия fixture, поэтому shutdown heartbeat не считается доказанным. Claim ceiling: явно attached active App agent, cooperative Stop; без auto-wakeup, native sandbox, Execution, closed-App или full M1/owner acceptance claims. Evidence/limits: `research/product-agent-os-web-m1-execution-2026-11-11.md` и source-owned execution results; исторический APP-08 сохранён.

WEB-M1-APP-08 (2026-11-11): владелец требует Codex App agents без отдельного API key; API-only setup отменён. [Auth](https://learn.chatgpt.com/docs/auth), [App Server auth](https://learn.chatgpt.com/docs/app-server#auth-endpoints), [SDK](https://learn.chatgpt.com/docs/codex-sdk) сверены свежими fetch. Subscription auth не равен existing-App-agent bridge; готового PAOS bridge в проверенном коде не найдено. Evidence/limits: research/product-agent-os-web-m1-execution-2026-11-11.md. Runtime code/credentials не менялись.

WEB-M1-ACTIVE-07 (2026-11-11): current activefixture55/Web213/browser669/headless33;9 runtime/UI/recovery defects repaired. Source-owned research/product-agent-os-web-m1-execution-2026-11-11.md and results retain source hashes/failed receipts/remaining gates. [Official approvals](https://learn.chatgpt.com/docs/app-server#approvals) + pinned0.167 schemas; Context7 main snippets secondary. No actual Codex/provider turn or full0045 acceptance.

WEB-M1-AUTO-06 (2026-11-11): source-owned SESSION_REQUIRED reproduction/fix, browser669, autonomous launcher56, Web197. Источник: research/product-agent-os-web-m1-execution-2026-11-11.md и execution-results. PAOS-0040 technical implemented по составным native/browser receipts; manual owner rejection сохранён. Standing authorization canonical AGENTS.md, managed controls неизменны; full M1/provider acceptance не заявлена.

WEB-M1-UI-05 (2026-11-11): PAOS-0004 browser667 passed, native zoom200% measured; scope limited to synthetic UI, no full WCAG/provider acceptance. [W3C resize](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html), [contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [Chromium zoom](https://raw.githubusercontent.com/chromium/chromium/main/chrome/browser/ui/zoom/chrome_zoom_level_prefs.cc). Evidence: research/product-agent-os-web-m1-execution-2026-11-11.md and results JSON. PAOS-0040 external receipt remains open.

WEB-M1-FIVE-04 (2026-11-11): offline repair пяти открытых M1 задач; Web192/192, build35, native headless33. Pending draft/Send ACK, post-await dispatch/approval, EOF reconnect/generation, shutdown drain и time journal admission проверены локально. Источник: research/product-agent-os-web-m1-execution-2026-11-11.md и execution-results continuation. [Node26.5 child lifecycle](https://nodejs.org/download/release/v26.5.0/docs/api/child_process.html#subprocesskillsignal), [OpenAI App Server events](https://learn.chatgpt.com/docs/app-server#events); Context7 official repository snippets — secondary context. Browser/provider/native-window gates не сняты, five tasks in_progress.

WEB-M1-ISOLATION-03 (2026-11-11): project-local main/profile identity wiring теперь изолирует credential namespace по canonical path + directory identity, без доступа к legacy/default targets; Quit ждёт HTTP drain перед SQLite close. Web166/166 и native headless33 passed, browser/provider/owner gates открыты. Источник: research/product-agent-os-web-m1-execution-2026-11-11.md и execution-results continuation; API/source claims AUTH-02 не менялись.

WEB-M1-AUTH-02 (2026-11-11, 08:46 MSK): после отдельной owner authority native Credential Manager fixture write/read/delete passed, отсутствие после cleanup подтверждено; второй isolated stdio canary квалифицировал actual local broker/account.type apiKey без inference, modelAccess unverified. PAOS-0041 implemented в local-auth scope; M1 12/5/1, PAOS-0045 blocked. Evidence: `research/product-agent-os-web-m1-execution-2026-11-11.md`, execution-results JSON, два synthetic runners под `tests/web/single-window/`. Источники: [CredWriteW](https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credwritew), [CredReadW](https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credreadw), [CredDeleteW](https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-creddeletew), [App Server auth](https://learn.chatgpt.com/docs/app-server#auth-endpoints), [pinned discovery guard](https://raw.githubusercontent.com/openai/codex/rust-v0.167.0/codex-rs/models-manager/src/manager.rs). Network zero не измерялся: verified loopback/discovery-off gates и pinned source дают ожидание отсутствия requests. Production OpenAI-selector activation, provider entitlement и browser acceptance не подтверждены. Отказ WEB-M1-EXEC-01 ниже относится к исходному срезу до нового разрешения.

WEB-M1-EXEC-01 (2026-11-11): реализация локального Web M1, native MXC ready и фактическая запись/отказ на синтетических контролях. Evidence: `research/product-agent-os-web-m1-execution-2026-11-11.md` и соседний execution-results JSON; historical QUAL-01 ниже относится к 10 ноября. Источники: [официальный Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox#mxc-compatibility), [pinned Codex availability](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/mxc-sandbox/src/availability.rs#L17-L50), [Microsoft MXC](https://learn.microsoft.com/en-us/windows/apps/develop/mxc/quickstart), [App Server auth](https://learn.chatgpt.com/docs/app-server#auth-endpoints), [FTS5 rank](https://www.sqlite.org/fts5.html#sorting_by_auxiliary_function_results). AUTH-G1–G6 блокируют commercial distribution; local engineering preview использует local_api_byok. Native-offline/headless/SQLite evidence не закрывает browser/provider/owner acceptance PAOS-0045. Native Credential Manager synthetic roundtrip отклонён automatic approval review; операция не выполнена.

PAOS-AUD-G9: [единое формирование](../product-agent-os/project-formation.md), versioned local planner, explicit full-catalog compatibility, canonical owners, dependency closure и существующий merge/rollback. Evidence: `research/product-agent-os-g9-execution-report.md`, `docs/superpowers/specs/paos-aud-g9-project-formation-results.json`; synthetic local, initial T10 accepted; T17 owner accepted with model-behavior limits; G9 closed. G8-T14 и закрытие G8 явно приняты владельцем; fresh-session activation отдельно.

G8 scope clarification (10.11.2026): подробные матрицы docs/planning/ сохраняются целиком, default 40k size trigger к ним не применяется. Audit matrix в research/ по решению владельца остаётся целой; split preview не разрешён к применению. T14 принят владельцем; G8 закрыта. Контракт: [technical](../product-agent-os/technical.md); evidence: research/product-agent-os-g8-execution-report.md.


PAOS-AUD-G8 (2026-11-10): локальные document contracts, scoped staging, сохранение managed content, UTF-8 byte budget, reviewed lossless compaction/recovery и provenance документов. Источник: [технический контракт](../product-agent-os/technical.md); repository evidence `research/product-agent-os-g8-execution-report.md` и `docs/superpowers/specs/paos-aud-g8-control-plane-results.json`. Synthetic local verification; owner accepted G8; fresh-session activation и интеграция адаптера M1 отдельно. Исторические результаты G6/G7 сохранены; ссылки вне docs_dir обозначены путями repository artifacts.


WEB-CP-01 (2026-11-10): control-plane подготовлен под Web M1, scope v0.7 / execution v0.8. Устаревшие Web/lifecycle receipts и прошлый handoff сохранены с source hashes в research/product-agent-os-control-plane-maintenance-2026-11-10.md. Project-authored маршрутизация и сохранение истории; без реализации, runtime и изменений внешних source claims.

WEB-ORDER-08 (2026-11-10): пользователь утвердил последовательность всех 56 задач в research/product-agent-os-web-task-manager-plan-2026-11-09.md и task-group JSON, execution_plan.revision=0.8; PRD scope остаётся v0.7. PAOS-0046 после M1, PAOS-0036 в M2, PAOS-0002 только M1 profile. Project-authored planning metadata; внешние source claims и runtime evidence не изменены.

## Web M1 v0.7 — решения после аудита, 2026-11-10

WEB-M1-QUAL-01: локальный evidence PAOS-0001/0054 в `research/product-agent-os-web-m1-initial-qualification-2026-11-10.md`. Способ генерации схемы сверён с [App Server](https://learn.chatgpt.com/docs/app-server#message-schema), фильтры с [Thread listing](https://learn.chatgpt.com/docs/app-server#list-threads-with-pagination--filters), `ephemeral` с [Credential storage](https://learn.chatgpt.com/docs/auth#credential-storage). Второй изолированный прогон подтвердил persisted history по [синтетическому формату тестов CLI 0.167.0](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/app-server/tests/common/rollout.rs). Именованный профиль подтверждён в metadata. Native Windows readiness и Execution не квалифицированы.

WEB-M1-QUAL-02 — 2026-11-10, `research/product-agent-os-web-m1-initial-qualification-2026-11-10.md`. Статус `ready` наблюдался при выборе MXC и `unelevated`. В текущем контексте MXC сообщил `availability: false`, запуск дочерней команды не подтверждён. Проверка `unelevated` ограничена readiness из-за возможного изменения DACL системного устройства. Файловый enforcement не квалифицирован. [OpenAI Docs — MXC compatibility](https://learn.chatgpt.com/docs/windows/windows-sandbox#mxc-compatibility), [Codex 0.167.0 — readiness](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/app-server/src/request_processors/windows_sandbox_processor.rs#L306), [подготовка команды](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/windows-sandbox-rs/src/spawn_prep.rs#L250), [DACL NUL](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/windows-sandbox-rs/src/acl.rs#L1061)

WEB-M1-QUAL-03 — 2026-11-10, `research/product-agent-os-web-m1-initial-qualification-2026-11-10.md`. PSEC probe сводит ошибку в boolean, локально наблюдался restricted AppContainer token. Связь с точной причиной сбоя остаётся открытой. Файловый SQLite fixture проверил rollback, snapshot и FK. [Codex 0.167.0 — PSEC probe](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/mxc-sandbox/src/availability.rs#L17-L50), [Microsoft Learn — Windows token](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class), [SQLite — VACUUM INTO](https://sqlite.org/lang_vacuum.html#vacuuminto)

WEB-M1-ALIGN-07: PRD §17, architecture §21, plan/JSON и UX v0.7; 56 planned tasks / 12 groups, 31 routes / 21 wireframes. Audit §9 содержит WA-01–13 → design decisions → future gates. Источники: [App Server](https://learn.chatgpt.com/docs/app-server) (schema, experimental dynamic tools, request resolved не равно action success), [config reference](https://learn.chatgpt.com/docs/config-file/config-reference) (ephemeral credential store), [Node 26.5 SQLite](https://nodejs.org/download/release/v26.5.0/docs/api/sqlite.html) (DatabaseSync/backup, release candidate), проверены 2026-11-10. Scope/thresholds/auth UX — project-authored proposals, не runtime/commercial proof. Source path: research/product-agent-os-web-m1-final-audit-2026-11-10.md, §9.

## Web M1 final audit — 2026-11-10

Source audit `research/product-agent-os-web-m1-final-audit-2026-11-10.md`: 13 contract findings, source lines/SHA256, unchanged specifications; no implementation or runtime proof. [App Server](https://learn.chatgpt.com/docs/app-server) checked 2026-11-10: version-specific schemas, turn policy defaults, request resolution versus action outcome; [SIWC client ID](https://developers.openai.com/siwc/request-client-id): admission remains separate. Existing AUTH claims retain their evidence ceiling.

## Web storage contract v0.6 — 2026-11-09

Выбор пользователя: SQLite + FTS5 local; PostgreSQL + pgvector team. PRD §16 / architecture §20 и G12 плана — schema/migration proposal, не реализация. Owning artifacts: `research/product-agent-os-web-prd-2026-11-05.md`, `research/product-agent-os-web-architecture-2026-11-05.md`, `research/product-agent-os-web-task-manager-plan-2026-11-09.md`.

| ID | Source | Claim scope | Checked | Status |
| --- | --- | --- | --- | --- |
| WEB-DB-08 | [SQLite FK](https://sqlite.org/foreignkeys.html) | Per-connection foreign-key enforcement | 2026-11-09 | official / documentation_checked; implementation_not_started |
| WEB-DB-09 | [PostgreSQL RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) | Opt-in row policies and owner/bypass boundary | 2026-11-09 | official / documentation_checked; implementation_not_started |

WEB-DB-02/03 FTS5/pgvector rechecked in this authoring run; earlier WAL/backup research retained with its provenance.

## Web storage research — 2026-11-09

Исследовательский отчёт: `research/product-agent-os-web-storage-research-2026-11-09.md`. Предлагаемая архитектура; официальные docs и пять GitHub аналогов, pinned файлы в §6. Без DB benchmark/реализации.

| ID | Source | Claim scope | Checked | Status |
| --- | --- | --- | --- | --- |
| WEB-DB-01 | [WEB-DB-01](https://sqlite.org/wal.html) | SQLite WAL, concurrency and runtime version caveat | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |
| WEB-DB-02 | [WEB-DB-02](https://sqlite.org/fts5.html) | Lexical baseline and BM25 | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |
| WEB-DB-03 | [WEB-DB-03](https://github.com/pgvector/pgvector) | PostgreSQL vector extension and filtered ANN | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |
| WEB-DB-04 | [WEB-DB-04](https://docs.lancedb.com/basics/guarantees) | LanceDB table transaction boundary | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |
| WEB-DB-05 | [WEB-DB-05](https://docs.lancedb.com/search/hybrid-search) | Embedded hybrid retrieval | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |
| WEB-DB-06 | [WEB-DB-06](https://qdrant.tech/documentation/edge/edge-vs-qdrant-cluster/) | Qdrant Server versus Edge | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |
| WEB-DB-07 | [WEB-DB-07](https://pglite.dev/docs/pglite-socket) | PGlite single-connection boundary | 2026-11-09 | official / documentation_checked; PAOS runtime not_verified |

## Web session UX v0.5 — 2026-11-09

| ID | Source | Scope | Checked | Status |
| --- | --- | --- | --- | --- |
| WEB-UX-05 | `research/product-agent-os-web-m1-wireframes-2026-11-09.md`, `research/product-agent-os-web-task-manager-screens-2026-11-09.md` | 28 маршрутов, 16 wireframes, 18 proposed критериев; чат, задачи, агенты, diff, permissions и recovery | 2026-11-09 | project-authored / draft_for_review; render and runtime not_verified |

## Web single-window v0.4 — 2026-11-09

Выбран собственный клиент Codex App Server; owning artifacts: `research/product-agent-os-web-prd-2026-11-05.md`, `research/product-agent-os-web-architecture-2026-11-05.md`, `research/product-agent-os-web-auth-commercial-2026-11-09.md`, `research/product-agent-os-web-task-manager-plan-2026-11-09.md`. 47 planned tasks / 11 групп; SW-01–12, 28 текстовых routes. Runtime/commercial admission не подтверждены; прежние entries/receipts исторические.

| ID | Source | Claim boundary | Checked | Status |
| --- | --- | --- | --- | --- |
| WEB-AUTH-01 | [WEB-AUTH-01](https://learn.chatgpt.com/docs/app-server#auth-endpoints) | App Server auth и commercial/hosted restriction; не доказательство допуска PAOS | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-02 | [WEB-AUTH-02](https://developers.openai.com/siwc/request-client-id) | Commercial SIWC: selected partners/waitlist | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-03 | [WEB-AUTH-03](https://developers.openai.com/siwc/token-sharing-open-source) | Plan usage отдельно от identity; paid/remote требует отдельного рассмотрения; ChatGPT history не предоставляется | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-04 | [WEB-AUTH-04](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server) | SIWC provider, client-owned renewal/restart/resume; model catalog не entitlement | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-05 | [WEB-AUTH-05](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations) | Ограничения SIWC route, local history и tool/input boundaries | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-06 | [WEB-AUTH-06](https://developers.openai.com/siwc/website) | PKCE/OIDC identity flow и собственная app session; не plan usage permission | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-07 | [WEB-AUTH-07](https://openai.com/policies/services-agreement/) | API Customer Applications и запрет передачи ключей/обхода ограничений; exact deployment review pending | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-08 | [WEB-AUTH-08](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform) | Раздельный billing ChatGPT/API | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |
| WEB-AUTH-09 | [WEB-AUTH-09](https://github.com/openai/codex/blob/main/LICENSE) | Apache-2.0 для Codex source; проверка exact distributed build отдельно | 2026-11-09 | official / documentation_checked; runtime and admission not_verified |

Продуктовые решения и ограничения хранятся в auth/commercial документе. Источники не разрешают скрытое наследование login или использование платной подписки без подходящего consent/admission.

## PAOS-AUD-G7 — implementation evidence, 2026-11-09

T08: владелец принял T07; локальные механизмы рекомендованы keep, superiority insufficient_evidence. Итоговое решение (`research/product-agent-os-g7-execution-report-2026-11-09.md`); T06/final T08 accepted 10.11.2026; G7 closed locally, activation отдельно.

T07 10.11.2026: attested results (`docs/superpowers/specs/paos-aud-g7-attested-results.json`), 12 eligible generations, 6/6 на arm; tools=[] и same normalized common context. Superiority insufficient_evidence, no OS/E2E/activation claim. [Official normalization precedent](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/core/tests/suite/responses_lite.rs#L136) и [CLI override parsing](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/config/src/overrides.rs) проверены 10.11.2026; source_inspected и local actual trace evidence разделены. T06 actual Python/JS tool checks 10/10 отражены в execution report; owner acceptance отдельно.

### Historical research intake

Углубление 09.11.2026: source review и traceability (`research/product-agent-os-g7-repository-deep-review-2026-11-09.md`) закрепляет пять repository revisions, прочитанные implementation/test slices и четыре tool-doc источника. Findings P/K/M/S/D/X внесены в восемь planned G7 карточек; adopt/adapt/reject разделены. Статус community: source_inspected_runtime_not_reproduced; primary tool docs проверены, installed compatibility не проверялась.

Матрица G7 (`research/product-agent-os-audit-remediation-task-plan-2026-11-09.md`) содержит G7-S0/S1–S6/S8: Ponytail (commit `96608e0`), Karpathy-inspired guidelines, Matt Pocock skills, Superpowers, Desloppify и primary docs Ruff/Import Linter/dependency-cruiser/Stryker. Источники прочитаны в предшествующем анализе; текущий authoring не повторяет runtime benchmarks. Community: `trust_level=community`, `verification_status=source_inspected_runtime_not_reproduced`; tool docs: `trust_level=primary`, local compatibility unverified. Это planned hypotheses, не новые доказанные product claims; никакие плагины или инструменты не установлены.

## Web issue workflows v0.3 — 2026-11-09

Jira Cloud reference model для Web v0.3; project-authored adaptation в `research/product-agent-os-web-prd-2026-11-05.md`, §14. Числовые лимиты и agent execution — PAOS proposals.

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| WEB-JIRA-01 | [Hierarchy](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/) | Epic → standard (Story/Task/Bug) → Subtask. В новых документах Jira используются work item/work type. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-02 | [Status categories](https://support.atlassian.com/jira-cloud-administration/docs/what-is-a-workflow-status/) | Каждый status относится к To do, In progress или Done. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-03 | [Transitions](https://support.atlassian.com/jira-cloud-administration/docs/create-workflow-transitions/) | Переход направленный; обратный переход задаётся отдельно. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-04 | [Kanban mapping](https://support.atlassian.com/jira-software-cloud/docs/configure-columns/) | Колонки доски сопоставляются статусам; колонка может содержать несколько статусов. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-05 | [Workflow schemes](https://support.atlassian.com/jira-cloud-administration/docs/add-edit-and-delete-an-issue-workflow-scheme/) | Workflow schemes сопоставляют типы работ workflow; изменения активной схемы требуют публикации draft и при необходимости mapping статусов. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-06 | [Versions](https://support.atlassian.com/jira-cloud-administration/docs/manage-versions/) | Affects versions описывает затронутые версии; Fix versions связывает работу с выпуском. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-07 | [Components](https://support.atlassian.com/jira-software-cloud/docs/what-are-jira-components/) | Jira components группируют работу и ограничены company-managed spaces. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-08 | [Creator](https://support.atlassian.com/jira-software-cloud/docs/jql-fields/) | Creator фиксирует пользователя, создавшего запись, и не меняется. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-09 | [Linked work items](https://support.atlassian.com/jira-cloud-administration/docs/configure-issue-linking/) | Тип связи имеет имя и прямое/обратное описание; создание связи требует права. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-10 | [Comments and history](https://support.atlassian.com/jira-software-cloud/docs/what-are-the-different-types-of-activity-on-an-issue/) | Activity разделяет Comments, History и Work log. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-11 | [Attachments](https://support.atlassian.com/jira-software-cloud/docs/add-an-attachment-to-an-issue/) | Файл можно добавить upload/drag-and-drop; действуют ограничения вложений. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-12 | [Priority and resolution](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-statuses-priorities-and-resolutions/) | Priority отличается от Resolution; стандартные priorities Highest–Lowest. | 2026-11-09 | official / documentation_checked; PAOS design proposed |
| WEB-JIRA-13 | [Scheduling](https://support.atlassian.com/jira-software-cloud/docs/schedule-issues-in-advanced-roadmaps-using-start-end-dates/) | Start date/Due date используются для планирования; рассмотренная страница Plans относится к Premium/Enterprise. | 2026-11-09 | official / documentation_checked; PAOS design proposed |

## PAOS-AUD-G6 — project-local evidence, 2026-11-09

G6 partially_verified: три синтетических пилота выполнены из текущего проекта в host-target/pilots; все проверки passed, результаты needs_user_acceptance. По разрешению владельца HOST-01 больше не блокирует эти пилоты. Fresh-session activation HOST-01/HOST-02 остаётся отдельной открытой задачей; T34 no-go. Owner feedback/acceptance null; manual_only сохраняется. Pilot results (`docs/superpowers/specs/paos-aud-g6-pilot-results.json`).

## PAOS-AUD-G5 — project-local contracts, 2026-11-09

F13: offline installer command contract; F14: explicit skill invocation и ordinary intake; F17: RU/EN semantic parity, local strict build, routes/links/anchors и source-bound Mermaid rendering. Источники: `tools/docs_install.ps1`, `tests/product_agent_os/test_product_agent_os_docs.py`, package README и audit remediation task plan (09.11.2026). Evidence относится к local source/build; dependency installation, publication и host acceptance не выполняются.

## PAOS-AUD-G4 — project-local contracts

Project-local G4 contracts: inline/legacy intake, canonical skill disclosure/authority и измеренное reuse inventory. Источники: task_routing.py, discovery.py, canonical skills/references и audit remediation task plan (09.11.2026). Local checks не доказывают host activation или live behavioral quality.

## PAOS-AUD-G3 — 2026-11-09

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| AUD-G3-F03 | `source_policy.py`, `tests/product_agent_os/test_source_policy.py` | RU/EN calendar markers, local registry resolution, lexical claim classes; no semantic verification | 2026-11-09 | project-local contract |
| AUD-G3-F08 | `self_learning_feedback.py`, self-learning tests | Zero human labels: insufficient_evidence; validity, coverage and sentiment separate | 2026-11-09 | project-local contract; manual_only |
| AUD-G3-F16 | `status_snapshot.py`, `PLAN.md` current pointer, owning source revisions | Newer execution evidence precedence; task/run/verification/acceptance separate; unknown/conflict explicit | 2026-11-09 | generated orientation only; owning audit plan contains run evidence |

## PAOS-AUD-G2 — 2026-11-09

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| AUD-G2-S01 | [Build plugins](https://developers.openai.com/plugins/build/plugins), [submission](https://developers.openai.com/plugins/deploy/submission) | Codex compatibility wrapper, portable precedence; publisher/listing distribution gate | 2026-11-09 | official / documentation_checked |
| AUD-G2-S02 | [Plugins](https://learn.chatgpt.com/docs/plugins#use-plugins-from-a-supported-surface), [Skills](https://learn.chatgpt.com/docs/build-skills) | Native plugin unsupported in IDE; standalone skills documented | 2026-11-09 | official / documentation_checked; no host activation |
| AUD-G2-S03 | [Models](https://learn.chatgpt.com/docs/models) | GPT-6.1 Terra CLI minimum 0.159.0; no App/account inference | 2026-11-09 | official / documentation_checked |
| AUD-G2-S04 | `research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` | Local compatibility/diagnostic evidence; bounded component provenance | 2026-11-09 | project-local; see owning receipt |

## Web Task Manager: документационный scope — 2026-11-09

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| WEB-TM-01 | `research/product-agent-os-web-prd-2026-11-05.md`, `research/product-agent-os-web-architecture-2026-11-05.md` | Требования пользователя: вкладки, CRUD agents/skills, сессии, graph, task fields, time, RU/EN/themes, автономность | 2026-11-09 | project-authored / proposed |
| WEB-TM-02 | `research/product-agent-os-web-task-manager-plan-2026-11-09.md`, `research/product-agent-os-web-task-manager-screens-2026-11-09.md` | 30 planned tasks, 8 групп, 24 экранных концепта; не runtime evidence | 2026-11-09 | draft_for_review / needs_user_acceptance |

Source status: `project-authored`

## Исправления PAOS-AUD-G1 — 2026-11-09

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| AUD-G1-S01 | [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules) | Prefix decisions; match/not_match assertions | 2026-11-09 | official / documentation_checked |
| AUD-G1-S02 | [Hooks](https://learn.chatgpt.com/docs/hooks) | Project discovery path and trust boundary | 2026-11-09 | official / documentation_checked |
| AUD-G1-S03 | `research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` | Локальные contracts и evidence; host acceptance отдельно | 2026-11-09 | project-local; see owning receipt |
| AUD-G1-S04 | [Microsoft icacls](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls) | Selected SID removal; DACL save/restore; local icacls /? corroboration | 2026-11-09 | official / documentation_checked; real ACL mutation not exercised |

## Session lifecycle isolation — 09.11.2026

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| LCS-S01 | [Hooks: common input fields](https://learn.chatgpt.com/docs/hooks#common-input-fields) | Top-level session_id; subagents используют parent session ID | 2026-11-09 | official / documentation_checked |
| LCS-S02 | `research/product-agent-os-session-lifecycle-fix-2026-11-09.md` | Local selector, bootstrap, tests и границы host evidence | 2026-11-09 | local implementation; verification receipt принадлежит отчёту |

## Product-Agent OS Web — проектирование 05.11.2026

Scope: документационные предложения, без разработки или runtime activation. Стек и ICP — гипотезы для review.

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| WEB-S01 | `research/sol-0.6-product-agent-os-web-analysis-2026-11-05.md` | Локальный стек, реализованные модули, ограничения и reuse hypotheses | 2026-11-05 | local audit / source-backed; прежние checks не перезапускались |
| WEB-S02 | `research/product-agent-os-web-architecture-2026-11-05.md` | Owning PAOS sources: snapshot, cockpit, routing, question ledger, merge, contract runner | 2026-11-05 | local source inspected; не Web implementation |
| WEB-S03 | [Codex App Server](https://learn.chatgpt.com/docs/app-server) | Rich client integration, events, approvals; proposed stdio adapter | 2026-11-05 | official / documentation_checked; local compatibility not_verified |
| WEB-S04 | `research/product-agent-os-web-prd-2026-11-05.md`, `research/product-agent-os-web-architecture-2026-11-05.md` | Экраны, сценарии, requirements, proposed stack и этапы A0–A6 | 2026-11-05 | project-authored / draft_for_review; implementation not_started |

## Локальные GAP-01–GAP-05 — 05.11.2026

Локальная реализация; host activation и semantic source support не доказаны. Evidence owner: `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`.

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| GAP-S01 | [Build plugins](https://developers.openai.com/plugins/build/plugins) | Portable/compatibility precedence, OpenAI settings overlay, MCP wrapper | 2026-11-05 | official / documentation_checked |
| GAP-S02 | [Manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) | Agent Plugins 1.0.0 supported structural subset; not full schema/host validation | 2026-11-05 | primary specification / documentation_checked |
| GAP-S03 | [Skill metadata](https://learn.chatgpt.com/docs/build-skills#optional-metadata) | policy.allow_implicit_invocation; explicit-only differs from loading/invocation | 2026-11-05 | official / documentation_checked |
| GAP-S04 | `plugin_components.py`, `validators.py`, B42 matrix | Local inventory/provenance, 12/12 skills, 11 normalized mismatches; four metadata placement errors corrected after owner approval, 12/12 source metadata valid | 2026-11-05 | project-authored / local evidence |
| GAP-S05 | `source_policy.py`, `test_source_policy.py` | Exact HTTPS hostname; source_present separate from claim_supported and freshness | 2026-11-05 | project-authored / heuristic only |
| GAP-S06 | Active/package `pre_tool_use_policy.py`, `test_lifecycle_hooks.py` | Pinned exact report grant, task transition and fail-closed negative cases | 2026-11-05 | project-authored / local; fresh host not_verified |

Source-policy принимает exact HTTPS hosts `developers.openai.com`, `platform.openai.com`, `learn.chatgpt.com`, `help.openai.com`, `openai.com` и GitHub organization `openai`. Заголовок Sources, lookalike/userinfo/query URL не подтверждает источник. `source_present` не означает `claim_supported`: semantic support остаётся `not_verified`. Дата старше 90 дней, future/invalid date требуют review; 90 дней — локальная эвристика, не стандарт OpenAI. Следующий шаг — открыть источник и проверить конкретный claim.

## Локальная интеграция ORD-01–ORD-06 — 05.11.2026

| ID | Source | Claim scope | Status |
| --- | --- | --- | --- |
| ORD-S01 | `plugins/product-agent-os/scripts/product_agent_os/task_routing.py`, `scripts/codex_runtime_runner/cli.py`, `state.py`, `routes.py` | Opt-in task context, готовые selectors T26/T27, state provenance, legacy trace, read-only result | project-authored / local integration; без host activation claim |
| ORD-S02 | `plugins/product-agent-os/scripts/product_agent_os/templates.py`, `infrastructure.py`; `tests/product_agent_os/test_infrastructure_renderer.py` | Выбор templates, сохранение staging/merge boundary и user files | project-authored / synthetic local checks |
| ORD-S03 | `tests/product_agent_os/test_codex_runtime_runner_cli.py`; active/package compact contract | Public CLI, RU/EN decisions, high-risk/negative cases, regression RED/GREEN и stale receipts | project-authored / bounded local evidence; не behavioral promotion |

Evidence и финальные команды принадлежат `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`. T23–T29 и historical receipts сохранены; T30–T34 вне этого slice.

## Обновление пользовательского сайта — 05.11.2026

Источники проверены через OpenAI documentation connector для аудита и этого docs slice. Проверка относится к перечисленным claims, не ко всему API, account availability или runtime activation. Воспроизводимые local checks принадлежат текущему evidence receipt; исторические записи ниже сохраняют свои даты.

| ID | Source | Claim scope | checked_at | Status |
| --- | --- | --- | --- | --- |
| SITE-S01 | [Model Context Protocol](https://learn.chatgpt.com/docs/extend/mcp) | local/cloud MCP and orchestration | 2026-11-05 | official / documentation_checked |
| SITE-S02 | [Hooks](https://learn.chatgpt.com/docs/hooks) | trust, merge, concurrency, supported handlers and failure boundaries | 2026-11-05 | official / documentation_checked |
| SITE-S03 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | delegation and inherited controls | 2026-11-05 | official / documentation_checked |
| SITE-S04 | [Approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) | retired approval policy and execution scope | 2026-11-05 | official / documentation_checked |
| SITE-S05 | [Package your plugin](https://developers.openai.com/plugins/build/plugins) | portable and compatibility layouts | 2026-11-05 | official / documentation_checked |
| SITE-S06 | [Developer settings](https://learn.chatgpt.com/docs/developer-settings) | effective configuration diagnostics | 2026-11-05 | official / documentation_checked |
| SITE-S07 | [Scheduled tasks](https://developers.openai.com/codex/app/automations) | modes and execution prerequisites | 2026-11-05 | official / documentation_checked |
| SITE-S08 | [Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) | Git isolation and Handoff | 2026-11-05 | official / documentation_checked |
| SITE-S09 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | instructions-first and exposure | 2026-11-05 | official / documentation_checked |
| SITE-S10 | [Models](https://learn.chatgpt.com/docs/models) | client availability and model controls | 2026-11-05 | official / documentation_checked |
| SITE-S11 | [Latest model](https://developers.openai.com/api/docs/guides/latest-model) | initiative, scoped verification and migration | 2026-11-05 | official / documentation_checked |
| SITE-S12 | [Agents](https://developers.openai.com/api/docs/guides/agents) | runtime and state ownership | 2026-11-05 | official / documentation_checked |
| SITE-S13 | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | discovery versus supporting docs | 2026-11-05 | official / documentation_checked |
| SITE-S14 | [Memories](https://developers.openai.com/codex/memories) | local/web stores, use/generate and reset | 2026-11-05 | official / documentation_checked |
| SITE-S15 | [Deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist) | reference only; no deployment claim | 2026-11-05 | official / documentation_checked |
| SITE-S16 | [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | single-agent baseline and evaluation | 2026-11-05 | official / documentation_checked |
| SITE-S17 | [Plugins](https://learn.chatgpt.com/docs/plugins) | component/client support and installation | 2026-11-05 | official / documentation_checked |
| SITE-S18 | [Cloud network scope](https://learn.chatgpt.com/docs/enterprise/security-cookbook#configure-cloud-environment-networking-separately) | current versus legacy networking | 2026-11-05 | official / documentation_checked |
| SITE-S19 | [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments) | setup, publication and network secrets | 2026-11-05 | official / documentation_checked |
| SITE-S20 | [Non-interactive](https://developers.openai.com/codex/noninteractive) | JSONL/final schema and approval failures | 2026-11-05 | official / documentation_checked |
| SITE-S21 | [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | explicit breakpoints and lifetime | 2026-11-05 | official / documentation_checked |
| SITE-S22 | [Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) | beta ownership and compatibility | 2026-11-05 | official / documentation_checked |
| SITE-S23 | [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling) | pending tools and call_id | 2026-11-05 | official / documentation_checked |
| SITE-S24 | [Mid-turn steering](https://developers.openai.com/api/docs/guides/steering) | steering does not undo tools | 2026-11-05 | official / documentation_checked |
| SITE-S25 | [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | output shape versus truth | 2026-11-05 | official / documentation_checked |

Затронуты: Codex surfaces/configuration/security/workflows, lifecycle, plugin packaging, hooks, skills, memory, runtime, prompting, related playbooks/templates/diagrams и их RU/EN пары. [Проверки текущего обновления](../superpowers/specs/site-docs-refresh-2026-11-05.json).


Этот файл сжат 2026-06-11, чтобы активный source registry оставался ниже soft-size limit в system-file hygiene audit. Полные historical source cards, включая URL, summaries, relevance и verification details, сохранены в archive sibling.

Archive sibling: `source-registry-archive-20260611.txt`.

## Compact field contract

```yaml
title: "Compact source registry route"
url: "docs/sources/source-registry-archive-20260611.txt"
type: "compact source index"
status: "compacted"
checked_at: "2026-06-11"
summary: "Active registry is a compact title and marker index."
relevance: "Full cards and URLs are preserved in the archive sibling."
trust_level: "high"
verification_status: "Current compaction preserves test-visible markers; full evidence remains in the archive sibling and owning source packets."
```

## Compact Source Title Index

- Product-Agent OS task-plan architecture section (checked_at=2026-06-07, trust=high)
- Product-Agent OS Batch 37 S1 task-matrix planning contract (checked_at=2026-06-07, trust=high)
- Product-Agent OS Batch 37 S2 task-matrix template and renderer registration (checked_at=2026-06-07, trust=high)
- Product-Agent OS Batch 37 S3 task-matrix validator, eval and completion-report guard (checked_at=2026-06-07, trust=high)
- Product-Agent OS Batch 37 S4 skill routing, discovery and planning control (checked_at=2026-06-08, trust=high)
- Product-Agent OS Batch 37 S5 docs, projection, hygiene, lifecycle and closure (checked_at=2026-06-08, trust=high)
- Product-Agent OS Batch 38 public docs, README and registry sync (checked_at=2026-06-08, trust=high)
- Product-Agent OS Batch 38 S1 release gate and package metadata (checked_at=2026-06-08, trust=high)
- Product-Agent OS T10-LIVE-M41 post-B38 audit (checked_at=2026-06-08, trust=high)
- Product-Agent OS T10-LIVE-M41 owner no-op closure and B38-S2 verification/install smoke (checked_at=2026-06-08, trust=high)
- Product-Agent OS Batch 38 S3 real-project pilot design (checked_at=2026-06-08, trust=high)
- Product-Agent OS Batch 38 S4 safety and rollback (checked_at=2026-06-08, trust=high)
- Product-Agent OS B38-PILOT-NF01 Neural_Flow target-specific pilot (checked_at=2026-06-08, trust=high)
- Product-Agent OS Batch 40 S1 Doubt verifier loop architecture contract (checked_at=2026-06-09, trust=high)
- Product-Agent OS Batch 40 S2 Doubt verifier loop plugin foundation (checked_at=2026-06-09, trust=high)
- Product-Agent OS Batch 40 S3 Doubt verifier loop eval hardening (checked_at=2026-06-09, trust=high)
- Product-Agent OS Batch 40 S4 Doubt verifier loop docs and site (checked_at=2026-06-10, trust=high)
- Product-Agent OS Batch 40 S4 source-transfer packet (checked_at=2026-06-10, trust=high for transfer bookkeeping; mixed per source family)
- Product-Agent OS Batch 41 first-run orchestration S1-S6 evidence plus first-run welcome/help disclosure (checked_at=2026-06-24, trust=high)
- Product-Agent OS Batch 41 cockpit, architecture dossier and HTML modernization S7-S9 evidence (checked_at=2026-06-20, trust=high)
- Product-Agent OS Batch 42 instruction/tool-use compliance planning matrix (checked_at=2026-06-20, trust=high)
- Product-Agent OS Track 11 documentation refresh G0 governance packet (checked_at=2026-06-20, trust=high)
- Product-Agent OS Track 11 G1 source records, registry and generated-site parity (checked_at=2026-06-20, trust=high)
- Product-Agent OS Track 11 G1.1 project-local documentation toolchain planning matrix (checked_at=2026-06-20, trust=high)
- Product-Agent OS Track 11 G2 first-run cockpit and artifact docs packet (checked_at=2026-06-21, trust=high)
- Product-Agent OS Track 11 G4 operator flows and system behavior docs packet (checked_at=2026-06-22, trust=high)
- Product-Agent OS Track 11 Batch 44 Self-Learning Loop activation, agent/skill metrics and HTML progress matrix with `B44-S0`, `B44-S1` and `B44-S2` local evidence and remaining slices planned-only (checked_at=2026-06-24, trust=high for local plan evidence; arXiv intake trust=primary preprint source)
- Product-Agent OS AI-agent coding standards research corpus with 135 sources, route `plugins/product-agent-os/assets/research/ai-agent-coding-standards-research.md` (checked_at=2026-06-29, trust=high for official sources; medium for community and author methodology sources)
- Product-Agent OS AI-agent senior coding literature research corpus with 60 books, route `plugins/product-agent-os/assets/research/ai-agent-coding-literature-research.md` (checked_at=2026-06-29, trust=high for publisher/author anchors; medium for marketplace bibliography anchors)
- Product-Agent OS Track 11 Batch 45 professional code authoring S0 synthesis and activation policy evidence with `B45-PCA-M01` and `B45-PCA-M20` implemented as `docs_contract_ready` (checked_at=2026-06-29, trust=high for local plan/spec evidence; does not prove runtime or agent behavior)
- Product-Agent OS Track 11 Batch 45 professional code authoring S1 artifact/workflow contract evidence with `B45-PCA-M02..M04` implemented as `docs_contract_ready` (checked_at=2026-06-29, trust=high for local template/test/spec evidence; does not prove runtime or automatic agent behavior)
- Product-Agent OS Track 11 Batch 45 professional code authoring S2 existing workflow/agent/skill retrofit evidence with `B45-PCA-M05..M09`, `B45-PCA-M15` and `B45-PCA-M17` implemented as `docs_contract_ready` (checked_at=2026-06-29, trust=high for local template/docs/test/spec evidence; does not prove runtime, hooks, automation or automatic agent behavior)
- Product-Agent OS Track 11 Batch 45 professional code authoring S3 evals, readiness, route, HTML and hook-governance visibility evidence with `B45-PCA-M10`, `B45-PCA-M11`, `B45-PCA-M16`, `B45-PCA-M18`, `B45-PCA-M21` and `B45-PCA-M22` implemented as `docs_contract_ready` (checked_at=2026-06-29, trust=high for local eval/template/test/spec evidence; does not prove live runtime, hook activation, automation or real AI-agent behavior)
- Product-Agent OS Track 11 Batch 45 professional code authoring S4 public docs/source cross-linking and closure-through-S4 evidence with `B45-PCA-M12`, `B45-PCA-M13` and `B45-PCA-M19` implemented as `docs_contract_ready`, while `B45-PCA-M14` remains closure-through-S4 pending `B45-PCA-M23` in S5 (checked_at=2026-06-29, trust=high for local docs/nav/test/spec evidence; does not prove root site freshness for the new page, runtime, hook activation, automation, provider/browser behavior or real AI-agent behavior)
- Product-Agent OS Track 11 Batch 45 professional code authoring S5 learning-loop and automation-candidate policy evidence with `B45-PCA-M23` implemented as `synthetic_green` and `B45-PCA-M14` updated to full Batch 45 closure after M23 (checked_at=2026-06-29, trust=high for local code/docs/test/spec evidence; does not prove active automation, hook activation, schedule creation, provider/browser behavior, target mutation, raw private chat ingestion or real AI-agent behavior)
- Product-Agent OS Track 11 Batch 45 owner-approved local manual pilot for six real non-mechanical code tasks with filled coding-standard checklists, false-positive, flake, cost and reviewer-usefulness evidence (`B45-PILOT-MANUAL-6-CODE-TASKS-A02`; checked_at=2026-06-30, trust=high for local code/test/spec evidence; promotion decision remains not_made and does not prove hook/blocker activation, active automation, provider/browser/runtime behavior, target mutation, git/release/deploy/publish or production readiness)
- Product-Agent OS Track 11 Batch 45 S6 advisory validation and promotion decision with `B45-PCA-M24..M27` implemented as keep-advisory-only/no-go evidence (checked_at=2026-06-30, trust=high for local/advisory/live-eval/decision summaries; decision is no-go and does not prove real AI-agent behavior improvement, CI/blocker enforcement, browser/runtime proof, target mutation, git/release/deploy/publish or production readiness)
- Product-Agent OS Track 11 Batch 45 Professional Code Authoring solution map, route `research/batch45-professional-code-authoring-solution-map.md` (checked_at=2026-06-30, trust=high as derived orientation from current Batch 45 artifacts; not source truth, runtime proof or promotion evidence)
- Product-Agent OS Track 11 Batch 45 S7 Professional Code Authoring Architecture v2 atlas, route `research/batch45-professional-code-authoring-architecture-v2.md` (checked_at=2026-06-30, trust=high as internal architecture derived from current Batch 45 artifacts; not source truth, source-copy approval, target execution, runtime proof or promotion evidence)
- Product-Agent OS Track 11 Batch 45 S7 real-project scenario inventory, route `research/b45-real-project-scenarios/README.md`, `research/b45-real-project-scenarios/source-inventory.md`, `research/b45-real-project-scenarios/scenario-candidates.json`, `research/b45-real-project-scenarios/rereview-2026-06-30.md` (checked_at=2026-06-30, trust=high for metadata-only read-only inventory and repeat-pass coverage notes over approved target labels; not proof of fixture-copy privacy clearance, target execution, runtime/browser/provider/live API behavior, git write, deployment/publication or external automation)
- Product-Agent OS Track 11 Batch 45 S7 sanitized fixture source policy, route `research/b45-real-project-scenarios/source-policy.md`, `research/b45-real-project-scenarios/scenario-manifest.schema.json`, `research/b45-real-project-scenarios/fixture-manifest.schema.json`, `research/b45-real-project-scenarios/redaction-manifest.schema.json` (checked_at=2026-06-30, trust=high for project-authored pre-copy policy and schema contracts; no source bodies copied, no target execution, no runtime/browser/provider/live API behavior, no git write, no deployment/publication/external automation; M31 source copy remains approval_required)
- Product-Agent OS Track 11 Batch 45 S7 SOL agent orchestration sanitized fixture pack, route `research/b45-real-project-scenarios/fixtures/sol/SOL-AGENT-ORCH-01/` (checked_at=2026-06-30, trust=high for owner-requested `analysis_only` fixture pack and manifest evidence; target `SOL 0.6` remained read-only; no target command/runtime/browser/provider/live API behavior/git/deploy/publish/automation evidence; runtime readiness not claimed)
- Product-Agent OS Track 11 Batch 45 S7 myPartners CRM chat-open sanitized fixture pack, route `research/b45-real-project-scenarios/fixtures/mypartners/MP-CRM-CHAT-OPEN-01/` (checked_at=2026-06-30, trust=high for owner-requested `analysis_only` fixture pack and manifest evidence; target `myPartners` remained read-only; no target command/runtime/browser/provider/live API behavior/git/deploy/publish/automation evidence; runtime readiness and production-data safety not claimed)
- Product-Agent OS Track 11 Batch 45 S7 real-project baseline analysis, route `docs/superpowers/specs/batch45-real-project-baseline-results.json` and `research/b45-real-project-scenarios/results/` (checked_at=2026-06-30, trust=high for fixture-local static/advisory/syntax evidence; SOL and myPartners targets remained read-only; no target command/runtime/browser/provider/live API behavior/git/deploy/publish/automation evidence; refactor readiness limited to fixture-local M33 gates)
- Product-Agent OS Track 11 Batch 45 S7 real-project refactor comparison, route `docs/superpowers/specs/batch45-real-project-refactor-comparison.json` and `research/b45-real-project-scenarios/refactors/` (checked_at=2026-06-30, trust=high for fixture-local comparison evidence; SOL no-code arms record churn prevention under unresolved TypeScript/test gaps; MP source arms reduce advisory warnings `2 -> 1 -> 0` with no new dependencies and syntax-only AST proof; no target command/runtime/browser/provider/live API/database/git/deploy/publish/automation evidence; promotion/readiness not claimed)
- Product-Agent OS Track 11 Batch 45 S7 real-project scorecard, route `docs/superpowers/specs/batch45-real-project-scorecard.json` and `research/b45-real-project-scenarios/results/B45-PCA-M34-scorecard-review.md` (checked_at=2026-06-30, trust=high for fixture-local scorecard evidence; MP advisory-guided is the best low-churn static arm, MP checklist-guided is a structure candidate blocked by characterization/runtime proof, SOL no-code arms are churn prevention; critical runtime/test/TypeScript-advisory/reviewer gaps override averages; no target command/runtime/browser/provider/live API/database/git/deploy/publish/automation/CI-blocker evidence; promotion/readiness not claimed)
- Product-Agent OS Track 11 Batch 45 S7 post-real-project decision packet, route `docs/superpowers/specs/batch45-real-project-decision-packet.json` (checked_at=2026-06-30, trust=high for source-owned decision evidence; keeps advisory-only/no-go for treatment v2 promotion, leaves smaller treatment v2 as source-only future option, defers more fixture pilots, marks disposable runtime/browser pilot approval_required and rejects CI/blocker promotion; no target command/runtime/browser/provider/live API/database/git/deploy/publish/automation/CI-blocker evidence; promotion/readiness not claimed)
- Product-Agent OS Track 11 Batch 45 review remediation local hook/validator hardening and docs/control-plane sync with `B45-PCA-M37` / `B45-PCA-M37-A01`, route `docs/superpowers/specs/batch45-review-remediation-summary.json`, `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md` and `.codex/product-agent-os/reviews/batch45/remediation-agent-04-code-repair.md` (checked_at=2026-07-04, trust=high for local hook/validator/docs/source/control-plane/test evidence; M36 remains reserved for optional runtime/browser approval packet; no runtime/browser/provider/target/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 repeat quality/refactor retest protocol with `B45-RETEST-Q0-Q2` / `B45-RETEST-Q0-Q2-A01`, route `docs/superpowers/specs/batch45-quality-retest-protocol.json` (checked_at=2026-07-04, trust=high for local source-owned protocol, held-out task contract and harness schema evidence; Q3 fixture-static retest remains next local route; no live/model eval, runtime/browser/provider/target/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 repeat quality/refactor retest Q3 fixture-static with `B45-RETEST-Q3-FIXTURE-STATIC` / `B45-RETEST-Q3-FIXTURE-STATIC-A01`, route `docs/superpowers/specs/batch45-quality-retest-fixture-static-summary.json` (checked_at=2026-07-04, trust=high for local/static sanitized-fixture replay; 37 files, 14 advisory warnings, blocking=false; no live/model/runtime/browser/provider/target/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 repeat quality/refactor retest Q4 project-slices-static with `B45-RETEST-Q4-PROJECT-SLICES-STATIC` / `B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01`, route `docs/superpowers/specs/batch45-quality-retest-project-slices-static-summary.json` (checked_at=2026-07-04, trust=high for local/static project-slice replay; 5 slices, 46 files, 14 advisory warnings, blocking=false; no live/model/runtime/browser/provider/target/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 post-Q4 next task queue with `B45-POST-Q4-NEXT-TASKS` / `B45-POST-Q4-NEXT-TASKS-A01`, route `docs/superpowers/specs/batch45-post-q4-next-tasks.json` (checked_at=2026-07-04, trust=high for source-owned post-Q4 task planning; routes targeted static repair, static delta verification, approval-gated live/model proof, promotion decision and optional M36 runtime/browser packet; no live/model/runtime/browser/provider/target/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 post-Q4 T01-T04 execution with `B45-POSTQ4-T01-T04` / `B45-POSTQ4-T01-T04-A01` and `B45-POSTQ4-T04-A01`, routes `docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json` and `docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json` (checked_at=2026-07-04, trust=high for copied-fixture static delta and approval-packet-only evidence; Q4 warnings reduce 14 -> 0; no live/model/runtime/browser/provider/target/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 post-Q4 T05 exact-approved live/model rerun attempt with `B45-POSTQ4-T05-LIVE-MODEL-RERUN` / `B45-POSTQ4-T05-A01`, route `docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json` (checked_at=2026-07-04, trust=high for sanitized T05 rollup; approved Codex CLI/OpenAI calls started 2 primary task runs, completed 1, timed out 1, stopped remaining 14 primary runs plus reviewer by policy; no treatment/reviewer comparison, no M26/M35 reversal, no target/runtime/browser/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T05B revised rerun approval packet with `B45-POSTQ4-T05B-RERUN-PACKET-REVISION` / `B45-POSTQ4-T05B-A01`, route `docs/superpowers/specs/batch45-postq4-t05b-rerun-approval-packet.json` (checked_at=2026-07-04, trust=high for approval-packet-only design after T05 timeout; no live/model/provider call, no reused T05 approval, no treatment/reviewer comparison, no M26/M35 reversal, no target/runtime/browser/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T06 promotion decision with `B45-POSTQ4-T06-PROMOTION-DECISION` / `B45-POSTQ4-T06-A01`, route `docs/superpowers/specs/batch45-postq4-t06-promotion-decision.json` (checked_at=2026-07-04, trust=high for source-owned promotion/no-go decision after static delta and T05 timeout; keeps M25 advisory-only, rejects stronger advisory/CI/blocker/automation promotion, requires fresh approval for T05B/T07; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T08 architecture next-actions with `B45-POSTQ4-T08-ARCHITECTURE-NEXT-ACTIONS` / `B45-POSTQ4-T08-A01`, route `docs/superpowers/specs/batch45-postq4-architecture-next-actions.json` (checked_at=2026-07-04, trust=high for source-owned post-T06 technical/architecture analysis and next routing; recommends T09 closure, T10 live-eval redesign packet, T07 runtime/browser packet and T11 source-only treatment design; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T10 live-eval harness redesign packet with `B45-POSTQ4-T10-LIVE-EVAL-HARNESS-REDESIGN-PACKET` / `B45-POSTQ4-T10-A01`, route `docs/superpowers/specs/batch45-postq4-t10-live-eval-harness-redesign-packet.json` (checked_at=2026-07-05, trust=high for source-owned approval-packet-only harness redesign after T05 timeout and T11 source design; defines paired scheduling, timeout/no-op quarantine, reviewer timing, exact approval fields and privacy retention boundaries; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T12 paired live-model exact approval packet with `B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN-EXACT-APPROVAL-PACKET` / `B45-POSTQ4-T12-A01`, route `docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-exact-approval-packet.json` (checked_at=2026-07-05, trust=high for source-owned exact approval packet draft; later consumed by T12 run approval; no runtime/browser/target/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T12 paired live-model rerun result with `B45-POSTQ4-T12-PAIRED-LIVE-MODEL-RERUN` / `B45-POSTQ4-T12-RUN-A01`, route `docs/superpowers/specs/batch45-postq4-t12-paired-live-model-rerun-results.json` (checked_at=2026-07-05, trust=high for sanitized exact-approved Codex CLI/OpenAI rollup; 16 primary calls, 14 completed, 1 no-op, 1 invalid JSON, 0 timeout, valid_pair_count=6, reviewer not run by gate, no promotion, no M26/M35/T05/T06 reversal, raw outputs temp-only)
- Product-Agent OS Track 11 Batch 45 post-Q4 T11 treatment v3 source design with `B45-POSTQ4-T11-TREATMENT-V3-SOURCE-DESIGN` / `B45-POSTQ4-T11-A01`, route `docs/superpowers/specs/batch45-postq4-t11-treatment-v3-source-design.json` (checked_at=2026-07-05, trust=high for source-owned treatment v3 design after T08 and five sidecar reviews; maps standards to compact pre-edit/post-edit behavior checks and keeps M26/M35/T05/T06 no-go boundaries; no live/model/provider/runtime/browser/target/CI/git/release/deploy/automation proof)
- Product-Agent OS Track 11 Batch 45 post-Q4 T13 strict output schema and harness hardening with `B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING` / `B45-POSTQ4-T13-A01`, route `docs/superpowers/specs/batch45-postq4-t13-strict-output-schema-and-harness-hardening.json` (checked_at=2026-07-05, trust=high for local schema/no-op harness hardening and sanitized rollup validation; no live/model/provider/reviewer call, no target/runtime/browser/CI/git/release/deploy/automation proof, no promotion, no M26/M35/T05/T06 reversal)
- Product-Agent OS Track 11 Batch 45 post-Q4 T14 strict rerun exact approval packet with `B45-POSTQ4-T14-STRICT-RERUN-APPROVAL-PACKET` / `B45-POSTQ4-T14-A01`, route `docs/superpowers/specs/batch45-postq4-t14-strict-rerun-approval-packet.json` (checked_at=2026-07-05, trust=high for source-owned exact approval packet draft after T13 hardening; revised to `gpt-5.5` with `model_reasoning_effort=high` and detailed run/pair/aggregate evidence; owner_confirmed=false, run_authorized_by_this_artifact=false, no live/model/provider/reviewer/runtime/browser/target/CI/git/release/deploy/automation proof, no promotion, no M26/M35/T05/T06/T12 reversal; no strict same-model comparability with prior `gpt-5.3-codex-spark` runs)
- Product-Agent OS Track 11 Batch 45 post-Q4 T14 strict rerun result with `B45-POSTQ4-T14-STRICT-RERUN` / `B45-POSTQ4-T14-RUN-A01`, route `docs/superpowers/specs/batch45-postq4-t14-strict-rerun-results.json` (checked_at=2026-07-05, trust=high for sanitized exact-approved Codex CLI/OpenAI rollup; model `gpt-5.5`, `model_reasoning_effort=high`, 16/16 primary calls completed, valid_pair_count=8, invalid_pair_count=0, timeout/no_op/invalid_json=0, average_score_delta_percent=3.27, treatment_equal_or_better_count=6, reviewer_calls_started=0, no promotion, no M26/M35 reversal, model-change decision still required, raw outputs temp-only)
- Product-Agent OS Track 11 Batch 45 post-Q4 T15 model-change decision with `B45-POSTQ4-T15-DECISION-PACKET-MODEL-CHANGE-INTERPRETATION` / `B45-POSTQ4-T15-A01`, route `docs/superpowers/specs/batch45-postq4-t15-model-change-decision-packet.json` (checked_at=2026-07-05, trust=high for source-owned decision evidence; T14 is a positive current-best-quality signal only, average_score_delta_percent=3.27 is below the >=20% promotion gate, reviewer_calls_started=0, same-model comparability=false, no promotion, no M26/M35 reversal, no live/model/provider/reviewer/runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T16-T22 promotion-grade eval task group with `B45-POSTQ4-T16-T22-PROMOTION-GRADE-EVAL-TASK-GROUP` / `B45-POSTQ4-T16-T22-A01`, route `docs/superpowers/specs/batch45-postq4-t16-t22-promotion-grade-eval-task-group.json` (checked_at=2026-07-07, trust=high for source-owned task-group design after read-only agent scan; defines frozen held-out corpus, explicit same-model/current-model comparison choice, strict structured output, reviewer gate, cost/timeout policy and raw-temp-only retention as required future gates; no promotion-grade eval run, no reviewer/model/provider call, no M26/M35/T15 reversal, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T17 metadata-only frozen held-out corpus with `B45-POSTQ4-T17-FROZEN-HELDOUT-CORPUS` / `B45-POSTQ4-T17-A01`, route `docs/superpowers/specs/batch45-postq4-t17-frozen-heldout-corpus.json` (checked_at=2026-07-07, trust=high for source-owned sanitized manifest; freezes 8 task IDs with source class, privacy class, difficulty, expected evidence, allowed evidence, blocked claims and hashes before any future baseline/treatment execution; no baseline/treatment run, no reviewer/model/provider call, no M26/M35/T15 reversal, no raw private source bodies/secrets/raw private chats/unredacted PII retained, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T18 promotion-grade eval design and strict schema with `B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA` / `B45-POSTQ4-T18-A01`, route `docs/superpowers/specs/batch45-postq4-t18-promotion-grade-eval-design.json` (checked_at=2026-07-08, trust=high for source-owned design/schema evidence after Context7 JSON Schema sanity check and read-only sidecar audits; selects same-model baseline/treatment as the promotion-grade mode, binds to the T17 frozen corpus, defines strict schema, deterministic quarantine, scoring threshold, reviewer rubric, result contract and privacy boundary; no baseline/treatment run, no reviewer/model/provider call, no concrete model approval, no M26/M35/T15 reversal, no raw outputs retained in repo, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T19 cost/timeout/retention policy with `B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY` / `B45-POSTQ4-T19-A01`, route `docs/superpowers/specs/batch45-postq4-t19-cost-timeout-retention-policy.json` (checked_at=2026-07-08, trust=high for source-owned no-run policy evidence after Context7 JSON Schema sanity check and read-only sidecar audits; defines call caps, 600-second per-call timeout, zero automatic retries, abort conditions, owner-filled USD cost cap requirement, raw-temp-only retention, sanitized rollup schema and T20 exact-approval fields; no baseline/treatment run, no reviewer/model/provider call, no concrete model or cost cap approval, no M26/M35/T15 reversal, no raw outputs retained in repo, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T20 exact approval packet with `B45-POSTQ4-T20-EXACT-APPROVAL-PACKET` / `B45-POSTQ4-T20-A01`, route `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet.json` (checked_at=2026-07-08, trust=high for source-owned exact approval packet draft after official OpenAI pricing/config/model checks, Context7 supplemental docs and read-only sidecar audits; names `gpt-5.5`, `model_reasoning_effort=high`, same-model baseline/treatment, frozen corpus v1, 17-call cap, 600-second timeout, USD 25.00 cap, reviewer policy, raw-temp-only retention and abort conditions; owner_confirmed=false, run_authorized_by_this_artifact=false, no baseline/treatment run, no reviewer/model/provider call, no M26/M35/T15 reversal, no raw outputs retained in repo, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T20 exact approval packet 1000s revision with `B45-POSTQ4-T20-EXACT-APPROVAL-PACKET` / `B45-POSTQ4-T20-A02`, route `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json` (checked_at=2026-07-08, trust=high for source-owned exact approval packet revision after official OpenAI pricing check; supersedes `B45-POSTQ4-T20-A01` by changing the per-primary/reviewer timeout to 1000 seconds while preserving `gpt-5.5`, `model_reasoning_effort=high`, same-model baseline/treatment, frozen corpus v1, 17-call cap, zero retries, USD 25.00 cap, reviewer policy, raw-temp-only retention and abort conditions; the packet artifact itself is approval text, later superseded by cost-waived approval `B45-POSTQ4-T20-A03`; no baseline/treatment run by this artifact, no reviewer/model/provider call by this artifact, no M26/M35/T15 reversal, no raw outputs retained in repo, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T20 cost-waived exact approval with `B45-POSTQ4-T20-EXACT-APPROVAL-PACKET` / `B45-POSTQ4-T20-A03`, route `docs/superpowers/specs/batch45-postq4-t20-promotion-grade-eval-approval-packet-cost-waived.json` (checked_at=2026-07-08, trust=high for source-owned owner-confirmed cost-waived approval; cost_policy=owner_accepts_unknown_unbounded_actual_provider_cost_for_this_run; owner accepted unknown/unbounded provider cost for one 17-call run; approval was consumed by `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, primary_calls_started=1, reviewer_calls_started=0, approval_reuse_allowed=false, repo_raw_retention_bytes=0)
- Product-Agent OS Track 11 Batch 45 post-Q4 T21 blocked promotion-grade eval preflight with `B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN` / `B45-POSTQ4-T21-PREFLIGHT-A01`, route `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json` (checked_at=2026-07-08, trust=high for source-owned blocked preflight after T20 approval-boundary check, Context7 supplemental OpenAI eval docs and read-only sidecar audits; owner did not restate the exact T20 approval text, approval_text_present_in_current_user_message=false, run_authorized=false, actual_model_or_reviewer_calls_started=0, estimated_total_cost_usd=0, repo_raw_retention_bytes=0, temp_root_created=false, no baseline/treatment run, no reviewer/model/provider call, no M26/M35/T15 reversal, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T21 blocked promotion-grade eval preflight with `B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN` / `B45-POSTQ4-T21-PREFLIGHT-A02`, route `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json` (checked_at=2026-07-08, trust=high for source-owned blocked preflight after owner supplied an approval-like block that changed the exact T20 timeout from 600s to 1000s; approval_text_present_in_current_user_message=true, approval_text_exact_match=false, run_authorized=false, actual_model_or_reviewer_calls_started=0, estimated_total_cost_usd=0, repo_raw_retention_bytes=0, temp_root_created=false, no baseline/treatment run, no reviewer/model/provider call, no M26/M35/T15 reversal, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T21 historical cost-unknown preflight with `B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN` / `B45-POSTQ4-T21-PREFLIGHT-A03`, route `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-run-preflight-cost-unknown.json` (checked_at=2026-07-08, trust=high for source-owned historical preflight after exact T20-A02 owner restatement; approval_text_exact_match=true, owner_confirmed=true, run_authorized_until_abort_gate=true, cost_known_before_first_call=false, run_authorized=false after abort gate, approval_reuse_allowed=false, actual_model_or_reviewer_calls_started=0, estimated_total_cost_usd=null, repo_raw_retention_bytes=0, temp_root_created=false, no baseline/treatment run, no reviewer/model/provider call, no M26/M35/T15 reversal, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T21 cost-waived promotion-grade eval run with `B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN` / `B45-POSTQ4-T21-COST-WAIVED-RUN-A01`, route `docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-results.json` (checked_at=2026-07-08, trust=high for source-owned cost-waived run result; consumed `B45-POSTQ4-T20-A03`, primary_calls_started=1, reviewer_calls_started=0, valid_pair_count=0, invalid_pair_count=8, schema_failure_count=1, raw_outputs_written_to_repo=false, repo_raw_retention_bytes=0, raw_files_present_after_cleanup=0, promotion_allowed=false, approval_reuse_allowed=false, no valid baseline/treatment pair set, no reviewer gate, no M26/M35/T15 reversal, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 post-Q4 T22 reviewer-gate/no-go decision with `B45-POSTQ4-T22-REVIEWER-GATE-AND-DECISION` / `B45-POSTQ4-T22-A02`, route `docs/superpowers/specs/batch45-postq4-t22-promotion-grade-decision-packet.json` (checked_at=2026-07-08, trust=high for source-owned blocked decision after T21 strict-schema abort; t21_result_exists=true, t21_valid_pair_count=0, t21_invalid_pair_count=8, t21_schema_failure_count=1, reviewer_gate_status=not_run_due_t21_invalid_schema_abort, reviewer_calls_started=0, reviewer_verdict=not_applicable_invalid_t21_result, promotion_allowed=false, repo_raw_retention_bytes=0, no valid baseline/treatment pair set, no reviewer/model call after failed T21 precondition, no M26/M35/T15 reversal, no runtime/browser/target/CI/git/release/deploy/automation action)
- Product-Agent OS Track 11 Batch 45 code-quality runtime recovery task group with `B45-CODE-QUALITY-RUNTIME-RECOVERY` / `B45-CQRR-A01`, route `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json` (checked_at=2026-08-10, trust=high for source-owned planning derived from the post-T22 audit and S9-0 test-ownership repair; T23-T34 cover executable schema/runtime alignment, compact code-change contract, stack/risk-aware test/comment/performance selection, artifact-test debt reduction, deterministic metrics, blinded review, multi-stack corpus, isolated treatment, local readiness and exact-approval-only final eval; no T23-T34 implementation, provider/model/reviewer call, runtime/browser/target/CI/git/release/deploy/automation action or promotion claim)
- Product-Agent OS Track 11 Batch 45 code-quality runtime recovery agent-team plan with `B45-CQRR-TEAM` / `B45-CQRR-A02`, route `docs/superpowers/specs/batch45-code-quality-runtime-recovery-agent-team.json` (checked_at=2026-08-10, trust=high for source-owned ownership and verified handoff routing; assigns every T23-T34 task to accountable, writer, verifier, independent-review, claim-gate and docs roles with explicit skills/write scopes, time-separates the T26/T27/T28 shared test, permits only the disjoint T30/T31 parallel branch and stops before T34 exact approval; no agent dispatch, T23-T34 implementation, external call, git/release action or promotion claim)
- Product-Agent OS Track 11 Batch 45 S9-0 fresh-context handoffs with `B45-S9-0-FRESH-CONTEXT-HANDOFFS` / `B45-CQRR-A03`, route `docs/superpowers/plans/2026-08-10-batch45-s9-0-team-readiness.md` and `docs/superpowers/specs/batch45-s9-0-fresh-context-handoffs.json` (checked_at=2026-08-10, trust=high for current local task-matrix, twelve-packet, role/skill/ownership, parallel-boundary and approval-stop evidence; proves handoff readiness only, with no subagent dispatch, T23-T34 implementation, provider/model/reviewer call, runtime/browser/target/CI/git/release/deploy/automation action, promotion or production-readiness claim)
- Product-Agent OS Track 11 Batch 45 durable contract recovery with `B45-CQRR-A04`, routes `docs/superpowers/plans/2026-08-10-batch45-s9-a-durable-contract-recovery.md` and `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json` (checked_at=2026-08-10T15:15:00+03:00, trust=high for current local implementation and focused-test evidence for T23/T24: shared promotion-result contract/enum source, normalization/quarantine before pair aggregation, exact T21 status regression; final local tests 15/15 and 8/8, `schema_equal=true`, independent `GO_local_code_gate`; does not prove CLI/runtime activation, live/provider/model/reviewer behavior, T22 no-go reversal, promotion, target/CI/Git/release/deploy/automation or production readiness)
- Product-Agent OS Track 11 Batch 45 compact authoring runtime with `B45-CQRR-A05`, routes `docs/superpowers/plans/2026-08-11-batch45-s9-b-compact-authoring-runtime.md` and `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json` (checked_at=2026-08-14T16:32:05+03:00, trust=high for current local implementation and focused-test evidence for T25-T27: compact code-change contract with explicit compatibility, project-native `present_unverified` stack/tool detection and minimum risk-to-test/comment/performance selection; RED behavior 10/3 and standards 6/1, final combined route 54 OK with focused 16/16 and legacy 38/38, reviewer and completion-skeptic `GO_local_code_gate`, RU/EN task-matrix validators and JSON parse, docs 100/100 and `check_docs` green; the RU plan is in `DOC_M25_PENDING_SITE_PAGES`, so no generated-site freshness claim; does not prove CLI/runtime activation, live/provider/model/external-reviewer behavior, T22 no-go reversal, promotion, target/CI/Git/release/deploy/automation or production readiness)
- Codex web / cloud (checked_at=2026-05-14, trust=high)
- Codex app (checked_at=2026-05-14, trust=high)
- Codex CLI (checked_at=2026-05-14, trust=high)
- Codex IDE extension (checked_at=2026-05-14, trust=high)
- Codex use cases (checked_at=2026-05-24, trust=high)
- Codex models (checked_at=2026-05-14, trust=high)
- OpenAI API models (checked_at=2026-05-14, trust=high)
- Agents SDK models and providers (checked_at=2026-05-15, trust=high)
- Reasoning best practices (checked_at=2026-05-14, trust=high)
- Agent Skills (checked_at=2026-05-24, trust=high)
- Codex build plugins (checked_at=2026-05-24, trust=high)
- Codex MCP (checked_at=2026-05-24, trust=high)
- Context7 MCP clients (checked_at=2026-05-15, trust=high)
- Codex hooks (checked_at=2026-08-10, trust=high; current project usage rechecked for project-local trust, concurrent matching handlers, `Bash`/`apply_patch` coverage, timeout semantics and `Stop` continuation contract)
- Subagents (checked_at=2026-05-24, trust=high)
- Subagent concepts (checked_at=2026-05-14, trust=high)
- Custom instructions with AGENTS.md (checked_at=2026-05-24, trust=high)
- Codex best practices (checked_at=2026-05-24, trust=high)
- Codex customization (checked_at=2026-05-24, trust=high)
- Building an AI-native engineering team (checked_at=2026-05-14, trust=high)
- Codex workflows (checked_at=2026-05-24, trust=high)
- Sandbox (checked_at=2026-05-14, trust=high)
- Agent approvals and security (checked_at=2026-05-24, trust=high)
- Codex memories (checked_at=2026-05-24, trust=high)
- Agents SDK sessions (checked_at=2026-05-14, trust=high)
- Agents SDK sandbox agent memory (checked_at=2026-05-14, trust=high)
- Codex changelog (checked_at=2026-05-14, trust=high)
- Codex create skill (checked_at=2026-05-14, trust=high)
- Codex with Agents SDK (checked_at=2026-05-15, trust=high)
- OpenAI Agents SDK Python (checked_at=2026-05-15, trust=high)
- OpenAI Agents SDK agent definitions (checked_at=2026-05-15, trust=high)
- OpenAI Agents SDK MCP (checked_at=2026-05-15, trust=high)
- OpenAI Agents SDK guardrails (checked_at=2026-05-15, trust=high)
- OpenAI Agents SDK Python sessions (checked_at=2026-05-15, trust=high)
- OpenAI Agents SDK tracing (checked_at=2026-05-15, trust=high)
- OpenAI API Responses guide (checked_at=2026-05-24, trust=high)
- OpenAI API structured outputs (checked_at=2026-05-24, trust=high)
- OpenAI API prompting (checked_at=2026-05-24, trust=high)
- OpenAI API prompt engineering (checked_at=2026-05-24, trust=high)
- OpenAI API model optimization (checked_at=2026-05-24, trust=high)
- OpenAI API text generation (checked_at=2026-05-24, trust=high)
- OpenAI API function calling (checked_at=2026-05-24, trust=high)
- OpenAI API tools guide (checked_at=2026-05-24, trust=high)
- OpenAI API file search (checked_at=2026-05-24, trust=high)
- OpenAI API retrieval (checked_at=2026-05-24, trust=high)
- OpenAI API embeddings (checked_at=2026-05-24, trust=high)
- OpenAI API evaluation best practices (checked_at=2026-05-24, trust=high)
- OpenAI Agents SDK guide (checked_at=2026-05-24, trust=high)
- OpenAI Agents SDK guardrails and human review (checked_at=2026-05-24, trust=high)
- OpenAI Agents SDK integrations and observability (checked_at=2026-05-24, trust=high)
- OpenAI evaluate agent workflows (checked_at=2026-05-24, trust=high)
- OpenAI Agents SDK orchestration and handoffs (checked_at=2026-05-24, trust=high)
- OpenAI API data controls (checked_at=2026-05-24, trust=high)
- OpenAI API safety best practices (checked_at=2026-05-24, trust=high)
- OpenAI API production best practices (checked_at=2026-05-24, trust=high)
- Promptfoo (checked_at=2026-05-24, trust=medium)
- Promptfoo assertions and metrics (checked_at=2026-05-24, trust=medium)
- Ragas metrics (checked_at=2026-05-24, trust=medium)
- OpenTelemetry GenAI semantic conventions (checked_at=2026-05-24, trust=medium)
- OpenAI Cookbook hallucination guardrails (checked_at=2026-05-24, trust=high)
- How OpenAI uses Codex (checked_at=2026-05-14, trust=high)
- A practical guide to building agents (checked_at=2026-05-14, trust=high)
- AGENTS.md open format (checked_at=2026-05-14, trust=medium)
- Codex CLI features (checked_at=2026-05-14, trust=high)
- Codex automations (checked_at=2026-05-24, trust=high)
- Codex iterate on difficult problems (checked_at=2026-05-14, trust=high)
- Codex add evals to your AI application (checked_at=2026-05-24, trust=high)
- OpenAI Codex: Building an AI-Native Engineering Team (checked_at=2026-05-24, trust=high)
- Codex code review for GitHub pull requests (checked_at=2026-05-14, trust=high)
- Codex create a CLI Codex can use (checked_at=2026-05-14, trust=high)
- Codex keep documentation up-to-date (checked_at=2026-05-14, trust=high)
- Codex run verified operations (checked_at=2026-05-24, trust=high)
- Codex save workflows as skills (checked_at=2026-05-24, trust=high)
- Codex set up a teammate (checked_at=2026-05-14, trust=high)
- Codex use cases taxonomy and collections (checked_at=2026-05-24, trust=high)
- Codex build responsive front-end designs (checked_at=2026-05-14, trust=high)
- Codex turn Figma designs into code (checked_at=2026-05-14, trust=high)
- Codex follow a goal (checked_at=2026-05-24, trust=high)
- Codex create browser-based games (checked_at=2026-05-14, trust=high)
- Codex debug in iOS simulator (checked_at=2026-05-14, trust=high)
- Codex build for macOS (checked_at=2026-05-14, trust=high)
- Codex automate bug triage (checked_at=2026-05-14, trust=high)
- Codex bring your app to ChatGPT (checked_at=2026-05-14, trust=high)
- Codex use your computer (checked_at=2026-05-14, trust=high)
- Agile Alliance Test-Driven Development (checked_at=2026-05-24, trust=high)
- Martin Fowler: The Practical Test Pyramid (checked_at=2026-05-24, trust=medium)
- Kent C. Dodds: Testing Trophy (checked_at=2026-05-24, trust=medium)
- ISTQB Certified Tester Foundation Level Syllabus v4.0.1 (checked_at=2026-05-24, trust=high)
- pytest documentation (checked_at=2026-05-24, trust=high)
- pytest fixtures (checked_at=2026-05-24, trust=high)
- pytest parametrizing tests (checked_at=2026-05-24, trust=high)
- Vitest features (checked_at=2026-05-24, trust=high)
- Vitest coverage (checked_at=2026-05-24, trust=high)
- Jest snapshot testing (checked_at=2026-05-24, trust=high)
- Playwright retries (checked_at=2026-05-24, trust=high)
- Stryker mutation testing (checked_at=2026-05-24, trust=high)
- Stryker mutation metrics (checked_at=2026-05-24, trust=high)
- Hypothesis documentation (checked_at=2026-05-24, trust=high)
- Codecov about code coverage (checked_at=2026-05-24, trust=medium)
- GitHub Actions GITHUB_TOKEN permissions (checked_at=2026-05-24, trust=high)
- Feature-Sliced Design documentation (checked_at=2026-05-24, trust=high)
- C4 model (checked_at=2026-05-24, trust=high)
- arc42 template overview (checked_at=2026-05-24, trust=high)
- ISO/IEC/IEEE 42010:2022 (checked_at=2026-05-24, trust=high)
- SEI Architecture Tradeoff Analysis Method (checked_at=2026-05-24, trust=high)
- OpenAPI Initiative (checked_at=2026-05-23, trust=high)
- OpenAPI Specification v3.2.0 (checked_at=2026-05-24, trust=high)
- OpenAPI Specification v3.1.1 (checked_at=2026-05-23, trust=high)
- AsyncAPI Specification v3.1.0 (checked_at=2026-05-24, trust=high)
- RFC 9110: HTTP Semantics (checked_at=2026-05-24, trust=high)
- RFC 9457: Problem Details for HTTP APIs (checked_at=2026-05-24, trust=high)
- RFC 9700: Best Current Practice for OAuth 2.0 Security (checked_at=2026-05-24, trust=high)
- OWASP API Security Top 10 2023 (checked_at=2026-05-24, trust=high)
- JSON Schema Specification (checked_at=2026-05-24, trust=high)
- CloudEvents (checked_at=2026-05-24, trust=high)
- GraphQL Specification Versions (checked_at=2026-05-24, trust=high)
- gRPC Introduction (checked_at=2026-05-24, trust=high)
- Pact Documentation (checked_at=2026-05-24, trust=high)
- OpenAPI Generator (checked_at=2026-05-24, trust=high)
- Stoplight Open Source API Toolkit (checked_at=2026-05-24, trust=medium)
- Google API Improvement Proposals (checked_at=2026-05-24, trust=medium)
- Storybook Autodocs (checked_at=2026-05-24, trust=high)
- Storybook accessibility tests (checked_at=2026-05-24, trust=high)
- Storybook interaction tests (checked_at=2026-05-24, trust=high)
- Storybook visual tests (checked_at=2026-05-24, trust=high)
- Playwright visual comparisons (checked_at=2026-05-24, trust=high)
- Playwright Trace Viewer (checked_at=2026-05-24, trust=high)
- Testing Library guiding principles (checked_at=2026-05-24, trust=high)
- WAI-ARIA Authoring Practices Guide (checked_at=2026-05-24, trust=high)
- MDN accessible HTML (checked_at=2026-05-24, trust=high)
- MDN using media queries (checked_at=2026-05-24, trust=high)
- web.dev Web Vitals (checked_at=2026-05-24, trust=high)
- web.dev Interaction to Next Paint (checked_at=2026-05-24, trust=high)
- GitLab documentation site architecture (checked_at=2026-05-23, trust=high)
- GitHub Actions workflows (checked_at=2026-05-24, trust=high)
- GitHub Actions deployments and environments (checked_at=2026-05-24, trust=high)
- GitHub Releases (checked_at=2026-05-24, trust=high)
- GitHub protected branches (checked_at=2026-05-23, trust=high)
- MkDocs (checked_at=2026-05-23, trust=high)
- Sphinx autodoc (checked_at=2026-05-23, trust=high)
- Antora documentation (checked_at=2026-05-23, trust=high)
- Agile Alliance Acceptance Test-Driven Development (checked_at=2026-05-24, trust=high)
- Agile Alliance Behavior-Driven Development (checked_at=2026-05-24, trust=high)
- Martin Fowler: Bounded Context (checked_at=2026-05-24, trust=medium)
- Martin Fowler: Ubiquitous Language (checked_at=2026-05-24, trust=medium)
- Domain Language (checked_at=2026-05-24, trust=medium)
- Agile Alliance User Stories (checked_at=2026-05-24, trust=high)
- Cucumber Gherkin Reference (checked_at=2026-05-24, trust=high)
- Cucumber Example Mapping (checked_at=2026-05-24, trust=high)
- ISO/IEC/IEEE 29148:2018 (checked_at=2026-05-24, trust=high)
- IEEE/ISO/IEC 29148-2018 (checked_at=2026-05-24, trust=high)
- IIBA BABOK (checked_at=2026-05-24, trust=high)
- Martin Fowler: Domain-Driven Design (checked_at=2026-05-24, trust=medium)
- EventStorming (checked_at=2026-05-24, trust=medium)
- Domain Storytelling Requirements (checked_at=2026-05-24, trust=medium)
- Google HEART framework paper (checked_at=2026-05-24, trust=high)
- Amplitude North Star Hub (checked_at=2026-05-24, trust=medium)
- Amplitude taxonomy planning (checked_at=2026-05-24, trust=medium)
- Amplitude implementation team organization (checked_at=2026-05-24, trust=medium)
- Product Talk Opportunity Solution Trees (checked_at=2026-05-24, trust=medium)
- The Lean Startup methodology (checked_at=2026-05-24, trust=medium)
- Strategyzer Value Proposition Canvas (checked_at=2026-05-24, trust=medium)
- MADR (checked_at=2026-05-24, trust=high)
- Structurizr DSL (checked_at=2026-05-24, trust=high)
- Structurizr as code (checked_at=2026-05-24, trust=high)
- Mermaid syntax reference (checked_at=2026-05-24, trust=high)
- Thoughtworks: Fitness function-driven development (checked_at=2026-05-24, trust=medium)
- AWS Well-Architected Framework (checked_at=2026-05-24, trust=high)
- Azure Well-Architected Framework (checked_at=2026-05-24, trust=high)
- PlantUML sequence diagram documentation (checked_at=2026-05-23, trust=high)
- TypeDoc (checked_at=2026-05-23, trust=high)
- JSDoc block and inline tags (checked_at=2026-05-23, trust=high)
- Oracle Javadoc documentation comment specification (checked_at=2026-05-23, trust=high)
- Microsoft C# XML documentation comments (checked_at=2026-05-23, trust=high)
- DBML documentation (checked_at=2026-05-23, trust=high)
- dbdocs generate DBML from database (checked_at=2026-05-23, trust=high)
- SchemaSpy documentation (checked_at=2026-05-23, trust=high)
- Docusaurus (checked_at=2026-05-23, trust=high)
- Docusaurus versioning (checked_at=2026-05-23, trust=high)
- Read the Docs (checked_at=2026-05-23, trust=high)
- GitHub CODEOWNERS (checked_at=2026-05-23, trust=high)
- GitHub workflow syntax (checked_at=2026-05-23, trust=high)
- Vale styles (checked_at=2026-05-23, trust=high)
- markdownlint rules (checked_at=2026-05-23, trust=high)
- Keep a Changelog (checked_at=2026-05-24, trust=high)
- Semantic Versioning 2.0.0 (checked_at=2026-05-24, trust=high)
- Conventional Commits 1.0.0 (checked_at=2026-05-24, trust=high)
- NIST Secure Software Development Framework SP 800-218 (checked_at=2026-05-24, trust=high)
- NIST Cybersecurity Framework 2.0 (checked_at=2026-05-24, trust=high)
- OWASP SAMM (checked_at=2026-05-24, trust=high)
- OWASP Application Security Verification Standard (checked_at=2026-05-24, trust=high)
- OWASP Top 10 Web Application Security Risks (checked_at=2026-05-24, trust=high)
- OWASP Top 10 for LLM Applications 2025 (checked_at=2026-05-24, trust=high)
- OWASP Secrets Management Cheat Sheet (checked_at=2026-05-24, trust=high)
- OWASP Logging Cheat Sheet (checked_at=2026-05-24, trust=high)
- GitHub Actions secure use reference (checked_at=2026-05-24, trust=high)
- GitHub secret scanning (checked_at=2026-05-24, trust=high)
- SLSA specification v1.1 (checked_at=2026-05-24, trust=high)
- OpenSSF Scorecard (checked_at=2026-05-24, trust=high)
- SPDX specifications (checked_at=2026-05-24, trust=high)
- CycloneDX specification overview (checked_at=2026-05-24, trust=high)
- Web Content Accessibility Guidelines 2.2 (checked_at=2026-05-24, trust=high)
- DORA software delivery performance metrics (checked_at=2026-05-24, trust=high)
- Google SRE: Service Level Objectives (checked_at=2026-05-24, trust=high)
- Google SRE: Release Engineering (checked_at=2026-05-24, trust=high)
- Google SRE: Postmortem Culture (checked_at=2026-05-24, trust=high)
- OpenTelemetry Documentation (checked_at=2026-05-24, trust=high)
- The Twelve-Factor App (checked_at=2026-05-24, trust=high)
- CNCF GitOps glossary (checked_at=2026-05-24, trust=high)
- Argo Rollouts (checked_at=2026-05-24, trust=high)
- OpenFeature (checked_at=2026-05-24, trust=high)
- CNCF Cloud Native Definition (checked_at=2026-05-24, trust=high)
- Kubernetes liveness, readiness, and startup probes (checked_at=2026-05-24, trust=high)
- Alistair Cockburn: Hexagonal Architecture (checked_at=2026-05-24, trust=medium)
- Martin Fowler: Microservices Guide (checked_at=2026-05-24, trust=medium)
- Microsoft Azure Architecture Center: Retry pattern (checked_at=2026-05-24, trust=medium)
- Microsoft Azure Architecture Center: Circuit Breaker pattern (checked_at=2026-05-24, trust=medium)
- Microsoft Azure Architecture Center: Queue-Based Load Leveling pattern (checked_at=2026-05-24, trust=medium)
- Microsoft Azure Architecture Center: Health Endpoint Monitoring pattern (checked_at=2026-05-24, trust=medium)
- Microsoft Azure Architecture Center: Saga pattern (checked_at=2026-05-24, trust=medium)
- PostgreSQL Transaction Isolation (checked_at=2026-05-24, trust=high)
- PostgreSQL Backup and Restore (checked_at=2026-05-24, trust=high)
- PostgreSQL Constraints (checked_at=2026-05-24, trust=high)
- PostgreSQL Indexes (checked_at=2026-05-24, trust=high)
- PostgreSQL EXPLAIN (checked_at=2026-05-24, trust=high)
- Liquibase core concepts (checked_at=2026-05-24, trust=high)
- Liquibase rollback (checked_at=2026-05-24, trust=high)
- Redgate Flyway migrations (checked_at=2026-05-24, trust=medium)
- dbt data tests (checked_at=2026-05-24, trust=high)
- dbt model contracts (checked_at=2026-05-24, trust=high)
- Great Expectations Expectations overview (checked_at=2026-05-24, trust=high)
- OpenLineage documentation (checked_at=2026-05-24, trust=high)
- NIST Privacy Framework 1.1 usage guidance (checked_at=2026-05-24, trust=high)
- NIST Privacy Framework (checked_at=2026-05-24, trust=high)
- California Consumer Privacy Act (checked_at=2026-05-24, trust=high)
- GDPR Regulation 2016/679 (checked_at=2026-05-24, trust=high)
- Martin Fowler: Evolutionary Database Design (checked_at=2026-05-24, trust=medium)
- Prisma Data Guide: expand and contract pattern (checked_at=2026-05-24, trust=medium)
- Product-Agent OS pre-Track 8 implemented plans and specs inventory (checked_at=2026-05-27, trust=high)
- Product-Agent OS Track 9 methodology intelligence design and backlog (checked_at=2026-05-25, trust=high)
- Product-Agent OS Track 9 backend methodology coverage (checked_at=2026-05-25, trust=high)
- Product-Agent OS Track 9 API & Integrations methodology coverage (checked_at=2026-05-25, trust=high)
- Product-Agent OS Track 9 Database & Data methodology coverage (checked_at=2026-05-26, trust=high)
- Product-Agent OS Track 8 scenario, eval and transcript docs with discovery status (checked_at=2026-05-24, trust=high)
- OpenAI Codex GitHub repository (checked_at=2026-05-14, trust=high)
- obra/superpowers (checked_at=2026-05-23, trust=medium)
- Community search backlog: Codex CLI tips and workflows (checked_at=2026-05-14, trust=low)
- Product-Agent OS Track 1-9 final documentation closure (checked_at=2026-05-27, trust=high)
- Product-Agent OS Track 10 guided question and status dashboard coverage (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 self-verification metrics-loop Batch 7 foundation (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 self-verification metrics-loop Batch 8 trace redaction dataset judge contracts (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 self-verification metrics-loop Batch 9 metrics scorecards confidence cadence contracts (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 self-verification metrics-loop Batch 10 ledger reports candidates cli contracts (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 self-verification metrics-loop Batch 11 runtime discovery lifecycle eval contracts (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 self-verification metrics-loop final closure (checked_at=2026-05-28, trust=high)
- Product-Agent OS Track 10 project code graph Batch 13-14 foundation and overlays (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 15 query runtime analysis (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 16 cockpit visualization (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 17 evals and future gates (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 18 final verification closure (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 19 offline static search index (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 20 local query backend gate (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 21 semantic retrieval, embeddings and cross-encoder eval (checked_at=2026-06-01, trust=high)
- Product-Agent OS Track 10 project code graph Batch 22 LLM semantic extraction (checked_at=2026-06-02, trust=high)
- Product-Agent OS Track 10 project code graph Batch 23 future extension verification (checked_at=2026-06-02, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 24 live governance (checked_at=2026-06-02, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 25 live runtime (checked_at=2026-06-02, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 26 external embedding provider gate and eval (checked_at=2026-06-02, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 27 cross-encoder reranker and hybrid retrieval (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 28 live LLM proposal adapter and safety eval (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 29 human review ledger and proposal diff preview (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 30 canonical graph mutation journal and rollback (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 31 audit logging security privacy observability and agent skill routing (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 32 real testing readiness target consent pilot harness and Codex surface smoke (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 33 runtime browser QA performance and stabilization (checked_at=2026-06-03, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 34 docs packaging closure matrix (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 34 project-authored docs packet (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 34A public docs boundary and IA packet (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 34B public copy rewrite packet (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 34C RU/EN I18N localization packet (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 34D product docs QA and closure packet (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 34E full-site i18n parity corrective matrix (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M34-M37 full-site i18n inventory and nav gate (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M38-M43 EN sibling translation pass (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M44 EN editorial quality sweep (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M45 RU quality sweep (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M46 language switcher parity (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M47 search sitemap and strict build parity (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34E M48-M49 final full-site i18n closure (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 34 packaging/install smoke packet (checked_at=2026-06-03, trust=high)
- Product-Agent OS Batch 35 approval packet draft (checked_at=2026-06-06, trust=high)
- Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 35 M37 approved local runtime launch evidence (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 35 M38 actual browser automation smoke evidence (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 35 M39 Codex session provider pilot evidence (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 35 M40 canonical mutation pilot evidence (checked_at=2026-06-06, trust=high)
- Product-Agent OS Batch 35 M41 git release/PR preflight evidence (checked_at=2026-06-06, trust=high)
- Product-Agent OS root RUNLOG compaction and evidence ownership (checked_at=2026-06-07, trust=high)
- Product-Agent OS root PLAN compaction and sequencing ownership (checked_at=2026-06-07, trust=high)
- Product-Agent OS root TEST compaction and verification ownership (checked_at=2026-06-07, trust=high)
- Product-Agent OS root AGENTS compaction and durable-rule ownership (checked_at=2026-06-07, trust=high)
- Product-Agent OS root EVALS compaction and eval ownership (checked_at=2026-06-07, trust=high)
- Product-Agent OS root README compaction and product-entrypoint ownership (checked_at=2026-06-07, trust=high)
- Product-Agent OS root control-plane current-state owner page, route `docs/product-agent-os/control-plane-current-state.md`, with `PLAN.md`, `RUNLOG.md`, `TEST.md` and `EVALS.md` compacted under the root routing contract and cold batch ledgers moved to source-owned docs/spec/backlog artifacts (checked_at=2026-07-07, trust=high for local docs/control-plane source routing; no runtime/browser/provider/target/git/release/deploy/automation claim)
- Product-Agent OS system file hygiene audit (checked_at=2026-06-07, trust=high)
- Codex Docs GPT-5.6 system-file audit and R1-R6 follow-up remediation, source report `research/2026-07-23-codex-gpt-5p6-system-files-audit.md` (checked_at=2026-08-06, trust=high for current repository/config/contract-test evidence; fresh-session MCP/`SessionStart` and behavioral quality/cost/latency promotion remain unverified)
- Product-Agent OS Batch 40 S5 Doubt verifier pilot metrics and closure (checked_at=2026-06-10, trust=high)

## Compact verification marker appendix

These markers preserve source-owned test routing after registry compaction. Full card context remains in the archive sibling.

```text
- product-agent-os
- mkdocs.yml
- check_docs.py
- registry.md
- registry.en.md
- product-agent-os-track-8-detailed-backlog.md
- product-agent-os-track-9-backlog.md
- product-agent-os-track-10-backlog.md
- product-agent-os-track-10-backlog.en.md
- product-agent-os-batch34-packaging-install-smoke.md
- product-agent-os-batch34a-public-docs-boundary.md
- product-agent-os-batch34b-public-copy-rewrite.md
- product-agent-os-batch34c-i18n-localization.md
- product-agent-os-batch34d-product-docs-qa-closure.md
- product-agent-os-batch34e-full-site-i18n-inventory.md
- product-agent-os-batch35-approval-packet-draft.md
- product-agent-os-batch35-approval-packet-draft.en.md
- product-agent-os-batch40-doubt-verifier-pilot-closure.md
- product-agent-os-batch40-doubt-verifier-pilot-closure.en.md
- 2026-05-25-track-9-methodology-intelligence.md
- 2026-05-27-track-10-guided-questions-status-dashboard.md
- README.md
- REQUIREMENTS.md
- PLAN.md
- TEST.md
- EVALS.md
- RUNLOG.md
- 2026-05-14-product-agent-os-generated-infrastructure.md
- 2026-05-14-product-agent-os-lifecycle-skills.md
- 2026-05-14-product-agent-os-plugin-core.md
- 2026-05-14-product-agent-os-production-hardening.md
- 2026-05-15-product-agent-os-codex-runtime-runner.md
- assets
- .html
- Task 26 Batch 35 `T10-LIVE-M41`
- owner_closed_no_op_git_release_pr
- blocked_pending_explicit_cache_mutation_approval
- docs/sources/registry.md
- docs/sources/product-agent-os-track-8-detailed-backlog.md
- docs/sources/product-agent-os-track-9-backlog.md
- docs/sources/product-agent-os-track-10-backlog.md
- docs/sources/product-agent-os-batch35-approval-packet-draft.md
- no git stage/commit/push/PR
- git diff --check
- python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
- B37-S1
- T10-PLAN-M01..M03
- T10-PLAN-M18
- task-matrix contract
- task-matrix-plan.md
- plugins/product-agent-os/assets/templates/artifact-templates/task-matrix-plan.md
- .codex/artifact-templates/task-matrix-plan.md
- artifact-task-matrix-plan
- renderer_file_count: 195
- does not call providers/live external model/API endpoints
- does not perform git stage/commit/push/PR
- B37-S2
- T10-PLAN-M04..M05
- T10-PLAN-M17
- validate_task_matrix.py
- validate_task_matrix_text
- task-matrix-validator-and-completion-report
- B37-S3
- T10-PLAN-M06
- T10-PLAN-M10
- T10-PLAN-M13
- present_unverified
- hard gates live in validator/tests/skills
- B37-S4
- T10-PLAN-M07..M09
- T10-PLAN-M20
- B37-S5
- T10-PLAN-M11..M12
- T10-PLAN-M14..M16
- T10-PLAN-M19
- T10-SV-M58..M62
- B34E-I18N-M34..M49
- Self-Verification And Modernization Loop
- docs/product-agent-os/index.md
- artifact-gallery.md
- methodology-intelligence.md
- approval-bound-real-testing.md
- plugins/product-agent-os/README.md
- server_shutdown_complete: true
- Playwright Chromium
- codex_user_session
- canonical_graph_source_mutated: false
- Solution architecture
- Codex / Agentic Workflow
- Frontend
- Backend
- approval_required
- usage_mode
- approval boundary
- no browser automation
- no canonical graph mutation
- product-agent-os/artifact-gallery.md
- B38-DOC-M04..M10
- artifact/output gallery
- public/internal documentation boundary
- compact README routing
- RU/EN parity confirmation
- final docs verification
- generated `site/` refresh decision
- read-only agent audits for README/i18n/registry/site scope
- site/` was refreshed intentionally
- root RUNLOG/TEST/EVALS remain compact
- verification_status: "Backed by the Batch 38 docs contract
- generated
- refresh decision
- B38-PROD-M01..M03
- git_stage_commit_push_pr_performed: false
- B38-S1 `B38-PROD-M01..M03`
- package_source_digest_sha256
- local-only/internal R&D distribution
- verification_status: "Backed by the B38-S1 source packet
- focused docs contract
- Codex compatibility returned `status: compatible`
- historical_preflight_snapshot
- B37/B38/B38-S1 did not themselves close M41
- fresh preflight is required before any git write
- B38-PROD-M04
- plugin_cache_refresh_attempt_status: blocked_sandbox_cache_write_denied_after_backup_stage
- cache_backup_path
- local_cache_refresh_result: REFRESH_OK
- local_cache_backup_path: tmp/product-agent-os-cache-backup-local-20260608-180210
- local_cache_moved_aside_target: local-product-agent-plugins/product-agent-os/0.1.0.pre-refresh-20260608-180210
- plugin_cache_refresh_final_status: completed_local_cache_refresh_from_prepared_stage
- target_cache_files_after_refresh: 586
- target_cache_skill_count_after_refresh: 11
- target_cache_docs_maintainer_present_after_refresh: true
- target_cache_still_stale: false
- blocked_sandbox_cache_write_denied_after_backup_stage
- B38-S2 `B38-PROD-M04..M05`
- fixture eval exited `0`
- approval_boundary
- docs-only
- AI/RAG
- product-agent-os/real-project-pilot.md
- B38-PROD-M06
- pilot_target_count: 7
- no_real_project_execution_performed
- B38-S3 `B38-PROD-M06..M09`
- design_only_not_run
- docs contract
- strict MkDocs
- B38-PROD-M10
- active_schedule_markers: 0
- B38-S4 `B38-PROD-M10..M11`
- reviewed_gap_recorded
- rollback/remove/cache recovery
- No release security certification
- validate_source_policy.py
- validate_system_file_hygiene.py
- secret_like_findings: 6
- validate_codex_compatibility.py
- not a security certification
- source_policy_status
- blocked
- false
- tmp/neural-flow-product-agent-os-pilot-20260608-191510
- internal target-specific pilot evidence
- usage_mode: legacy_onboarding
- source_policy_status: blocked
- false `pr_review` route
- dashboard aggregation is incomplete
- staged hooks require exact owner approval
- No target workspace mutation
- run_methodology_audit.py
- 481 nodes
- secret_like_findings: 0
- staged outputs validated
- root_readme
- technical
- system_file_hygiene_audit
- system-file-hygiene-audit.md
- system-file-hygiene-report.md
- on-change
- release/automation
- schedule_status: not_created
- read_only
- root control-plane files
- docs source-control files
- .github/workflows
- T10-HYG-M04..M06
- T10-HYG-M07
- workflow-system-file-hygiene-audit
- artifact-system-file-hygiene-report
- automation-system-file-hygiene-audit
- T10-HYG-M08..M09
- Product-Agent OS technical docs
- runtime automation docs
- source registry/backlog
- renderer_file_count: 194
- T10-HYG-M10..M12
- activation_gate
- accepted_residual_risks_present
- future_activation_handoff_required
- schedule text for non-metrics candidates
- T10-HYG-M13
- file_statuses
- mtime_utc
- age_days
- content_digest
- last_audit_at
- status_dashboard_projection
- system file hygiene projection is generated status evidence, not source of truth
- T10-HYG-M14..M15
- System Hygiene
- system-file-hygiene
- status_dashboard.py
- status-dashboard/status.html
- status-dashboard/status.css
- top_finding
- missing
- unreadable
- stale
- owner_unknown
- T10-HYG-M16..M17
- system_file_hygiene_dashboard_present
- system_file_status_dates_present
- agent_skill_file_status_present
- system_hygiene_dashboard_not_source_of_truth
- filesystem metadata
- freshness hints
- not semantic proof
- batch36_final_closure
- strict_mkdocs_environment_gap
- No module named mkdocs
- audit_trigger
- no_secrets_status
- active_schedule_markers
- finding_type
- compaction_decision
- --trigger
- scenarios.md
- behavioral-evals.md
- codex-compatibility.md
- product-agent-os/scenarios.md
- product-agent-os/behavioral-evals.md
- product-agent-os/codex-compatibility.md
- T10-Q-M15..M22
- T10-Q-M23..M25
- question_queue_contract_present
- status_snapshot_present
- status_dashboard_present
- dashboard_no_external_assets
- dashboard_not_source_of_truth
- stale_evidence_no_success_claim
- status snapshot
- Task 23 guided question protocol and status dashboard
- scenarios
- requirements
- agent_skill_metrics_loop_contract_present
- metrics_report_redacted
- trace_normalization_contract_present
- judge_calibration_gate_present
- scorecard_ledger_contract_present
- source_priority_contract_present
- metrics_packet_bounds_present
- trace_data_classification_gate_present
- offline_artifact_safety_shared
- no_baseline_renderer_pollution
- active_metrics_automation_blocked
- update_candidate_rollback_required
- metrics_loop_runtime_route_contract_present
- metrics_loop_lifecycle_contract_present
- metrics_loop_false_positive_guards_present
- agent_skill_metrics_loop
- target registry
- trace intake
- dataset quality
- grader/judge calibration
- cadence recommendation
- scorecard ledger
- modernization candidates
- staged evidence
- active schedules
- self-verification metrics loop
- staged evidence only
- explicit-only git boundary
- T10-CG-V2-M19..M26
- project_cockpit_model.py
- project_graph_visual_model.py
- project_graph_renderer.py
- project-cockpit.html
- Graphology-compatible static visual projection
- local Graphology/Sigma vendor boundary
- Code Flow
- Code Intelligence
- local Graphology/Sigma
- selected-node evidence
- fallback
- no external assets
- not source of truth
- Task 25 Batch 16
- Graphology-compatible static
- fallback static
- explicit-only
- T10-CG-V2-M27..M30
- project_graph_search_quality.py
- project_graph_search_quality_present
- project_graph_future_backend_semantic_gates_present
- search-quality eval loop
- fixture structural fields
- future backend and semantic gates
- live database/server
- Task 25 Batch 17
- explicit approval
- T10-CG-V2-M39
- Batch 20 local backend gate
- project_graph_extension_closure.py
- T10-CG-V2-M52..M57
- project_graph_llm_extraction.py
- project_graph_llm_extraction_gate_present
- rationale/comment proposals
- staged proposals, not canonical graph facts
- prompt/model policy
- semantic node and edge proposals
- AI incident workflow
- Task 25 Batch 22
- structured JSON
- rollback/disable path
- project_graph_llm_proposal_schema_present
- project_graph_rationale_comment_proposals_present
- project_graph_llm_extraction_eval_present
- T10-CG-V2-M58..M62
- project_graph_future_extension_closure_present
- project_graph_extension_rollback_deletion_present
- verify-extensions
- disable-extensions
- deletion proof
- graph-only fallback
- blocked_without_new_explicit_approval
- Task 25 Batch 23
- rollback/data deletion proof
- no live external model/API calls
- project_graph_unapproved_surface_blocking_present
- project_graph_extension_full_verification_contract_present
- T10-LIVE-M01..M06
- project_graph_live_governance.py
- project_graph_live_approval_packet_present
- project_graph_live_redaction_guard_present
- project_graph_live_data_classification_policy_present
- project_graph_provider_credentials_boundary_present
- project_graph_live_cache_deletion_policy_present
- project_graph_live_budget_guard_present
- project_graph_live_governance_no_live_calls_present
- no live server
- no provider calls
- T10-LIVE-M07..M10
- project_graph_live_runtime.py
- project_graph_live_runtime_contract_present
- project_graph_live_runtime_auth_policy_present
- Live Local Read-Only Runtime, Auth And Fallback
- project_graph_live_runtime_governance_prerequisite_present
- project_graph_live_runtime_read_only_routes_present
- project_graph_live_runtime_lifecycle_controls_present
- project_graph_live_runtime_graph_only_fallback_present
- project_graph_live_runtime_no_public_or_mutation_surface_present
- disabled_by_default_not_started
- local-only access
- rejects unauthorized access
- no write endpoints
- graph_only_query_mode
- T10-LIVE-M11..M12
- project_graph_embedding_provider.py
- project_graph_external_embedding_provider_gate_present
- project_graph_external_embedding_eval_baseline_present
- No external call without approval/redaction/cache/budget
- Must beat approved threshold or stay disabled
- semantic_retrieval_or_graph_only
- External Embedding Provider Gate And Eval
- project_graph_external_embedding_governance_prerequisite_present
- project_graph_external_embedding_redaction_cache_budget_present
- project_graph_external_embedding_threshold_fallback_present
- project_graph_external_embedding_no_live_calls_present
- provider_call_allowed
- external_call_performed
- T10-LIVE-M13..M14
- project_graph_reranker_provider.py
- project_graph_hybrid_retrieval.py
- reranker_provider.py
- hybrid_retrieval.py
- project_graph_external_reranker_provider_gate_present
- project_graph_hybrid_retrieval_pipeline_present
- Precision/MRR improves or fallback remains active
- source-backed, bounded and explainable
- Cross-Encoder Reranker And Hybrid Retrieval
- project_graph_external_reranker_governance_prerequisite_present
- project_graph_external_reranker_redaction_cache_budget_present
- project_graph_external_reranker_eval_baseline_present
- project_graph_external_reranker_threshold_fallback_present
- project_graph_external_reranker_no_live_calls_present
- project_graph_hybrid_retrieval_explainable_fusion_present
- project_graph_hybrid_retrieval_fallback_present
- project_graph_hybrid_retrieval_no_canonical_mutation_present
- No live provider calls
- T10-LIVE-M15..M16
- project_graph_llm_proposal_provider.py
- llm_proposal_provider.py
- llm-proposal-eval.json
- project_graph_live_llm_proposal_provider_gate_present
- project_graph_live_llm_proposal_safety_eval_present
- proposal-only, never canonical fact
- hallucination, privacy, grounding and stale-context tests
- incident_blocked
- local_llm_proposals_or_semantic_retrieval_or_graph_only
- Live LLM Proposal Adapter And Safety Eval
- project_graph_live_llm_proposal_provider_gate
- external_llm
- llm_proposal_safety_eval
- project_graph_live_llm_proposal_governance_prerequisite_present
- project_graph_live_llm_proposal_prompt_schema_present
- project_graph_live_llm_proposal_redaction_cache_budget_present
- project_graph_live_llm_proposal_threshold_fallback_present
- project_graph_live_llm_proposal_incident_path_present
- project_graph_live_llm_proposal_no_live_calls_present
- project_graph_live_llm_proposal_no_canonical_mutation_present
- T10-LIVE-M17..M18
- project_graph_review_ledger.py
- graph-review-ledger.json
- proposal-diff.json
- project_graph_human_review_ledger_present
- project_graph_proposal_diff_preview_present
- No accepted proposal without owner decision
- Accept, reject or accepted_gap decisions with evidence refs
- Human can inspect before mutation
- proposal-only until Batch 30 dry-run mutation
- Human Review Ledger And Proposal Diff Preview
- project_graph_human_review_ledger
- project_graph_proposal_diff_preview
- human_review_ledger
- proposal_diff_preview
- accepted
- rejected
- accepted_gap
- project_graph_human_review_ledger_governance_prerequisite_present
- project_graph_human_review_ledger_owner_decision_required_present
- project_graph_human_review_ledger_evidence_refs_present
- project_graph_human_review_accepted_gap_present
- project_graph_proposal_diff_inspectable_changes_present
- project_graph_proposal_diff_no_canonical_mutation_present
- project_graph_human_review_ledger_no_live_calls_present
- T10-LIVE-M19..M22
- project_graph_canonical_mutation.py
- canonical_graph_mutation.py
- graph_rollback.py
- mutation_plan.json
- graph-mutation-journal.jsonl
- project_graph_canonical_mutation_dry_run_plan_present
- project_graph_rollback_previous_digest_restore_present
- No mutation without dry-run plan
- Every mutation has rollback patch
- Only accepted proposals mutate graph
- Rollback restores previous graph digest
- accepted_gap remains non-mutating
- Canonical Graph Mutation, Journal And Rollback Engine
- project_graph_canonical_mutation_plan
- project_graph_mutation_journal
- project_graph_rollback_proof
- canonical_mutation_dry_run
- mutation_journal
- project_graph_canonical_mutation_governance_prerequisite_present
- project_graph_canonical_mutation_conflict_checks_present
- project_graph_mutation_journal_append_only_present
- project_graph_mutation_journal_rollback_patch_present
- project_graph_canonical_mutation_only_accepted_proposals_present
- project_graph_canonical_mutation_apply_digest_present
- project_graph_canonical_mutation_no_live_calls_present
- T10-LIVE-M23..M26
- project_graph_live_audit.py
- audit-log.jsonl
- runtime-observability.json
- agent-skill-handoff.json
- project_graph_live_audit_log_present
- project_graph_live_audit_no_live_calls_present
- security-privacy.json
- Audit Logging, Security/Privacy Tests, Observability And Agent/Skill Routing
- project_graph_live_audit_log
- project_graph_live_security_privacy_tests
- project_graph_runtime_observability
- project_graph_agent_skill_handoff_routing
- batch31_audit_security_observability_agent_skill_routing
- security_privacy_tests
- runtime_observability
- agent_skill_handoff_routing
- redacted append-only audit event
- project_graph_live_audit_governance_prerequisite_present
- project_graph_live_audit_event_coverage_present
- project_graph_live_audit_redaction_append_only_present
- project_graph_live_security_privacy_tests_present
- project_graph_live_security_privacy_negative_cases_blocked_present
- project_graph_live_runtime_observability_present
- project_graph_live_runtime_observability_degraded_mode_visible_present
- project_graph_live_agent_skill_handoff_routing_present
- project_graph_live_agent_skill_handoff_stop_conditions_present
- project_graph_live_audit_operability_stage_disable_present
- verification evidence
- stop conditions
- T10-LIVE-M27..M31
- project_graph_real_testing.py
- real-testing-readiness.json
- pilot-harness.json
- codex-surface-smoke.json
- real-testing-pilot-matrix.json
- project_graph_real_testing_readiness_present
- project_graph_real_testing_stage_disable_present
- real-testing-targets.json
- Real Testing Readiness, Target Consent, Pilot Harness And Codex Surface Smoke
- project_graph_real_testing_readiness
- project_graph_real_testing_targets
- project_graph_pilot_harness
- project_graph_codex_surface_smoke
- project_graph_real_testing_pilot_matrix
- batch32_real_testing_readiness_target_consent_pilot_harness_codex_surface_smoke
- real_testing_readiness
- pilot_harness
- codex_surface_smoke
- use_case_pilot_matrix
- dry-run pilot harness
- project_graph_real_testing_target_consent_present
- project_graph_real_testing_pilot_harness_present
- project_graph_real_testing_codex_surface_smoke_present
- project_graph_real_testing_use_case_pilot_matrix_present
- project_graph_real_testing_no_hidden_track10_gates_present
- project_graph_real_testing_no_unapproved_actions_present
- T10-LIVE-M32..M34
- project_graph_runtime_qa.py
- runtime-browser-qa.json
- performance-budget.json
- stabilization-ledger.json
- project_graph_runtime_browser_qa_present
- project_graph_performance_budget_threshold_fallback_present
- project_graph_stabilization_no_open_p0_p1_present
- project_graph_runtime_qa_stage_disable_present
- browser smoke
- console/network checks
- mobile overflow
- generated-view labels
- source-boundary labels
- Runtime Browser QA, Performance And Stabilization
- project-code-graph-runtime-browser-qa.json
- project-code-graph-performance-budget.json
- project-code-graph-stabilization-ledger.json
- project_graph_runtime_browser_qa
- project_graph_performance_budget
- project_graph_stabilization_ledger
- batch33_runtime_browser_qa_performance_stabilization
- runtime_browser_qa
- project_graph_runtime_browser_qa_console_network_checks_present
- project_graph_runtime_browser_qa_mobile_overflow_labels_present
- project_graph_performance_budget_present
- project_graph_stabilization_ledger_present
- project_graph_runtime_qa_no_unapproved_actions_present
- T10-LIVE-M35..M36
- Batch 34 Detailed Task Matrix
- B34-DOC-M01
- B34-DOC-M15
- docs/product-agent-os/project-code-graph.md
- docs/product-agent-os/live-runtime-governance.md
- docs/product-agent-os/approval-bound-real-testing.md
- docs/product-agent-os/agent-skill-modernization-loop.md
- docs/product-agent-os/cli-reference.md
- docs/product-agent-os/artifact-contracts.md
- docs/product-agent-os/packaging-and-closure.md
- project_graph_sanitization.py
- docs/product-agent/product-agent-os-plugin-spec.md
- python -m mkdocs build --strict
- site/
- docs-maintainer plugin-cache gap
- Mermaid external asset gap
- no provider/live external model/API calls
- B34-DOC-M01..M15
- project-authored docs pages
- `site/` rebuild
- project-code-graph.md
- live-runtime-governance.md
- agent-skill-modernization-loop.md
- cli-reference.md
- artifact-contracts.md
- packaging-and-closure.md
- product-agent/product-agent-os-plugin-spec.md
- product-agent-os/project-code-graph.md
- product-agent-os/live-runtime-governance.md
- product-agent-os/approval-bound-real-testing.md
- product-agent-os/agent-skill-modernization-loop.md
- product-agent-os/cli-reference.md
- product-agent-os/artifact-contracts.md
- product-agent-os/packaging-and-closure.md
- Generated `site/` pages are review output and not source of truth
- no git staging/commit/push/PR
- accepted Mermaid external asset gap
- status: compatible
- plugin publication
- external writes
- hook activation
- provider/live external model/API calls
- git stage/commit/push/PR
- T10-LIVE-M37..M41
- approved_local_runtime_launch
- actual_browser_automation_smoke
- approved_provider_api_pilot
- approved_canonical_mutation_pilot
- explicit_git_release_pr_action
- checked-in `docs-maintainer` presence
- installed-cache `docs-maintainer` absence
- Batch 35 approval packet draft for `T10-LIVE-M37..M41`
- B34-PROD-M16
- docs/superpowers/
- root control-plane
- public_forbidden_terms
- docs/diagrams/index.md
- docs/runtime/overview.md
- docs/agent-systems/subagents-skills.md
- docs/playbooks/docs-update.md
- B34-PROD-M16..M18
- public documentation boundary
- internal evidence inventory
- proposed presentation IA
- public-docs forbidden-term policy
- cleanup_pending
- public_ready
- Batch 34C RU/EN localization
- Codex App
- subagents
- `AGENTS.md`
- B34-PROD-M19..M23
- internal ledger language removed
- internal ledger language removed from public-ready pages
- mkdocs-static-i18n
- B34-I18N-M24
- RU default at site root
- fallback_to_default: false
- reconfigure_search: false
- localized_page_parity
- B34-I18N-M24..M30
- EN under `/en/`
- B34-QA-M31
- localized_nav_coverage
- static_html_language_switcher_evidence
- regular site/ rebuild evidence
- md-select
- /en/
- B34-QA-M31..M33
- en/index.html
- before
- default
- does
- each
- have
- only
- path
- runs
- starts
- support
- supports
- that
- this
- through
- under
- used
- validate
- validates
- when
- where
- without
- writes
- B34E-I18N-M45
- done_through_m45
- full_site_ru_quality_sweep
- ru_source_forbidden_english_phrase_hits: 0
- B34E-I18N-M46
- done_through_m46
- full_site_language_switcher_parity
- static_language_switcher_pairs_checked: 121
- english_original_pages_total: 7
- language_switcher_pair_failures: 0
- file_url_escape_failures: 0
- B34E-I18N-M47
- done_through_m47
- full_site_search_sitemap_parity
- search_index_ru_pages_present: 121
- search_index_en_pages_present: 121
- sitemap_ru_pages_present: 121
- sitemap_en_pages_present: 121
- search_index_ru_fallback_pollution: 0
- sitemap_ru_fallback_pollution: 0
- B34E-I18N-M48..M49
- search_index.json
- sitemap.xml
- B34E-I18N-M48
- done_through_m48
- done_through_m49
- full_site_i18n_closure
- full_site_i18n_final_evidence
- strict_mkdocs_final_closure_exit_code: 0
- docs_ru_pages_total: 128
- localized_ru_pages_total: 121
- existing_en_siblings: 121
- missing_localized_en_siblings: 0
- rendered_ru_pages_checked: 121
- rendered_en_pages_checked: 121
- en_source_cyrillic_hits: 0
- B34E-I18N-M34..M37
- B34E-I18N-M38..M43
- B34E-I18N-M44
- full_site_en_nav_configured
- full_site_en_siblings_created
- full_site_en_editorial_quality_sweep
- no remaining Batch 34E gates
- full-site bilingual documentation
- full_site_i18n_inventory
- full_site_i18n_red_gate
- initial_m35_existing_en_siblings: 37
- initial_m35_missing_en_siblings: 90
- expected_red_full_site_i18n_parity
- sources/registry.md
- product-agent-os/index.md
- methodologies/api-integrations.md
- methodologies/backend.md
- methodologies/database-data.md
- sources/product-agent-os-batch34-packaging-install-smoke.md
- sources/product-agent-os-batch34a-public-docs-boundary.md
- sources/product-agent-os-batch34b-public-copy-rewrite.md
- sources/product-agent-os-batch34c-i18n-localization.md
- sources/product-agent-os-batch34d-product-docs-qa-closure.md
- sources/product-agent-os-batch35-approval-packet-draft.md
- sources/product-agent-os-pre-track-8-implementation-inventory.md
- sources/product-agent-os-track-10-backlog.md
- sources/product-agent-os-track-8-detailed-backlog.md
- sources/product-agent-os-track-9-backlog.md
- superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md
- done_through_m44
- T10-LIVE-M37
- T10-LIVE-M38
- T10-LIVE-M39
- T10-LIVE-M40
- batch35_approval_bound_real_testing_execution
- live-server-run-evidence.json
- browser-automation-smoke.json
- provider-call-evidence.json
- provider-eval-report.json
- canonical-mutation-run.json
- rollback-proof.json
- git-release-pr-evidence.md
- desktop.png
- mobile.png
- short-lived local server bound to `127.0.0.1`
- desktop/mobile screenshots
- console_errors: 0
- network_failures: 0
- mobile_overflow: false
- OPENAI_API_KEY used: false
- direct API call from workspace shell: false
- stage_root_only
- rollback_restores_previous_graph_digest: true
- missing_required_fields
- performs no canonical graph mutation
- performs no git stage/commit/push/PR
- blocked_pending_explicit_git_release_fields
- 127.0.0.1
- redaction.ok: true
- provider_secret_stored: false
- operation_count: 1
- journal_entry_count: 1
- T10-CG-V2-M39..M44
- project_graph_backend.py
- project_graph_local_backend_gate_present
- disabled by default
- generated local file-store
- server mode is disabled by default
- no production server
- Task 25 Batch 20
- T10-CG-V2-M45..M51
- project_graph_semantic.py
- project_graph_semantic_retrieval_gate_present
- embeddings cache metadata
- semantic query packets
- present_unverified orientation evidence
- no canonical graph edge rewrites
- Task 25 Batch 21
- T10-CG-V2-M31..M32
- focused/full verification
- Task 25 Batch 18
- T10-CG-V2-M33..M38
- project_graph_index.py
- project_graph_static_search_index_present
- explicit user approval
- generated, cache-bound and not source of truth
- no live database/server, LLM, embedding or cross-encoder
- Task 25 Batch 19
- .codex/product-agent-os/project-code-graph-search-index.json
- graph artifact only
- docs/product-agent-os/scenarios.md
- docs/product-agent-os/behavioral-evals.md
- docs/product-agent-os/codex-compatibility.md
- plugins/product-agent-os/scripts/product_agent_os/discovery.py
- plugins/product-agent-os/scripts/run_transcript_eval.py
- T8-D
- T9-D7
- backend_contract_present
- runtime/failure/observability/security/rollback evidence
- Backend methodology
- T9-D8
- api_integrations_contract_present
- T9-D9
- database_data_contract_present
- agent-task-packet.md
- automation-candidate.md
- methodology_synthesis
- codex_compatibility
- Task 22 final documentation sync closure
- docs/product-agent-os/methodology-intelligence.md
- plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py
- plugins/product-agent-os/scripts/codex_runtime_runner/contracts.py
- OpenAPI v3.2.0 freshness claim
- doubt-verification-loop.md
- product-agent-os-batch40-doubt-verifier-source-transfer.md
- playbook
- mkdocs
- check_docs
- runlog
- index.md
- technical.md
- development-standards.md
- architecture.md
- overview.md
- product-agent-os-plugin-spec.md
- automations-github.md
- subagents-skills.md
- docs-update.md
- artifact-gallery.en.md
- real-project-pilot.md
- real-project-pilot.en.md
- `reviewed_gap_recorded`
- verification gates
- behavioral-workflows.json
- forbidden behavior
- fixture eval
- transcript/session eval runner
- evidence-before-completion
- residual risk
- .codex-plugin/plugin.json
- staged hooks
- orientation evidence
- data classification
- scan_project_code_graph.py
- --build-index
- --build-backend
- --build-llm-proposals
- product-agent-os/
- index.html
- B34E-I18N-M
- staged infrastructure
- source of truth
- Codex runtime runner
- renderer_file_count
- run_transcript_eval.py
- staged proposal
- transcript/session replay
- staged artifact boundary
- playbooks
- completion-skeptic
- doubt_verification_packet
- B40-S4 source-transfer packet
- Chain-of-Verification
- CRITIC
- Self-Refine
- intrinsic self-correction limitations
- evidence ledger
- tripwire
- doubt_verification_packet_v1
- generated-view boundary
- owner review
- candidate-only
- eval cases
- Doubt / verifier loop
- playbooks/doubt-verification-loop.md
- sources/product-agent-os-batch40-doubt-verifier-source-transfer.md
- docs/playbooks/doubt-verification-loop.md
- docs/sources/product-agent-os-batch40-doubt-verifier-source-transfer.md
- generated `site/` is not source of truth
- completion_skeptic_manual_pilot_ledger
- completion_skeptic_scorecard_calibration
- completion_skeptic_go_no_go_closure
- manual_only
- no_unapproved_actions
- rollback_disable_path
- docs/sources/product-agent-os-batch40-doubt-verifier-pilot-closure.md
- generated `site/` was rebuilt for S5
- B40-DVL-M22
- product-agent
- diagrams
- agent-systems
- B38-S3
- B38-PROD-M06..M09
- B38-S4
- B38-PROD-M10..M11
- requirements.txt
- technical.en.md
- artifact-contracts.en.md
- automations-github.en.md
- docs/product-agent-os/
- .en.md
- index.en.md
- location
- Product-Agent OS Batch 39 M20 first-run analysis artifact contract
- B39-FRIA-M20.9
- docs/product-agent-os/artifact-contracts.md
- docs/product-agent-os/cli-reference.md
- plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py
- plugins/product-agent-os/scripts/product_agent_os/analysis_artifact_renderer.py
- Product-Agent OS Batch 39 S4/S5 hardening and closure evidence
- B39-S4-REMAINING-GATES-A01
- B39-S5-CLOSURE-A01
- docs/superpowers/specs/batch39-s4-remaining-gates-summary.json
- docs/superpowers/specs/batch39-s4-closure-readiness-matrix.json
- docs/superpowers/specs/batch39-s5-closure-summary.json
- docs/superpowers/specs/batch39-s5-go-no-go-decision-packet.json
- docs/superpowers/specs/batch39-s5-no-unapproved-actions-proof.json
- docs/superpowers/specs/batch39-s5-owner-feedback-test-plan.json
- release no_go
- owner-feedback conditional_go
- runtime-browser approval_required
- manual_only_not_promoted
- Product-Agent OS Batch 41 first-run orchestration S1-S6 evidence
- batch41_first_run_orchestration_s1_s6
- docs/superpowers/specs/batch41-s1-command-contract-summary.json
- docs/superpowers/specs/batch41-s2-script-matrix-summary.json
- docs/superpowers/specs/batch41-s3-project-analysis-summary.json
- docs/superpowers/specs/batch41-s4-html-artifact-summary.json
- docs/superpowers/specs/batch41-s5-guided-questions-summary.json
- docs/superpowers/specs/batch41-s6-closure-summary.json
- plugins/product-agent-os/scripts/run_first_project_analysis.py
- plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py
- first-run welcome/help now discloses Product-Agent OS purpose and Self-Learning Loop as manual-first, project-scoped and not activated by first-run help
- local/read-only/staged evidence only
- Product-Agent OS Batch 41 cockpit, architecture dossier and HTML modernization S7-S9 evidence
- batch41_cockpit_architecture_html_modernization_s7_s9
- docs/superpowers/specs/batch41-s7-m31-m33-cockpit-foundation-summary.json
- docs/superpowers/specs/batch41-s8-m47-neural-flow-before-after-summary.json
- docs/superpowers/specs/batch41-s9-html-modernization-summary.json
- docs/superpowers/specs/batch41-s9-m57-neural-flow-comparison.json
- plugins/product-agent-os/scripts/product_agent_os/analysis_artifact_renderer.py
- tests/product_agent_os/test_batch41_first_run_automation.py
- generated artifacts are orientation_only_not_proof
- Product-Agent OS Batch 42 instruction/tool-use compliance planning matrix
- batch42_instruction_tool_use_compliance_matrix_v1
- docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json
- planned_only_not_implementation_evidence
- Product-Agent OS Track 11 documentation refresh G0 governance packet
- documentation_refresh_G0-A01
- docs/superpowers/specs/documentation-refresh-g0-governance-summary.json
- closed_g0_scope_only
- Product-Agent OS Track 11 G1 source/site parity packet
- documentation_refresh_G1-A01
- docs/superpowers/specs/documentation-refresh-g1-source-site-parity-summary.json
- source records, registry and generated-site parity
- pre-G1 generated `site/` stale orientation evidence
- 2026-06-20 strict MkDocs was blocked in default active Python: No module named mkdocs; historical dependency targets found at C:\tmp\codex_docs_mkdocs and tmp\mkdocs_deps_b40s4 but they were not usable as a runnable MkDocs module from that process
- no browser automation, provider/API call, target mutation, publication, git action, cache refresh or automation activation
- Product-Agent OS Track 11 G1.1 project-local documentation toolchain planning matrix
- documentation_refresh_G1_1-PLANNING-A01
- documentation_refresh_G1_1-SYSTEM-FILES-A01
- documentation_refresh_G1_1-DOC-M34-A01
- documentation_refresh_G1_1-DOC-M35-PREFLIGHT-A01
- documentation_refresh_G1_1-DOC-M35-INSTALL-A01
- documentation_refresh_G1_1-DOC-M36-NODE-A01
- documentation_refresh_G1_1-DOC-M37-VALE-A01
- documentation_refresh_G1_1-DOC-M38-LINK-SECRET-A01
- documentation_refresh_G1_1-DOC-M39-MERMAID-A01
- documentation_refresh_G1_1-DOC-M40-AUDIT-SBOM-A01
- documentation_refresh_G1_1-DOC-M41-DEFERRED-PLATFORMS-A01
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m34-folder-contract-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-preflight-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m35-install-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m36-node-tooling-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m37-vale-language-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m38-link-secret-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m39-mermaid-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m40-dependency-audit-summary.json
- docs/superpowers/specs/documentation-refresh-g1-1-doc-m41-deferred-platform-triggers-summary.json
- Product-Agent OS project-local lifecycle hook activation
- product_agent_os_LIFECYCLE-HOOKS-A01
- docs/superpowers/specs/product-agent-os-lifecycle-hooks-local-activation-summary.json
- docs/superpowers/specs/product-agent-os-lifecycle-hooks-full-brief-marker-summary.json
- .codex/hooks.json
- .codex/hooks/hooks.json
- .codex/product-agent-os/lifecycle-state.json
- task_start_brief_v1 full field-list lifecycle marker contract
- ready_for_completion_brief terminal-final contract with no post-Brief tool calls
- read-only PreToolUse fast path, current-patch comment advisory and five-second project hook timeout contract
- Codex hook trust review / fresh-session execution remains unclaimed
- tools/docs_install.ps1
- tools/docs_node_install.ps1
- tools/docs_vale_install.ps1
- tools/docs_link_secret_install.ps1
- tools/docs_mermaid_install.ps1
- tools/docs_dependency_audit.ps1
- .vale.ini
- .gitleaks.toml
- .docs-tools/vale/
- .docs-tools/link-secret/
- .docs-tools/bin/vale.sha256
- .docs-tools/bin/lychee.sha256
- .docs-tools/bin/gitleaks.sha256
- docs/assets/javascripts/vendor/mermaid-10.9.6.min.js
- docs/assets/javascripts/vendor/mermaid-10.9.6.min.js.sha256
- docs/assets/javascripts/vendor/mermaid-10.9.6.LICENSE.txt
- docs/assets/javascripts/vendor/mermaid-10.9.6.package.json
- .docs-tools/node/package.json
- .docs-tools/node/package-lock.json
- DOC-M34..DOC-M41
- Product-Agent OS Track 11 G2 first-run cockpit and artifact docs packet
- documentation_refresh_G2-A01
- docs/superpowers/specs/documentation-refresh-g2-first-run-cockpit-artifact-docs-summary.json
- docs/product-agent-os/first-run-architecture-cockpit.md
- docs/product-agent-os/first-run-architecture-cockpit.en.md
- docs/product-agent-os/artifact-contracts.md
- docs/product-agent-os/artifact-gallery.md
- docs/product-agent-os/project-code-graph.md
- docs/product-agent-os/cli-reference.md
- docs/product-agent-os/technical.md
- implemented_source_docs_no_site_rebuild
- DOC_M25_PENDING_SITE_PAGES
- root `site` freshness deferred to final DOC-M25
- browser/runtime/Cosmos.gl/WebGL/root site freshness unsupported in G2
- Product-Agent OS Track 11 G3 diagram atlas and architecture maps packet
- documentation_refresh_G3-A01
- docs/superpowers/specs/documentation-refresh-g3-diagram-atlas-architecture-maps-summary.json
- docs/diagrams/source-generated-trust-boundary.md
- docs/diagrams/first-run-cockpit-architecture.md
- docs/diagrams/evidence-risk-lifecycle.md
- docs/diagrams/skill-exposure-and-invocation.md
- docs/diagrams/architecture-intelligence-diagram-atlas.md
- implemented_source_docs_no_site_rebuild
- DOC_M25_PENDING_SITE_PAGES
- root `site` freshness deferred to final DOC-M25
- browser proof approval_required, Cosmos.gl/WebGL runtime proof unsupported and Structurizr DSL deferred/uninstalled in G3
- Product-Agent OS Track 11 G4 operator flows and system behavior docs packet
- documentation_refresh_G4-A01
- docs/superpowers/specs/documentation-refresh-g4-operator-flows-system-behavior-summary.json
- docs/product-agent-os/instruction-tool-use-compliance.md
- docs/product-agent-os/operator-command-matrix.md
- docs/product-agent-os/guided-questions-answer-ledger.md
- docs/product-agent-os/source-cache-session-state.md
- docs/product-agent-os/index.md
- docs/product-agent-os/scenarios.md
- docs/product-agent-os/cli-reference.md
- docs/product-agent-os/methodology-intelligence.md
- implemented_source_docs_no_site_rebuild
- DOC_M25_PENDING_SITE_PAGES
- root `site` freshness deferred to final DOC-M25
- auto-engagement/cache refresh/global config/fresh session proof unsupported in G4
- Product-Agent OS Track 11 G5 evidence quality and final site gate docs packet
- documentation_refresh_G5-A01
- docs/superpowers/specs/documentation-refresh-g5-evidence-quality-site-gate-summary.json
- docs/product-agent-os/generated-artifact-ux-criteria.md
- docs/product-agent-os/graph-intelligence-contract.md
- docs/product-agent-os/privacy-supply-chain-retention.md
- docs/product-agent-os/local-html-interaction-boundary.md
- docs/product-agent-os/residual-follow-up-site-freshness.md
- implemented_source_docs_no_site_rebuild
- DOC_M25_PENDING_SITE_PAGES
- root `site` freshness deferred to final DOC-M25
- browser proof, broad scans, dependency remediation and raw report retention approval_required in G5
- .venv-docs/
- .docs-tools/node/
- .docs-tools/bin/
- .docs-tools/reports/
- docs/assets/javascripts/vendor/
- mkdocs-material, mkdocs-static-i18n, markdownlint-cli2, Prettier, Redocly CLI, Vale, lychee, gitleaks, Mermaid
- Docusaurus, Storybook and Structurizr DSL deferred until trigger evidence exists
- implemented_contract_only_no_install for DOC-M34; DOC-M35 installed_smoke_passed in .venv-docs with strict smoke output under .docs-tools/reports; DOC-M36 installed_smoke_passed in .docs-tools/node with scoped README smoke; DOC-M37 installed_advisory_smoke_passed with local Vale rules/checksum; DOC-M38 installed_scoped_smoke_passed with local lychee/gitleaks checksums and scoped fixture smokes; DOC-M39 installed_offline_vendor_smoke_passed with local Mermaid checksum/license/static MkDocs smoke; DOC-M40 implemented_audit_sbom_governance_current_findings_recorded with local Python inventory, Node CycloneDX SBOM generation and 3 moderate / 0 high / 0 critical npm audit findings; DOC-M41 implemented_deferred_platform_trigger_governance_no_install_no_site_rebuild
- root control-plane system files synced for G1.1 implementation route
- Product-Agent OS Track 11 DOC-M25 root site freshness packet
- documentation_refresh_DOC-M25-A01
- documentation_refresh_DOC-M25-A02
- docs/superpowers/specs/documentation-refresh-doc-m25-site-freshness-summary.json
- tools/fix_site_i18n_links.ps1
- site/
- site/search/search_index.json
- site/sitemap.xml
- implemented_root_site_search_sitemap_freshness
- former DOC_M25_PENDING_SITE_PAGES rendered in RU/EN HTML, search index and sitemap after owner-approved root MkDocs build
- 2026-07-07 refresh includes Batch 45 T15 source docs/control-plane markers in generated root site/search/sitemap after local MkDocs build and i18n link repair
- browser proof, broad scans, dependency remediation, raw report retention, publication, release, deploy and git actions remain out of scope
- Product-Agent OS Track 11 Batch 44 Self-Learning Loop activation, Product-Agent OS project scope, agent/skill metrics and HTML progress matrix; `B44-S0` research/gap/scope detector evidence, `B44-S1` state/due-check/trigger UX evidence and `B44-S2` manual runner/progress artifact evidence implemented, remaining activation slices planned-only
- batch44_self_learning_loop_S0_S1_implemented_rest_planned
- docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md
- arXiv research intake: 2507.21046, 2508.07407, 2507.19457, 2510.04618, 2510.09801, 2603.20939, 2510.09720, 2507.05257, 2511.20857, 2603.03329, 2510.26852, 2510.23595, 2506.15841, 2512.16301, 2602.12670, 2605.05726, 2603.00718, 2605.18693, 2603.15401, 2512.24565, 2507.21504, 2605.20251, 2511.13998, 2508.03680, 2602.12430, 2602.20867, 2602.20156, 2604.15415
- expanded metrics intake: Product-Agent OS-only project scope, owner feedback import filter, paired skill utility, skill retrieval, tool composition, process-control, adversarial skill safety, satisfaction, memory quality, resumable progress state and project-local HTML progress artifact
- planned_only_not_implementation_evidence
- no active scheduler, hook activation, automation activation, global user-session analysis, hidden telemetry, real private session ingestion, provider/model call, cache refresh, global config write, target mutation, project HTML proof claim, git action, release, deploy or publish action
- Product-Agent OS Track 11 Batch 44 Self-Learning Loop docs/contracts/closure packet
- B44-SLL-M15-M16-A01
- docs/superpowers/specs/batch44-self-learning-loop-docs-contracts-closure-summary.json
- docs/product-agent-os/agent-skill-modernization-loop.md
- docs/product-agent-os/artifact-contracts.md
- docs/product-agent-os/behavioral-evals.md
- self-learning-automation-candidate.md
- self_learning_docs_contracts_closure_v1
- batch44_self_learning_loop_S0_S1_S2_S3_S4_S5_S6_implemented_rest_planned
- automation promotion remains candidate_only with minimum_manual_successful_runs: 3 and active schedule remains not_created
- no real Codex App session export import, hidden telemetry, raw transcript, provider/model/live eval call, target mutation, active automation, git/release/deploy/publish, external write or auto-apply
- Product-Agent OS Track 11 Batch 45 professional code authoring S0 synthesis and activation policy packet
- B45-S0-M01-M20-A01
- docs/superpowers/specs/batch45-professional-code-authoring-summary.json
- docs/superpowers/specs/batch45-professional-code-activation-map.json
- docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md
- B45-PCA-M01 and B45-PCA-M20 implemented as docs_contract_ready
- remaining B45-PCA-M02..M19 and B45-PCA-M21..M23 planned, with B45-PCA-M14 reserved for final closure
- no template/eval/agent profile/runtime-route/HTML/hook activation/provider/browser/cache/target/git/release/deploy/publish behavior proved by S0
- Product-Agent OS Track 11 Batch 45 professional code authoring S1 artifact/workflow contract packet
- B45-S1-M02-M04-A01
- docs/superpowers/specs/batch45-professional-code-s1-artifact-workflow-summary.json
- plugins/product-agent-os/assets/templates/workflows/coding-standards.md
- plugins/product-agent-os/assets/templates/artifact-templates/coding-standard-checklist.md
- plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md
- plugins/product-agent-os/scripts/product_agent_os/templates.py
- tests/product_agent_os/test_batch45_coding_standards.py
- B45-PCA-M02, B45-PCA-M03 and B45-PCA-M04 implemented as docs_contract_ready template/workflow/handoff contracts
- remaining B45-PCA-M05..M19 and B45-PCA-M21..M23 planned, with B45-PCA-M14 reserved for final closure
- no eval enforcement, public docs page, runtime route, HTML visibility, hook activation/update, automation, provider/browser/cache/target/git/release/deploy/publish behavior proved by S1
- Product-Agent OS Track 11 Batch 45 professional code authoring S2 existing workflow, agent and skill retrofit packet
- B45-S2-M05-M09-M15-M17-A01
- docs/superpowers/specs/batch45-professional-code-s2-existing-workflow-retrofit-summary.json
- docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md
- plugins/product-agent-os/assets/templates/workflows/development-standards.md
- plugins/product-agent-os/assets/templates/workflows/build-slice.md
- plugins/product-agent-os/assets/templates/workflows/review-slice.md
- plugins/product-agent-os/assets/templates/workflows/legacy-onboarding.md
- plugins/product-agent-os/assets/templates/workflows/bug-rescue.md
- plugins/product-agent-os/assets/templates/workflows/api-migration.md
- plugins/product-agent-os/assets/templates/workflows/data-migration.md
- plugins/product-agent-os/assets/templates/workflows/security-sensitive-change.md
- plugins/product-agent-os/assets/templates/workflows/ci-stabilization.md
- plugins/product-agent-os/assets/templates/workflows/desktop-local-first.md
- plugins/product-agent-os/assets/templates/workflows/complex-system-acceleration.md
- plugins/product-agent-os/assets/templates/artifact-templates/api-style-guide.md
- plugins/product-agent-os/assets/templates/artifact-templates/supply-chain-review.md
- plugins/product-agent-os/assets/templates/artifact-templates/quality-strategy.md
- plugins/product-agent-os/assets/templates/artifact-templates/plan-quality-check.md
- plugins/product-agent-os/assets/templates/agents/builder.toml
- plugins/product-agent-os/assets/templates/agents/reviewer.toml
- plugins/product-agent-os/assets/templates/agents/architect.toml
- plugins/product-agent-os/assets/templates/agents/tester.toml
- plugins/product-agent-os/assets/templates/artifact-templates/subagent-context-packet.md
- plugins/product-agent-os/assets/templates/artifact-templates/subagent-result-packet.md
- plugins/product-agent-os/assets/templates/evals/handoff-completeness.json
- plugins/product-agent-os/skills/implementation-planner/SKILL.md
- plugins/product-agent-os/skills/agent-team-designer/SKILL.md
- plugins/product-agent-os/skills/docs-maintainer/SKILL.md
- docs/product-agent-os/development-standards.md and .en.md
- docs/playbooks/code-review.md and .en.md
- tests/product_agent_os/test_batch45_s2_existing_workflow_retrofit.py
- B45-PCA-M05, B45-PCA-M06, B45-PCA-M07, B45-PCA-M08, B45-PCA-M09, B45-PCA-M15 and B45-PCA-M17 implemented as docs_contract_ready retrofit contracts
- remaining B45-PCA-M10..M13, B45-PCA-M16, B45-PCA-M18..M19 and B45-PCA-M21..M23 planned, with B45-PCA-M14 reserved for final closure
- no dedicated public coding-standards page, eval enforcement, runtime route, HTML visibility, hook activation/update, automation, provider/browser/cache/target/git/release/deploy/publish behavior proved by S2
- Product-Agent OS Track 11 Batch 45 professional code authoring S3 evals, readiness, route, HTML and hook-governance visibility packet
- B45-S3-M10-M11-M16-M18-M21-M22-A01
- docs/superpowers/specs/batch45-professional-code-s3-evals-visibility-summary.json
- docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md
- plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json
- plugins/product-agent-os/assets/templates/evals/agent-context-contract.json
- .codex/evals/agent-context-contract.json
- plugins/product-agent-os/assets/templates/evals/project-readiness.json
- plugins/product-agent-os/assets/methodology/methodology-catalog.json
- plugins/product-agent-os/assets/templates/artifact-templates/acceptance-scenarios.md
- plugins/product-agent-os/assets/templates/artifact-templates/test-eval-matrix.md
- plugins/product-agent-os/assets/templates/artifact-templates/behavioral-eval-case.md
- plugins/product-agent-os/assets/templates/artifact-templates/codex-compatibility-report.md
- plugins/product-agent-os/assets/templates/artifact-templates/hook-governance.md
- plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py
- plugins/product-agent-os/assets/templates/hooks/post_tool_use_evidence.py
- plugins/product-agent-os/assets/templates/hooks/stop_runlog_reminder.py
- plugins/product-agent-os/scripts/product_agent_os/behavioral_evals.py
- plugins/product-agent-os/scripts/product_agent_os/discovery.py
- plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py
- plugins/product-agent-os/scripts/product_agent_os/analysis_artifact_renderer.py
- plugins/product-agent-os/scripts/product_agent_os/status_dashboard.py
- plugins/product-agent-os/scripts/codex_runtime_runner/routes.py
- plugins/product-agent-os/scripts/run_fixture_eval.py
- .codex/workflows/coding-standards.md
- .codex/artifact-templates/coding-standard-checklist.md
- .codex/workflows/build-slice.md
- .codex/workflows/review-slice.md
- .codex/agents/builder.toml
- .codex/agents/reviewer.toml
- .codex/agents/architect.toml
- tests/product_agent_os/test_batch45_s3_professional_code_authoring.py
- tests/product_agent_os/test_behavioral_workflow_evals.py
- tests/product_agent_os/test_discovery.py
- tests/product_agent_os/test_status_dashboard.py
- tests/product_agent_os/test_infrastructure_templates.py
- tests/product_agent_os/test_fixture_eval_runner.py
- B45-PCA-M10, B45-PCA-M11, B45-PCA-M16, B45-PCA-M18, B45-PCA-M21 and B45-PCA-M22 implemented as docs_contract_ready eval/visibility/governance contracts
- remaining B45-PCA-M12, B45-PCA-M13, B45-PCA-M19 and B45-PCA-M23 planned, with B45-PCA-M14 reserved for final closure
- no dedicated public coding-standards page, live runtime behavior, hook activation/update, automation, provider/browser/cache/target/git/release/deploy/publish behavior proved by S3
- Product-Agent OS Track 11 Batch 45 S6 advisory validation, live behavior eval and promotion decision packet
- B45-PCA-M24-A01; B45-PCA-M24-TUNING-A02; B45-PCA-M25; B45-PCA-M26; B45-PCA-M27
- docs/superpowers/specs/batch45-comment-sufficiency-false-positive-audit.json
- docs/superpowers/specs/batch45-comment-sufficiency-tuning-comparison.json
- docs/superpowers/specs/batch45-comment-sufficiency-advisory-wiring-summary.json
- docs/superpowers/specs/batch45-agent-behavior-eval-plan.json
- docs/superpowers/specs/batch45-agent-behavior-eval-results.json
- docs/superpowers/specs/batch45-comment-policy-promotion-decision.json
- M26 live no-go: baseline 4.22, treatment 3.88, 15/16 completed, warnings 29 -> 15, reviewer no_go
- M27 decision keeps M25 advisory-only and rejects stronger advisory, CI and blocker promotion; no browser/target/git/release/deploy proof
- Product-Agent OS Track 11 Batch 45 M37 review remediation/docs-control-plane packet
- B45-PCA-M37; B45-PCA-M37-A01
- docs/superpowers/specs/batch45-review-remediation-summary.json
- .codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md
- .codex/product-agent-os/reviews/batch45/remediation-agent-04-code-repair.md
- M37 implements local advisory hook/validator hardening/docs sync only; M36 remains reserved; promotion remains no_go/advisory-only; no runtime/browser/provider/target/git/release/deploy/automation proof
- Product-Agent OS Track 11 Batch 45 repeat quality/refactor retest Q0-Q2 protocol packet
- B45-RETEST-Q0-Q2; B45-RETEST-Q0-Q2-A01
- docs/superpowers/specs/batch45-quality-retest-protocol.json
- Q0 freezes M26/M27/M35/M37 claim ceilings, Q1 defines 8 fresh held-out task slots plus SOL/MP fixture canaries, and Q2 defines harness/rubric/privacy/approval schema; next local route is Q3 fixture-static; no live/model/runtime/browser/provider/target/git/release/deploy/automation proof
- Product-Agent OS Track 11 Batch 45 repeat quality/refactor retest Q3 fixture-static packet
- B45-RETEST-Q3-FIXTURE-STATIC; B45-RETEST-Q3-FIXTURE-STATIC-A01
- docs/superpowers/specs/batch45-quality-retest-fixture-static-summary.json
- Q3 scanned 37 existing sanitized fixture files, found 14 advisory warnings with blocking=false, keeps continue_investigation_keep_advisory_only_no_go and does not prove live/model/runtime/browser/provider/target/git/release/deploy/automation readiness
- Product-Agent OS Track 11 Batch 45 repeat quality/refactor retest Q4 project-slices-static packet
- B45-RETEST-Q4-PROJECT-SLICES-STATIC; B45-RETEST-Q4-PROJECT-SLICES-STATIC-A01
- docs/superpowers/specs/batch45-quality-retest-project-slices-static-summary.json
- Q4 scanned five existing sanitized SOL/myPartners project slices, found 14 advisory warnings with blocking=false, keeps continue_investigation_keep_advisory_only_no_go and does not prove live/model/runtime/browser/provider/target/git/release/deploy/automation readiness
- Product-Agent OS Track 11 Batch 45 post-Q4 next task queue packet
- B45-POST-Q4-NEXT-TASKS; B45-POST-Q4-NEXT-TASKS-A01
- docs/superpowers/specs/batch45-post-q4-next-tasks.json
- Post-Q4 tasks route targeted static hotspot repair, static delta verification, approval-gated live/model rerun, promotion decision and optional M36 runtime/browser packet while preserving advisory-only/no-go and all approval boundaries
- Product-Agent OS Track 11 Batch 45 post-Q4 T01-T04 execution and approval packet
- B45-POSTQ4-T01-T04; B45-POSTQ4-T01-T04-A01; B45-POSTQ4-T04-A01
- docs/superpowers/specs/batch45-postq4-t01-t04-execution-summary.json
- docs/superpowers/specs/batch45-postq4-live-model-rerun-approval-packet.json
- T01-T03 copied-fixture static repair reduced Q4 advisory warnings 14 -> 0; T04 only stages an approval packet for a future live/model rerun and preserves all no-go/promotion boundaries
- Product-Agent OS Track 11 Batch 45 post-Q4 T05 exact-approved live/model rerun timeout rollup
- B45-POSTQ4-T05-LIVE-MODEL-RERUN; B45-POSTQ4-T05-A01
- docs/superpowers/specs/batch45-postq4-t05-live-model-rerun-results.json
- T05 used exact-approved Codex CLI/OpenAI calls but stopped on baseline timeout after 1 completed primary run and 1 timed-out primary run; 14 primary runs and the reviewer were not run by stop rule, so M26/M35 no-go remains active
- Product-Agent OS Track 11 Batch 44 Self-Learning Loop S7 state initializer, manual pilot, Promptfoo/HALO and staged repair contracts
- B44-S7-SELF-LEARNING-MANUAL-PILOT-A01
- docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json
- docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-feedback.jsonl
- docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-metrics.jsonl
- docs/product-agent-os/self-learning-loop.md
- docs/product-agent-os/artifact-contracts.md
- docs/product-agent-os/behavioral-evals.md
- plugins/product-agent-os/scripts/init_self_learning_state.py
- plugins/product-agent-os/scripts/run_self_learning_loop.py
- plugins/product-agent-os/scripts/check_self_learning_due.py
- plugins/product-agent-os/scripts/export_self_learning_promptfoo.py
- plugins/product-agent-os/scripts/product_agent_os/self_learning_initializer.py
- plugins/product-agent-os/scripts/product_agent_os/self_learning_evals.py
- plugins/product-agent-os/scripts/product_agent_os/self_learning_repair.py
- plugins/product-agent-os/scripts/product_agent_os/self_learning_progress.py
- plugins/product-agent-os/scripts/product_agent_os/self_learning_state.py
- tests/product_agent_os/test_self_learning_extensions.py
- tests/product_agent_os/test_self_learning_state.py
- B44-S7 manual pilot reached ready_for_owner_review using explicit staged state, one redacted feedback row, one metrics row and two review-only candidates
- Promptfoo export staged 8 eval cases and failure taxonomy; HALO-style packet staged 6 local recommendations; no Promptfoo run, HALO service call, provider/model/API call, browser automation, target workspace mutation, active automation, git/release/deploy/publish or auto-apply was performed
```

## Обновление документации GPT-6 — 2026-11-03

Официальные страницы прочитаны через OpenAI Developer Docs для обновления по 20 пунктам. Trust level: official/high; verification status: чтение источника и сопоставление документации, не проверка аккаунта или runtime. Кандидатные роли и migration rubric — проектные предложения. Исторические cards/URL в archive сохранены.

| Source | Findings | Checked at |
| --- | --- | --- |
| [Models / availability](https://learn.chatgpt.com/docs/models) | 3, 4, 12 | 2026-11-03 |
| [API model catalog](https://developers.openai.com/api/docs/models) | 3, 12 | 2026-11-03 |
| [GPT-6 migration / prompting](https://developers.openai.com/api/docs/guides/latest-model) | 4, 12-15 | 2026-11-03 |
| [Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) | 12, 16 | 2026-11-03 |
| [Sol 6.1](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | 12, 16 | 2026-11-03 |
| [Terra 6.1](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | 12, 16 | 2026-11-03 |
| [Luna 6](https://developers.openai.com/api/docs/models/gpt-6-luna) | 12, 16 | 2026-11-03 |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | 1, 2, 9 | 2026-11-03 |
| [Permissions](https://learn.chatgpt.com/docs/permissions) | 1, 7, 8 | 2026-11-03 |
| [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 5, 6, 7 | 2026-11-03 |
| [AGENTS discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 10 | 2026-11-03 |
| [Skills](https://learn.chatgpt.com/docs/build-skills) | 2, 9 | 2026-11-03 |
| [Caching](https://developers.openai.com/api/docs/guides/prompt-caching) | 16 | 2026-11-03 |
| [Async tools](https://developers.openai.com/api/docs/guides/async-tool-calling) | 17 | 2026-11-03 |
| [Steering](https://developers.openai.com/api/docs/guides/steering) | 17 | 2026-11-03 |
| [Reasoning updates](https://developers.openai.com/api/docs/guides/reasoning) | 18 | 2026-11-03 |
| [Compaction](https://developers.openai.com/api/docs/guides/compaction) | 18 | 2026-11-03 |
| [Agent runtimes](https://developers.openai.com/api/docs/guides/agents) | 19 | 2026-11-03 |
| [Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) | 19 | 2026-11-03 |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | 20 | 2026-11-03 |

Canonical mapping: старые Codex models/subagents/security URL могут перенаправляться; это не доказательство массово сломанных ссылок. В измененных действующих руководствах используются прочитанные canonical pages. Неизмененные исторические ссылки сохраняются как датированные evidence, а не как заново проверенные claims. См. [план](../superpowers/plans/2026-11-03-gpt6-documentation-refresh.md) и [матрицу моделей](../codex/models-and-reasoning.md).


## Согласование исполняемых контрактов — 2026-11-03

Официальные контракты повторно проверены: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Permissions](https://learn.chatgpt.com/docs/permissions), [Models](https://learn.chatgpt.com/docs/models), [Migration quickstart](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart). Permissions и MCP задаются в родительской сессии; custom agents могут ограничивать поддерживаемые capabilities. В 15 активных и 8 staged profiles назначены Sol/Terra 6.1 с прежним effort. Валидаторы проверяют политику проекта, не весь каталог поддерживаемых OpenAI моделей. Реальные активация, доступность и качество не доказаны. План и evidence: [техническое продолжение](../superpowers/plans/2026-11-03-gpt6-documentation-refresh.md).


## 2026-11-03 — Согласование lifecycle с Trade

Проектный источник: Trade `AGENTS.md`, Task Start Brief, Completion Ledger, delivery/review workflows и control-plane cases; чтение без изменений, SHA-256 сохранены в owning task group. Актуальный шаблон содержит 13 пунктов ledger; старое описание eleven fields в eval не считается контрактом. PAOS переносит 9 стартовых полей, 13 завершающих пунктов и условную применимость без путей развёртывания Trade. Stop рекомендательный; явная проверка пакета даёт только локальные evidence. Официальные [Hooks](https://learn.chatgpt.com/docs/hooks) описывают Stop continuation и exact-hash trust; изменение исходников не доказывает активацию в новой доверенной сессии. Статус и проверки: `docs/superpowers/specs/gpt6-documentation-refresh-task-group.json`, `lifecycle_parity`.


## 2026-11-03 — Приёмка lifecycle в новой сессии

Источник: разрешённый новый desktop chat и компактные receipts в `docs/superpowers/specs/gpt6-documentation-refresh-task-group.json`, `lifecycle_parity.activation_check`. Наблюдаются полный формат 9/13 и краткий обычный маршрут; строгий ledger validator расходится с синтаксисом ответа. Подтверждена доставка SessionStart/PostToolUse context, но PreToolUse не запретил `functions.exec -> tools.apply_patch` при terminal marker: sentinel создан. Прямой script deny — отдельное synthetic evidence. Итог: activation_failed, runtime-ready не заявляется. [Официальные Hooks](https://learn.chatgpt.com/docs/hooks) требуют trust конкретного определения для non-managed hooks; фактическая причина trust/matcher/response handling не установлена. Trust и реализация не менялись.


## 2026-11-03 — Lifecycle repair acceptance

Исправлены ACT-F1..F6. Причина пропуска PreToolUse и Stop подтверждена read-only `hooks/list`: изменение двух statusMessage сделало определения `modified`. Восстановлены прежние определения со статусом `trusted`; команды, matcher, timeout, код защиты и записи trust не менялись. Новая desktop-сессия прошла полный 9/13 и обычный concise маршруты; запись через nested apply_patch при terminal marker запрещена, sentinel отсутствует. Валидатор принимает plain/bold labels и сохраняет обязательные closure/review ограничения. Согласованы eval, assigned scope product-manager, parent-owned skills и Sol identifier. Evidence: `lifecycle_parity.repair` в существующем November task-group JSON. Граница: проверенные локальные desktop-маршруты; исполнение молчащего Stop отдельно не трассировалось, production и полнота всех каналов записи не заявляются. [Official Hooks](https://learn.chatgpt.com/docs/hooks) describes exact-definition trust and skipping modified hooks. The previous failed acceptance remains historical evidence.

## G7: проверка архитектурных инструментов — 2026-11-09

[Import Linter 2.16](https://pypi.org/project/import-linter/2.16/) и [dependency-cruiser v18.6.0](https://github.com/sverweij/dependency-cruiser/blob/v18.6.0/package.json): разрешённая локальная установка с pinned dependency locks; синтетические Python/JavaScript controls описаны в G7 report (`research/product-agent-os-g7-execution-report-2026-11-09.md`). Installed JSON reporter и resolver filtering прочитаны; 10 ожидаемых outcomes распознаны после исправления фильтра, скрывавшего unresolved edges. Это local synthetic evidence, не target/TypeScript/production verification. [Codex v0.167.0 trace source](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/rollout-trace/README.md) — основание request receipt parser; фактическая eligibility указана отдельно и не выводится из config. Прежние утверждения об отсутствии установки относятся к этапу исследования.

G9 T11–T17: оценка влияния задачи на документацию, section CAS, восстановимые обновления карточки/указателя и ограниченная проверка межфайловых копий. Источник: `documentation_sync.py`, `document_navigation.py`; [контракт](../product-agent-os/project-formation.md); проверки и ограничения: `research/product-agent-os-g9-execution-report.md`. Локальная реализация; без утверждений о смысловом/модельном превосходстве или fresh-host activation.
