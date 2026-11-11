# Web M1 — реализация и пакет приёмки, 2026-11-11

Source status: project-authored / current-run local and native-offline evidence / partial acceptance. Исторические попытки 10 ноября сохраняются в [первичной квалификации](product-agent-os-web-m1-initial-qualification-2026-11-10.md). Этот отчёт не закрывает browser, provider или owner acceptance.

## Scope и ограничения

Владелец запросил реализацию всех 18 задач PAOS-M1 по DAG до PAOS-0045. Разрешены локальные изменения, синтетические данные и изолированные stdio/native проверки. Запрещены изменения системных политик, реальные ключи, provider и browser. Git history, публикация и миграция planning files текущего репозитория не выполнялись. Действующие scope/acceptance: PRD §17, architecture §21, wireframes v0.7; порядок и статусы — [матрица v0.8](product-agent-os-web-task-manager-plan-2026-11-09.md) и её JSON.

Root владеет интеграцией, HTTP/domain/import и evidence. `/root/m1_launcher` владеет launcher/runtime/connections, `/root/m1_task_model` — SQLite/search/backup и согласованными import fixes, `/root/m1_theme_locale` — UI/catalogs. Read-only review выявил дополнительные ошибки, исправления согласованы по файлам; review имеет `separate_reused_context`, не blind mode.

## Разрешение PAOS-0054

Причина прежнего Windows отказа локализована до контекста запуска: предыдущая диагностика выполнялась внутри AppContainer. Санкционированный native runner использовал обычный non-elevated token с `isAppContainer:false`, сохранил внутренний Codex MXC и managed configuration. Windows registry, политики, DACL устройства NUL и global Codex settings не менялись.

Закреплённый Codex 0.167.0: SHA-256 `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70`. `codex -c windows.sandbox=mxc sandbox --include-managed-config --permission-profile paos_fixture_write -- cmd.exe /d /c echo MXC_OK` завершился exit 0. App Server stdio сообщил `ready`, `Windows sandbox selection: mxc`, `MXC availability: true` и ожидаемый именованный profile, `workspaceWrite`, отсутствие сети и дополнительных writable roots. Оба синтетических файла были доступны до sandbox: внутри root ребёнок записал контроль, снаружи получил отказ; внешние bytes сохранились. Child exit 0; turns 0; auth.json отсутствовал; временный профиль удалён.

| Receipt в игнорируемом `.tmp/paos-m1/` | SHA-256 / результат |
| --- | --- |
| `native-mxc-smoke-result.json` | `7f6cc3e29d74bd1a6252736ee7bd757d1bbd5a0883b66e008c96f9d1cdcaad86`; native smoke exit 0 |
| `native-2026-11-11/windows-mxc-boundary-result.json` | `612e77d09da65e6329d39b1621eb79f4a50b5dbbac21409c13424d9a468661d7`; inside written / outside denied |
| `ephemeral-auth-verified-2026-11-11/windows-mxc-boundary-result.json` | Синтетический login/logout и проверка отсутствия canary; digest сохранён в execution-results JSON |

Проверка `node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema .tmp/paos-m1/stdio-diagnostics-result.json .tmp/paos-m1/native-2026-11-11/windows-mxc-boundary-result.json --sqlite-fixture-root .tmp/paos-m1` вернула exit 0, `stdio_checks_passed`, `missing:[]`, SQLite rollback/backup/FK true. Persisted-history control 1/1/0/2 принадлежит ранее выполненной изолированной диагностике; новый write/deny receipt дополняет её для того же binary SHA, не выдаётся за новый history run.

Синтетический `account/login/start` с `apiKey` принят, logout успешен. Прямой tool environment не содержит canary. После выхода процесса сканирование временного профиля завершено: 0 canary files, 0 unreadable files, auth.json отсутствует. Offline provider вернул `accountType:null`; это не доказательство реального account, entitlement или model access. Первые два canary harness attempts завершились ошибками сканирования открытых файлов/инициализации state; исправленный повтор сканирует только после остановки процесса.

Manifest: `packages/contracts/runtime/qualified-manifest.json`. Loader сравнивает exact OS/arch/build, Codex/Node hashes, SQLite version, adapter revision и lock digest; изменение tuple останавливает dispatch. Runtime selection хранится отдельно в приватном профиле; без него приложение остаётся `qualification_required`. Provider authority дополнительно выключена по умолчанию. Manifest не даёт commercial admission и не заменяет реальную проверку turn.

