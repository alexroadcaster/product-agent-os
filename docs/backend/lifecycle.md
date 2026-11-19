# Backend: жизненный цикл local service

Source status: repository_source / static_source_review + bounded_native_synthetic_verified; 15.11.2026.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Владелец: backend/local-service и runtime owner. Scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении startup, session admission, route selection или shutdown.

## Запуск и admission

1. [main.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts) экспортирует `startLocalService`: импорт не создаёт server, базу, GUI или runtime child. Исполняемый entrypoint требует launcher IPC и профиль/instance ID. Профиль должен быть абсолютным локальным путём, identity привязывается до открытия `state.sqlite`.
2. Создаются store, runtime gateways, selector, recipes и scheduler; HTTP listener привязывается к случайному порту `127.0.0.1`. Код проверяет Host, origin, target и ограничивает размеры запросов. Health сообщает `alive` и отдельно `runtimeCapable`; первое не доказывает второе.
3. [session-gate.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) хранит sessions в памяти: restart и повторный pairing инвалидируют прежние cookies. Mutation требует origin и CSRF; exact origin/host проверяется и на read. Direct navigation bootstrap и pairing — разные пути входа в общий session contract.
4. [route-selector.ts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) сериализует connect/disconnect/runtime actions; default — `codex_app_agent` при отсутствии явного route и API key, наличие `apiKey` при отсутствии route выбирает `local_api_byok`. Переключение занятого route требует disconnect; implicit fallback отсутствует. Наличие App route не означает, что consumer подключён.

## Квалификация native runtime — FUNC-01

Текущий checkout проверяется по exact tuple в `packages/contracts/runtime/qualified-manifest.json`: Codex binary, Node binary/version, Windows release/arch, SQLite, adapter sources и Web lockfile. Изменение UI dependencies может изменить lockfile и остановить native broker с `package_lock_mismatch` даже при неизменном adapter. Обновлять pin без новой квалификации нельзя.

15.11.2026 исходный mismatch воспроизведён. Явный `sandbox-broker-acceptance.mts --run-once --candidate-inspection --binary <verified-local-binary>` проверил candidate на disposable roots, после чего manifest обновлён; повтор без candidate mode прошёл через production loader. Execution записывает внутри разрешённого root, outside/private temp получают `EPERM`; Discussion и Planning не записывают. Подмена binary, lockfile или adapter отклоняется до spawn. Первый отказ executor (`native MXC unavailable`) сохранён отдельно от успешного native прогона.

Это bounded native offline evidence без provider/model calls и human acceptance. После любого изменения pinned source нужен новый candidate receipt и повтор production admission. В карточке [PAOS-FUNC-01](../planning/functional-remediation-2026-11-15.md#task-paos-func-01) сохранены исходные проверки и повторная квалификация после F08.

### Квалификация Codex 0.170.0 {#codex-0170-qualification}

19.11.2026 для нативного брокера квалифицирован установленный Codex CLI `0.170.0`
на Windows x64 (`10.0.26200`). SHA-256 бинарника
`8d06dc231dba649c7d48d3eecab239c452a1ac498c41dd6492a6f301b90a22ce`,
ревизия адаптера `fb6db331a76a9acac5d5244400741483524a91fd53ae57aebd3bc8cb080b839b`.
На изолированной копии проверен штатный загрузчик с манифестом кандидата. После
обновления манифеста и брокера повторён тот же сценарий в рабочей копии.
Оба отчёта имеют SHA-256 `6eff0f2013db861528b3458ac7b030b43f780f4fabcf14621cf2e321f072d437`.
Отчёты сохранены в `.tmp/native-codex-0.170.0/`.

В `Discussion` и `Planning` запись внутри проекта получила `EPERM`. В
`Execution` запись внутри проекта прошла, запись за его пределами и в приватный
временный каталог получила `EPERM`. Остановка завершила активную команду.
Подмена хеша бинарника, lockfile или ревизии адаптера отклоняется до запуска.
Путь выбирает `runtime-selection.json` конкретного профиля. При откате версию
брокера, бинарник и ревизию манифеста восстанавливают согласованным набором.

После исправления PMETH-23 этот бинарник повторно квалифицирован с ревизией
адаптера `05fbd1d086c8411c1ad689bbdf02671e17db3da706a5691c467f30080846d5a9`.
Кандидат и штатный допуск прошли. [Повторная приёмка](../superpowers/specs/paos-pmeth-23-expanded-evidence.md#create-recovery-closure)

## Завершение

При `quit()` сервис сначала отклоняет новые запросы и отзывает sessions, отменяет собственный desktop dialog и начинает закрытие HTTP server. Затем закрываются scheduler и recipes, дренируется selector, закрываются gateways/channel. HTTP requests дренируются до закрытия store — это защищает незавершённые import/restore handlers. Повтор `quit` использует одну pending promise; ошибки сохраняют возможность повторной попытки, а не доказывают полный останов.

[supervisor/lifecycle.ts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/supervisor/lifecycle.ts) — отдельный supervisor contract: при неизвестном drain требуется durable recovery receipt до stop children; failure возвращает `stop_blocked`, подтверждённый drain — `stopped`, неизвестный после записи — `stopped_recovery_required`. Не смешивайте этот контракт с доказательством его исполнения в конкретном host-сеансе.

## Проверки и ограничения

[runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts), [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts) — связанные тесты; их ссылки не являются текущим прогоном. Проверить фактическую активацию конкретного маршрута можно только с авторизованным runtime evidence. Эта страница не подтверждает сетевую изоляцию произвольных native clients или доступ к provider.

## FUNC-G03 / F27 — сохраняемое фоновое сканирование

Сервис `apps/local-service/src/project-scans/service.mts` отделяет регистрацию проекта от полного обхода. `createProjectScans` предоставляет `initialized`, `status`, `start`, `cancel`, `retry` и `close`. `start` после проверки registry/root и сохранения CAS возвращает `queued`; inventory и analyzer выполняются в фоне. HTTP/onboarding wiring и доказательство нового пути принадлежат владельцу [FUNC-G03](../planning/functional-remediation-2026-11-15.md#func-g03-results); одни service tests не доказывают поведение Add в браузере.

Profile-owned `store_meta` namespace `project_scan_v1` содержит record `paos_project_scan_record_v1`: latest attempt, отдельно последнее успешное/частичное покрытие и до32 request digests. Это не task/document entity и не новая SQL migration. View `paos_project_scan_view_v1` передаёт monotonic CAS version; scan `paos_project_scan_v1` привязан к projectId, scanId, attempt, rootIdentity, policyVersion и inventoryRevision. Повтор request ID не запускает работу снова; одинаковые активные requests coalesce, конфликт scope/revision объясняется. После restart queued/running становятся `interrupted`, а продолжение требует явного `retry`. Неизвестный или повреждённый record не объявляется completed и возвращает `PROJECT_SCAN_STATE_UNAVAILABLE` для этого проекта.

Основные stages — inventory/documents/code/analysis. Versioned contract допускает schema/code_database только при явно переданном adapter; отсутствующие capabilities остаются false. Нет auto-install, provider/model вызовов или замены отсутствующего analyzer другим scanner. Ошибка отдельного analyzer оставляет результаты остальных stages, общий outcome — partial. `lastSuccessful` может быть partial с известным покрытием, не означает полный анализ проекта.

Cancel сначала подтверждает project/scan ownership, затем прерывает собственный controller и сохраняет terminal state. Analyzer получает signal, `publicationGuard` и синхронный `canPublish`; он обязан перед собственной публикацией/внешним эффектом проверить их. Orchestrator повторно сверяет scanId, root/policy и текущую inventory revision перед сохранением stage и последнего результата. Старый, отменённый или заменённый attempt не может поздно перезаписать lastSuccessful. Root интегрирует эти fences в code-index worker; внешняя timeout Promise без такого analyzer fence недостаточна.

Default budgets: один active scan, до20 queued/active intents на instance,60s на job,30s на stage,256KiB на sanitized stage result; persistent record ограничен1MiB storage boundary. Эти ограничения не изолируют произвольный JavaScript callback по RSS: adapter отвечает за остановку своего child/worker и собственные memory limits. Shutdown прерывает только scan IDs, принадлежащие этому instance, сохраняет interrupted и не воспроизводит работу. Источник остаётся read-only; bookkeeping хранится вне target.

Focused verification: `node --test tests/web/project-scans.test.mts` —12/12,0skip; `.tmp/func-g03/f27-final-focused.log`. Проверены queued-before-completion, stage failure/unsupported, late cancel, foreign-project cancel denial, coalescing/replay/restart/retry, source/root/policy drift, stale requested revision, external CAS supersession, timeout/result budgets, optional schema contract и повреждённый current-version record. Tests используют отдельный target workspace и profile DB. Focused strict TypeScript check service/contract прошёл (`.tmp/func-g03/f27-typecheck-green.log`); это не общий Web/build/browser run. Настоящие RED receipts сохранены, два первых timing-oracle checks исправлены на наблюдаемый persisted progress, а не на ещё не вызванный adapter.

Context7: [Node26 AbortSignal](https://github.com/nodejs/node/blob/v26.0.0/doc/api/globals.md) и [timers cancellation](https://github.com/nodejs/node/blob/v26.0.0/doc/api/timers.md). Abort listeners и timers снимаются при completion; даже pre-aborted Promise сохраняет rejection handler. Runtime activation, current native tuple qualification, UI и human acceptance проверяет root отдельно.

### F27 — persisted scan status UI

`ProjectScanStatus` использует authenticated scan API выбранного проекта. Он показывает latest/lastSuccessful coverage, stage progress/reasons, независимые unknown counters, root/policy/revision provenance и start/cancel/retry/refresh. Single-flight2s polling работает только при enabled и mounted; cleanup отменяет requests и снимает timers. Monotonic record/attempt и project/scope guards отвергают поздние ответы и не открывают terminal attempt заново. Pure merge regressions3/3 и scoped React TypeScript прошли; root отвечает за фактическое размещение, browser proof и final source/build bindings.

## FUNC-G03 — текущая проверка интеграции

Production App/API путь проверен: асинхронный сохранённый Add → Files до готовности graph → scan status → инертный source preview и line deep link → structured document backlink → задача. Browser foundation15/15, RU/EN × light/dark при1440/390px, Back focus, clipboard fallback, rejection позднего ответа другого проекта, отсутствие внешних запросов/page errors, неизменность target hashes. Clipboard и задержка доставки — явно synthetic boundaries. Source/build hashes и screenshots: `.tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json`. Service/API integration13/13 (`.tmp/func-g03/f26-f27-api-integration.log`), backend typecheck и production frontend build прошли. F18 common freshness и итоговая group/native qualification следуют далее; human acceptance отдельно.

## FUNC-G03 — итоговая проверка

Текущий интегрированный source, после первоначального lower-module handoff: browser19/19; полный Web594/594,0skip; backend TypeScript и production build прошли. Source/build hashes и screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Policy-race findings исправлены и независимо перепроверены5/5. Native candidate и production-default receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`. Прежние pending/wiring формулировки описывают датированный промежуточный slice; закрытием владеют итоговые task reports. Checkout core доступен; packaged core явно unavailable. Human/provider acceptance и F14/F33/F34 отдельно.

## FUNC-G04 — независимые stages и read snapshots

F27 сохраняет выбранный набор stages вместе с scan; inventory обязателен, schema и code_database могут запускаться отдельно от code/analysis. Coalescing связывает и stages; retry повторяет их, recovery не запускает работу автоматически. SQLite metadata job удерживает read lease до завершения/остановки extractor; helper loss/cancel запрещает публикацию. Target code, migrations и SQL не исполняются.

Graph status сравнивает F28 metadata revision/root/policy без перечитывания всех source bodies. Проверенный excerpt по-прежнему сверяет raw SHA256. Build сохраняет два checked raw passes,8 parallel handles и8MiB aggregate reservation; cache8 использует LRU, новый generation инвалидирует старый cursor. Task/startup readers выбирают kinds до64MiB safety budget. History использует bounded disk-backed frozen TEMP snapshots, не persistent schema migration; expiry/eviction/restart требуют новый cursor. Aggregate payload230MiB и TEMP mainfile256MiB не заявляются как лимит всего transient disk/RSS процесса.