Источники решения: [Codex Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox#mxc-compatibility), [pinned availability implementation](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/mxc-sandbox/src/availability.rs#L17-L50), [Microsoft MXC](https://learn.microsoft.com/en-us/windows/apps/develop/mxc/quickstart). Свежие официальные источники сверены через OpenAI Docs, Context7 и web.

## Разрешение PAOS-0039

PRD §17.5 и auth §7 уже определяют `local_engineering_preview`, `local_api_byok`, плательщик `user_api_account`. AUTH-G1–G6 запрещают commercial/hosted distribution до отдельного review PAOS-0046/0030. Этот gate ошибочно препятствовал локальному implementation; карточка приведена к существующему scope. Inherited Codex login и SIWC остаются запрещены, model access — unverified. [App Server auth](https://learn.chatgpt.com/docs/app-server#auth-endpoints) не считается blanket разрешением коммерческой перепродажи.

## Реализованные поверхности

| Owner | Реализация и проверяемая граница |
| --- | --- |
| 0001/0002/0003 | Project root identity/coverage; flat M1 profile и стабильные ключи/UUID/provenance; event time с pause/retry/crash и actual-run projector. Imported time не обнуляется без наблюдаемого нового старта |
| 0004/0043 | React SPA RU/EN, Light/Dark/System, Tasks/sessions/comments/history, manual check/acceptance, read-only catalogs/search, import/export и backup/restore. UI rendering и accessibility требуют browser receipt |
| 0040 | Настоящий launcher entrypoint, single-instance reservation, loopback health, private pairing, keep-running owner и authenticated Quit. Browser/native window не открывались |
| 0041 | Connection broker, isolated ephemeral API login, no fallback, canary redaction, lazy Credential Manager bridge. Native vault roundtrip не разрешён auto-review |
| 0042/0044 | Pinned stdio RPC, server-owned task scope/revision, global lease, durable intent, duplicate/lost ACK reconciliation, approvals ACK отдельно от outcome, Stop/crash/restart guards. Не было реального provider turn |
| 0048 | Dedicated SQLite Worker, FK/project scope, revisions/epoch, immutable keys, atomic entity+audit+outbox, canonical command idempotency, bounded replay |
| 0049 | FTS5 RU/EN/exact IDs, scope/revision recheck, tombstones, partial coverage при failed index/rebuild; real workload ниже |
| 0050/0055 | Versioned MD/JSON preview, source snapshot/digest/provenance, unsupported significant fields блокируют; domain tools без raw SQL/credentials/Done; неизвестные legacy writers помечаются unsupported и блокируют cutover |
| 0051/0056 | Consistent snapshots/immutable manifests/blobs, отдельный restore, stale approvals/recovery-required runs, no dispatch replay; source lock/hash/identity, restore rehearsal и atomic authority switch, committed retry и reverse transfer |

Реальный target-project cutover не выполнялся. Synthetic supported project использовался для нативной проверки. Наличие неизвестных scripts в текущем репозитории корректно сохраняет legacy authority; adapter не объявляет их совместимыми по одному имени.

## Сквозная проверка без браузера

`node tests/web/single-window/headless-acceptance.mts --synthetic`, reviewed native runner, **exit 0**, 33 checks; финальный повтор 2026-11-11 08:00:29–08:00:46 MSK. Настоящие launcher, child service, HTTP loopback, built HTML и SQLite Worker; `showWindow` заменён только HTTP test callback. Browser/provider/real keys/system policies — false. Fixture cleanup — true. Предыдущий 26-check receipt принадлежал 07:17:17–07:17:23 MSK.

Проверены: unpaired 401; одноразовое pairing; cross-origin 403; project registration; task/ключ/идемпотентный retry; FTS; preferences; persisted session draft; Send fail-closed без provider authority; настоящий backup и отдельный restore; reverse export текущей задачи и повторный import как proposal; fixed source read/hash; native file sharing lock отклоняет запись, после release она доступна; hardlink source отклонён; preview сохраняет alias; JSON/MD conflict блокируется, согласованные records deduplicated; сервер перечитывает оба файла и отвергает drift каждого; locked cutover с restore rehearsal; обе привязки сохраняются в SQL; последующее изменение legacy source показывается без auto-import; committed retry после изменения source возвращает receipt; authenticated Quit ACK, exit и освобождение reservation.

Первый headless attempt обнаружил HTTP 400 вместо 409 для `runtime_unverified`: исправлена классификация lowercase runtime errors. Следующий прогон 19 checks и расширенный прогон 26 checks прошли. Headless не доказывает visual rendering, самостоятельный путь при закрытом Codex App или provider execution.

## Workload и performance

`node tests/web/single-window/workload.mts`: синтетическая файловая БД через настоящий Worker, 10 000 Tasks, 100 000 видимых messages, 1 000 documents, 209 736 923 UTF-8 bytes. 111 001 indexed records, FK failures 0, coverage complete, cleanup true. Node v26.5.0 / SQLite 3.53.3 / Windows 10.0.26200, 20 logical CPUs, RAM 16 892 026 880 bytes.

Baseline: 90,44 s, search p95 1298,77 ms — **не прошёл** цель 500 ms. Причина — scans counters и FTS query plan с дополнительной сортировкой. Исправлены derived counters, rank ordering и hashed scope tokens с последующим scope/revision check; migration v1 checksum сохранён. [FTS5 rank ordering](https://www.sqlite.org/fts5.html#sorting_by_auxiliary_function_results).

Первый повтор на том же dataset/40 queries/порогах: 48,43 s; search p95 87,67 ms, max 95,70 ms; small-command ACK p95 3,94 ms; warm page 50 Tasks p95 7,37 ms; fresh Worker reopen existing DB 58,71 ms. Финальный повтор после source freeze: **51,25 s; search p95 108,02 ms**, max 109,40 ms; ACK p95 4,72 ms; warm page p95 9,90 ms; fresh Worker reopen 63,14 ms. Все три порога пройдены. Финальный receipt содержит актуальные source digests. OS cache не очищался. Это не замер 4-core hardware, cold GUI launch или event-to-visible UI latency.

## Исправления по независимой проверке

Помимо исходных blockers исправлены: terminal run, ошибочно блокировавший новый mode/target; stale search при смене проекта; скрытые approval details/response_sent; canonical-key collision и строковые dependencies, обходившие cycle check; потеря committed retry после reopen; неканонический argument hash; стирание системных review flags агентом; отсутствие normalized-export proposal и MD/JSON bundle; source drift после cutover; hardlink catalog leakage; отсутствие источников read/hash, rebuild и explicit backup rotation в UI/API; autosave/scroll и неполная pagination.

Runtime использует fixed recipe `m1_fixed_v1`, реальные analyst/planner/builder assignments по mode и quoted saved task context. Original user message очищается и записывается одной транзакцией с intent до RPC; поздний wrapped provider echo не дублируется. EOF/reopen/retry проверены с реальным SQLite. Polling ограничен 750 ms/20 pages, последние ≤1000 messages читаются по локальному `journalOrder`; старые страницы по 50 доступны отдельно, одновременно ≤1050 persisted rows. Ordinal относится к DB generation; это не ID/cursor. Относительная хронология проверена через настоящий backup/restore закреплённого SQLite.

Streaming допускает только подтверждённый `final_answer`, держит bounded redaction state для split canary/key prefix и скрывает unknown phase. Check outcomes хранятся отдельно от turn success; diff обозначает proposed/runtime-reported partial/external и не выдаётся за filesystem verification. HTTP disconnect отменяет rebuild через AbortSignal; host/HTTP/task/storage/contracts входят в executable revision pin. Prompt behavior и provider streaming не подтверждены реальным turn.

Перед managed rotation UI показывает candidate IDs и требует отдельное подтверждение. Пройдена проверка создания шести копий без скрытого удаления, explicit rotation до пяти, сохранения pinned backups и пользовательских exports. При ENOSPC инъекции незавершённый snapshot удаляется, live DB/session/audit сохраняются; реальный disk quota не менялся.

## Обязательные незакрытые gates PAOS-0045

| Acceptance | Имеющееся evidence | Остаток |
| --- | --- | --- |
| SW-AC-01/10 | Настоящий headless launcher/service/SQL/Quit | Codex App закрыт, одно настоящее окно, provider turn и пользовательский путь не проверены |
| SW-AC-02 | Unconfigured/offline headless 401/403/409, no hidden fallback | Browser presentation отсутствует |
| SW-AC-03/04/05/06/07/08/09 | Contracts/failure injection, native scoped write/deny, durable SQL, account isolation fixtures | Provider turn/approval/interrupt/crash и token/limit responses не наблюдались end-to-end |
| ST-AC-01–07, DATA-AC-01–05 | Real SQLite workload/backup/restore, native source lock/cutover, deterministic fault fixtures | UI import/search/restore journeys не проверены browser; arbitrary legacy writers остаются unsupported |
| UX-AC-01–14/16–18 | Typed UI/API, controller/policy tests, production build; headless HTTP wiring | Rendering, streaming, diff/approval presentation и реальный workflow требуют browser/runtime |
| UX-AC-15 | RU/EN catalogs/themes и сборка | Keyboard, focus, 200% zoom, 320/1280/1440/1920 и контраст не проверены |
| 0041 native vault | Static PowerShell parse и injected-store tests | Automatic approval review отклонил synthetic Windows Credential Manager write/read/delete: это OS credential store вне временного профиля. Операция не выполнена и не обходилась |

PAOS-0045 получает `blocked` / `partially_verified`, а не фиктивный pass. Нельзя объявить M1 полностью принятой или разрешить следующую группу без изменения доступного evidence. Это остаточные acceptance/implementation obligations соответствующих owners, не принятый пользователем технический долг. Запрет browser/provider остаётся действующим; в рамках этой проверки он не ослаблялся.

## Итоговая проверка и control-plane sync

Итоговые команды, exit codes, hashes и review dispositions сохраняются в соседнем `product-agent-os-web-m1-execution-results-2026-11-11.json` после source freeze. Native Node/Web suite — **150/150, 0 skips**, exit 0; strict TypeScript — exit 0; production build — exit 0, 34 modules. Полный Python suite: `python -B -m unittest discover -s tests -q` — **1450 tests / 388,774 s, OK, 1 skip**, exit 0. Fixture eval — **91/91**, transcript — **26/26**, Codex compatibility — `compatible`, только local structure. Ранее concurrent suites во время незавершённых runtime/HTTP правок показывали failures и не используются как финальный результат.

Manifest loader проверен без запуска Codex: unconfigured blocked, точный tuple qualified, подменённый binary hash blocked. Manifest SHA-256 `0a980658f60e0198d1b2045feb832d53be6b1f81789422e0247846e751091cc3`, executable revision `ac18ca8a85a4757425250dd157eae47af3c4944afea25f274eaefc51a9e97d20`.

Root REQUIREMENTS/PLAN/TEST/RUNLOG обновляются компактными pointers через reviewed documentation sync; source registries RU/EN — парой. EVALS: `no_change_needed`, оценочные thresholds/claim policy не менялись; prod_test и AGENTS: `not_applicable`. Новые lifecycle hooks, schedules или durable permissions не активировались. Root site freshness не заявляется; MkDocs nav/extensions не менялись. Существующие canonical research records с непредставимыми значимыми полями сохраняют blocked preview; принудительная миграция ради зелёного статуса не выполняется.

Post-sync: обязательные docs/lifecycle/templates — **209 tests / 13,390 s, OK**, exit 0; `python -B tools/check_docs.py` и task-matrix validator — exit 0. Дополнительная проверка manifest/native gates после записи manifest — **9/9**, exit 0. Первый `git diff --check` обнаружил только новый пустой EOF в последней собственной карточке; он удалён, повтор завершился **exit 0**. Предупреждения Git о CRLF в старых Batch 39/41 artifacts не сопровождались semantic diff; их содержание не изменялось и не откатывалось.

Root docs применены existing sync writer с exact reviewed digest `sha256:6fd48b4b16de7eeeb6b9d4fcd7cddb968f55b01609bbbbb5c330a3211e2eb4f4`. Первый запуск не мог создать recovery journal в read-only `.codex`; reviewed native повтор записал только журнал и четыре Markdown-файла, config/hooks/permissions не менялись. Journal: `.codex/product-agent-os/compaction/6fd48b4b16de7eeeb6b9d4fcd7cddb968f55b01609bbbbb5c330a3211e2eb4f4.json`.

Generic section writer признаёт size exception только для `docs/planning/` и отклонил существующую research matrix размером около 250 KB. Ранее выбранное владельцем сохранение подробной research matrix без split соблюдено: 15 собственных M1 cards и JSON обновлены отдельным reviewed CAS, с before-images в private scratch, проверкой source hashes и matrix schema. 41 чужая/неизменяемая карточка и DAG сохранены; source files не разделялись и не сокращались. Все четыре root файла остаются ниже 40 000 UTF-8 bytes; REQUIREMENTS предупреждает выше 32 000. Это не изменение size guard или полномочий writer.

Итоговая projection: **11 implemented, 6 in_progress, 1 blocked** среди 18 M1 tasks; 56 MD/JSON statuses совпадают. Source digests финального workload и executable manifest совпали с текущими файлами; абсолютные user-specific paths в execution-results отсутствуют. Private recovery journals исключены через `.gitignore`; `git check-ignore` и финальный `git diff --check` завершились exit 0. Git history/publication не выполнялись. Остаток группы принадлежит PAOS-0041/0045 и связанным UI/runtime acceptance owners; он не объявлен принятым или списанным долгом.
