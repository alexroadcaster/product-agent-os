# RUNLOG.md

## PAOS-PMETH-23 — закрытие восстановления create, 19.11.2026

После подтверждённого создания следующий шаг читает только совпавший входной артефакт. Подмена с теми же байтами блокируется. Нативные `create` и `modify` прошли по 68/68, полный Web — 733/733. Ревизия адаптера `05fbd1d0` прошла квалификацию кандидата и штатный допуск. PMETH-23 закрыта локально, для поставки действует `hold`. [Повторная приёмка](docs/superpowers/specs/paos-pmeth-23-expanded-evidence.md#create-recovery-closure)

## PAOS-PMETH-23 — расширенная приёмка B3/B4, 19.11.2026

На `4f2d3400` прошли базовый CLI/Web, Design и FSD-пилот, G9/F13, нативное доказательство и откат, сохранение решения после перезапуска и браузерное восстановление `modify`. Восстановление `create` остановилось на `FILE_PREFLIGHT_BLOCKED` до запуска шага проверки. Полный Web — 729/729, целевой Python — 109/109. Квалификация `partially_verified`, поставка `hold`. [Матрица приёмки и пробелы](docs/superpowers/specs/paos-pmeth-23-expanded-evidence.md)

## Project Scan — регрессия полного Web-набора, 19.11.2026

Исправлена синхронизация теста при изменении файлов после входа в анализатор. Управляемое воспроизведение подтвердило отказ до входа при изменении во время проверки снимка. Целевой Windows-набор прошёл 21/21, полный — 729/729 без пропусков. [Причина и доказательства](TEST.md#project-scan-regression)

## Codex 0.170.0 — нативная квалификация, 19.11.2026

Установленный бинарник прошёл нативный допуск на одноразовых профилях с манифестом кандидата и со штатным манифестом. В брокере закреплена версия `0.170.0`, в манифесте обновлены SHA-256 бинарника и ревизия адаптера. Проверены три режима, остановка и отказ до запуска при подмене закреплённых компонентов. Оба полных Web-прогона дали 728/729 из-за одного сценария сканирования. Для поставки действует `hold`. [Квалификация и откат](docs/backend/lifecycle.md#codex-0170-qualification) · [Проверки](TEST.md#codex-0170)

## PAOS-PMETH-B4 — исполнение, доказательства и восстановление, 19.11.2026

Закрыты восемь локальных карточек B4. Технический результат связан с одним критерием, решение владельца и пробелы видны в карточке задачи. G9 и F13 проверены на одноразовых проектах, потеря результата после dispatch не вызывает повторного выполнения. Полный Python — 1401 тест с одним пропуском, полный Web — 727/727, целевой Web — 44/44, браузер — 53/53. Candidate и штатный нативный допуск прошли для одной точной ревизии. Для поставки действует `hold`. [Доказательства и границы](docs/superpowers/specs/paos-pmeth-b4-evidence.md)

## PreToolUse — проверка кандидата до записи, 19.11.2026

Активный hook и шаблон проверяют полный маркер до допуска записи. При неверном JSON, дайджесте или устаревших строках замены прежний маркер сохраняется. Точные `git --no-optional-locks status [--short]` и `Get-FileHash -LiteralPath` проходят проверку чтения без активного маркера. Эта проверка прошла до старта B4. [Регрессии](TEST.md#pretooluse-marker-preflight)

## PAOS-PMETH-B3 — design-сценарии и F14, 19.11.2026

Закрыты 08 → 09 и 10 → 11 → 12. Целевые проверки 26/26, браузер 48/48, Web 724/724. После правки узкой раскладки повторены 37 проверок пакета и интерфейса. Новый хеш F14 прошёл candidate и штатный нативный допуск. В B4 доступны 06 и 13. Для применения миграции отдельно выбираются область и PMETH-16. Решение о поставке остаётся `hold`. [Доказательства и ограничения](docs/superpowers/specs/paos-pmeth-b3-evidence.md)

## PAOS-PMETH-B2 — совет CLI/Web и решение о поставке, 19.11.2026

Закрыты 19 → 20 → 26 → 23 → 24 → 25. Нативный Web 718/718, браузер 35/35, CLI/Python 40/40. Четыре прогона дали один и тот же верный первый шаг в каждой паре. Полезность `insufficient_evidence`. Владелец утвердил `hold` для поставки точной локальной ревизии. [Доказательства, условия пересмотра и откат](docs/superpowers/specs/paos-pmeth-b2-evidence.md)

## PAOS-PMETH-B1 — совет в CLI, 18.11.2026

Выполнены 01 → 02 → 22 → 03 → 04 → 05 → 07. Сохранён baseline до изменения выбора. На одном синтетическом проекте CLI выдаёт именованный тест для backend-ошибки и исходник для docs-only. Проверены Python/TypeScript, сохранение байтов проекта, правильный RED, минимальный GREEN и отдельная ошибка импорта. Полный Python-прогон — 1386 тестов, один пропуск, fixture eval — 91/91. Следующая задача — PAOS-PMETH-19. [Проверки, ограничения и передача](docs/superpowers/specs/paos-pmeth-b1-evidence.md)

## PAOS-METH-15 — выбранные границы App и экранов, 18.11.2026

Back снова открывает сообщение по тому же URL. Сняты четыре импорта внутренних файлов Tasks. Web 714/714 без пропусков, браузер 163/163. Выполнены 17 из 17 карточек A в выбранном объёме. Пять прежних исключений сохраняют отдельный `hold`. [Приёмка и откат](docs/planning/methodology-improvement-2026-11-15.md#meth-15-results)

## PAOS-METH-14 — выбранный срез Team, 18.11.2026

AgentDashboard перенесён в Team. Снято последнее исключение с импортом Dashboard из Team. Web 710/710 без пропусков. Браузер сохранил командную статистику, профиль и каталог, 114/114 до и после. При закрытии METH-14 для Skills и METH-15 действовал `hold`. [Приёмка и откат](docs/planning/methodology-improvement-2026-11-15.md#meth-14-results)

## PAOS-METH-13 — выбранный срез Tasks, 18.11.2026

Панель передана владельцу Usage, два исключения удалены. Проверены возврат к той же задаче, черновики и фокус. Web 709/709 без пропусков, браузер 212/212. На момент METH-13 действовал `hold` для Workflows, METH-14 и METH-15. [Приёмка и откат](docs/planning/methodology-improvement-2026-11-15.md#meth-13-results)

## PAOS-METH-10 — общие Markdown и диаграммы, 18.11.2026

Общие Markdown, Mermaid и D3 вынесены в `ui`. Удалены пять импортов, из них два закреплённых исключения. Осталось 12 исключений. Web 707/707 без пропусков. Браузерные сценарии прошли 131/131 до и после. На момент METH-10 действовал `hold` для METH-13/14/15. [Приёмка METH-10](docs/planning/methodology-improvement-2026-11-15.md#meth-10-results) · [Условия повторного выбора](docs/architecture/decisions/adr-dashboard-task-boundary.md#a2-rollout)

## PAOS-METH-11 — выбранный объём A4 выполнен, 18.11.2026

TeamManager использует публичный вход Tasks. Два исключения удалены. Web 705/705, браузер 55/55 до и после, четыре файла сборки совпали по SHA-256. [Результат METH-11](docs/planning/methodology-improvement-2026-11-15.md#a4-results)

## PAOS-METH-A3 — регрессии и передача задачи, 18.11.2026

Выполнены METH-05/06/07. Целевой Web-набор 44/44 и Python 88/88. Исходный и сокращённый handoff подтвердили 6/6 фиксированных решений каждый. Кандидат сохранён для сравнения со статусом `hold`. Следующая работа A4 — METH-11 для TeamManager. [Результаты A3](docs/planning/methodology-improvement-2026-11-15.md#a3-results)

## PAOS-METH-A2 — пилот Dashboard принят, 18.11.2026

METH-12/17/18 выполнены. Три прямые связи Dashboard с внутренними модулями Tasks заменены публичным входом. Web 704/704 и браузер 52/52. Следующий шаг A3 — METH-05. В A4 выбран один потребитель TeamManager для METH-11. [Результаты и решение](docs/planning/methodology-improvement-2026-11-15.md#a2-results)

## PAOS-METH-A1 — Dashboard, 18.11.2026

Группа A1 выполнена. Закреплены контракт Dashboard, браузерная регрессия и правила импортов с 19 исходными исключениями. Финальные проверки: Web 702/702 и браузер 50/50. Следующий вход в A2 — METH-12 с узким API чтения Tasks. [Критерии, ADR и evidence](docs/planning/methodology-improvement-2026-11-15.md#a1-results)

## Методологии — пересмотр планов A и B, 18.11.2026

В A технический пилот заканчивается проверкой границы Dashboard. В B первым результатом запланирован совет в CLI и Web для двух задач одного проекта, с объяснением выбора и следующего шага. В карточках указаны владельцы анализа, решений, доказательств по критериям и операций записи. Дальнейшее выполнение требует отдельного запроса. [План A](docs/planning/methodology-improvement-2026-11-15.md) · [План B](docs/planning/user-project-methodologies-2026-11-15.md) · [Основания изменений](research/methodology-plan-review-2026-11-18.md)

При сверке четырёх RU/EN-матриц подтверждены 43 исполняемые карточки в статусе `planned`, 155 ID критериев и отдельная справочная METH-16. В A осталось 17 обязательных рёбер, в B — 31. Обе пары JSON-зеркал побайтно совпадают. Графы ацикличны, обратные `blocks` согласованы. Перед расширением поставки B выбранные возможности проходят профильную проверку PMETH-23, решение о расширении принадлежит PMETH-25.

## F23 — ожидание решения пользователя, 16.11.2026

По прямому запросу владельца F23 переведена в awaiting_user_decision / «Ожидание решения пользователя». Проверку и обратную связь выполняет пользователь; дальнейшее действие — после его решения. F24/F19/F25 implemented, FUNC-G07 открыта, общий итог33implemented/1awaiting_user_decision. Прежние technical receipts сохранены в verification.previous_func_g07; новые Web/native/site прогоны этим изменением статуса не заявляются. Control-plane sync updated REQUIREMENTS/PLAN/RUNLOG/TEST; EVALS/prod_test no_change_needed: исходные AC, thresholds и Batch39 не менялись. [Карточка и evidence](docs/planning/functional-remediation-2026-11-15.md#func-g07-results).

## FUNC-G06 — закрыта, 16.11.2026

FUNC-G06 implemented3/3. F21processcrash/ownership20/20; F22import/backup11/11; finalweb694/694,0skip. Managedactualpackage10/10,3installedA/B/Aphases withrealNativeLauncherIPC/service andreadback; nativewindow=false,currentOSaccountfreshfixtureenvonly. Homeenvandhomelock defects actualRED→GREEN; originalfilehashespreserved,newemptyWAL/32KiBSHM explicitlyrecorded. Finalreview separate_reused_context,closed_allowed (.tmp/func-g06/final-review.json);157source/package/distbindings,31foreigncards/JSONperlanguage,141rootsections preserved. RUENvalidatorok=true/errors=[],docs14passed; priorfailedvalidatorreceiptsretained. No provider/realcredentials/Git/systeminstallation/publication. [Решения/evidence](docs/planning/functional-remediation-2026-11-15.md#func-g06-results).

## FUNC-G05 — закрыта, 16.11.2026

FUNC-G05 implemented,5/5. Fullweb686/686,0fail/skip; browser16/16 source/build bound, typecheck/build/native candidate→default passed. Independent source review нашёл rollback-operation defect, исправленный actual RED→GREEN; browser нашёл Usage wiring defect, исправленный и проверенный. Setup/selector/HTTP fixture failures сохранены. Final review separate_reused_context, closed_allowed (.tmp/func-g05/final-review.json). Preservation check:29foreign cards/JSON,137root sections, AC/groups/M5/history и215source+4dist hashes сохранены; docs28/validators passed. Текущий итог27 implemented/7 planned; M5, остальные29 cards и historical evidence сохраняются. Residual limits: Windows writer, non-atomic external ignore revocation, explicit unknown recovery, no host telemetry/loaded attestation/money enforcement/human acceptance. [Решения и evidence](docs/planning/functional-remediation-2026-11-15.md#func-g05-results).

## FUNC-G04 — закрыта, 16.11.2026

F20/F09/F14/F33/F34 implemented,5/5; [итоговые решения и evidence](docs/planning/functional-remediation-2026-11-15.md#func-g04-results). Web658/658,0skip, browser18/18/current204source+dist, TS/build/native candidate→default и F20 current133-input protocol выполнены. Review closed_allowed; исходные4 findings и поздний P2 magic table-name dictionary исправлены с regressions, продуктовые/UI failures и sandbox refusals сохранены. Общий итог22 implemented/12planned; остальные29 cards, M5, root foreign sections и baseline HEAD5a9c87b… сохраняются.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG updated; EVALS/prod_test no_change_needed (нет AI rubric/Batch39 изменения); atlas/MkDocs no_change_needed. Корневые файлы превышают advisory40KB: deferred_hygiene, исходный материал не сокращался. Residual risks: cold history/catalog выше1s,10k-directory30s timeout, native/aggregate RSS и reference-hardware limits; Windows/offline/static subset, provider/human/release отдельно. Owned synthetic fixtures и binary очищаются с сохранением receipts; чужой session marker не меняется. Другая группа не стартовала.

## FUNC-G03 — завершена, 15.11.2026

Семь карточек implemented / locally_verified; [итоговые решения/evidence](docs/planning/functional-remediation-2026-11-15.md#func-g03-results). Полный Web594/594,0skip; final browser19/19; TS/build и native candidate/default текущего tuple64cd3b58… прошли. Independent review policy-race подтверждён RED, общий final registry fence исправлен, cycle2 проверил5/5 и дал closed_allowed. Docs/statuses/source/build/preservation синхронизированы; temporary browser/core/native fixtures очищены, failed receipts сохранены. Начальный snapshot5a9c87b…, baseline/evidence `.tmp/func-g03/`; прежние G01/G02, прочие27 cards, M5 и чужие planning/marker hunks сохранены. Остаточные границы: packaged core unavailable (F17), performance/RSS (F09/F20), future Map/schema consumers (F14/F33/F34), human/provider/release отдельно. Другой scope не запущен.

## FUNC-G02 — закрыта как исследование, 15.11.2026

F30/F31/F32 implemented / poc_research_locally_verified,3/3; [источник решений/evidence](docs/planning/functional-remediation-2026-11-15.md#func-g02-results). F30 bounded_adopt imports10/10 vs7/10baseline; F31 reject before-index для текущего Windows profile, downstream unexecuted/null; F32 reject authoritative metadata,23positive/3candidate defects retained, explicit Node alternative. Nullability P2 и два UI P2 независимого review исправлены; root проверил final delta. Combined unit22/22, prototype TS/build, browser22/22, source/build/hash bindings и screenshots подтверждены. Docs/registry/task MD/JSON/control-plane synchronized; общий итог10 implemented/24planned, остальные31 records/3M5 сохранены. Matrices RU/EN, source-docs19, preservation/provenance и diff checks passed. EVALS/prod_test no_change_needed; production tuple, real DB/credentials, provider/model/global config/Git не затрагивались. Rollback только own hunks; human/product integration отдельно.

## METH — план разделён на A и B без реализации, 15.11.2026

[A](docs/planning/methodology-improvement-2026-11-15.md): 17 внутренних planned задач + METH-16 reference-only; [B](docs/planning/user-project-methodologies-2026-11-15.md): 26 planned задач, 104 AC и отдельный JSON owner. Все 18 прежних ID и legacy AC сохранены; два прежних dependency edges к METH-16 сняты с active DAG, критерии METH-05/18 уточнены с сохранением прежнего текста в history. Пользовательский маршрут не ждёт внутреннего FSD. Current static split/parity/preservation evidence — в B-плане; application/runtime/model проверки этим запросом не запускались. Параллельный FUNC-G03 и чужие markers/source edits сохранены; TEST/EVALS/prod_test no_change_needed. Следующий возможный B-slice — PMETH-01 после отдельного запроса.

## FUNC-G01 — закрыта, 15.11.2026

F01/F03/F04/F05/F06/F07/F08 implemented_locally_verified,7/7; [полный evidence](docs/planning/functional-remediation-2026-11-15.md#func-g01-results), [machine state](docs/planning/functional-remediation-2026-11-15.json). Native tuple переквалифицирован после contracts move; broker write/deny/restart и drift fences passed. Draft/browser54 + dashboard/browser30, Web507 unique с отдельным15-case environment retest; TS/build passed. Independent architecture/implementation и CSS delta review closed_allowed. RU/EN domain docs, registry, task cards/statuses и control-plane обновлены. Другие27 FUNC и3 M5 refs сохранены; другая группа не запущена. EVALS/prod_test no_change_needed. Human/provider/production/site freshness не повышены; rollback только own hunks, pinned-source rollback требует requalification.

DG07 завершена: DOCS-14/15/16 implemented / docs_static_verified; все 16 documentation tasks и 7 DG-групп закрыты. Шесть новых RU/EN operations pairs, пять обновлённых plugin pairs; FUNC owner/update matrix покрывает 7 групп/34 задачи. [Evidence](docs/planning/documentation-architecture-2026-11-15.md#dg07-results): source4, matrices2, strict/site7, links/parity/preservation и cross-review passed. Далее bounded FUNC slice; F17/F25/M5 и runtime/human/commercial gates не закрывались. EVALS/prod_test no_change_needed.

DG06 завершена: DOCS-12/13 implemented / docs_static_verified; 11 RU/EN пар security/testing, nav/registry/maps и owning plan synchronized. [Результаты и команды](docs/planning/documentation-architecture-2026-11-15.md#dg06-results). Source4, matrices2, strict build/site7, HTML/source links и source parity passed; перекрёстный static review closed_allowed. Следующий DG07; DOCS-16/B открыт, DOCS-14/15 planned. Runtime/provider/human/release claims не повышены; EVALS/prod_test no_change_needed.

## DG05 — завершено, 15.11.2026

DOCS-08–11 implemented / docs_static_verified: 20 RU/EN пар AI/agents/LLM/retrieval/code-intelligence. [Evidence и команды](docs/planning/documentation-architecture-2026-11-15.md#dg05-results): source3+card parity1, matrix2, strict build, site7, HTML/pinned-source links passed. Scoped reviews LLM и retrieval/graph пройдены; WebFTS/Python/gates/live разделены. Код, prompts/config и runtime/providers не менялись; новый end-to-end Web RAG и PoC не заявлены. Далее DG06; DOCS-13/16 B открыты.

## DG04 — завершено, 15.11.2026

DOCS-06 implemented / docs_static_verified: 6 RU/EN пар frontend, 15 разделов навигации, components/state/drafts/design/a11y boundaries. [Evidence и команды](docs/planning/documentation-architecture-2026-11-15.md#dg04-results): source3 + card parity1, matrix2, strict build, site7, HTML/pinned-source links passed. Независимый scoped review пройден; desktop/historical narrow-width и human/WCAG gaps разделены. Application/browser/provider checks не выполнялись. Далее DG05; DOCS-13/16 B открыты.

## DG03 — завершено, 15.11.2026

DOCS-04/05/07 implemented / docs_static_verified: 17 RU/EN пар backend/API/DB и editable ERD. [Результаты и команды](docs/planning/documentation-architecture-2026-11-15.md#dg03-results): source4, matrix2, strict build, site7, HTML/source links и Mermaid2 passed. Scoped independent API review; уточнения action bodies и ERD cardinality исправлены. Приложение, реальные БД и providers не запускались; FUNC/M5 не менялись. Следующий DG04; DOCS-13/16 B открыты.

## DG02 — завершено, 15.11.2026

DOCS-01–03 implemented / docs_static_verified: 13 RU/EN пар, три входа/owners, продуктовая модель и traceability, архитектура компонентов/потоков, ADR provenance и схема в atlas. [Результаты](docs/planning/documentation-architecture-2026-11-15.md#dg02-results): source3, matrix2, translation-card regression, strict build, site7, HTML links и Mermaid2 passed; scoped independent review, W05 finding resolved. Продуктовые runtime/provider проверки не выполнялись; ссылки на тесты не выданы за прогон. Следующие DG03/DG04; DOCS-13/16 B остаются открыты.

## DG01 — завершено, 15.11.2026

DOCS-13/A и DOCS-16/A completed / docs_static_verified. [Evidence](docs/planning/documentation-architecture-2026-11-15.md#dg01-results): links/anchors и восемь полных EN-переводов; 16 matrices, source 3/3, archive 99/99, site 7/7, targeted hooks 3/3, strict isolated build и HTML links passed. Parent DOCS-13/16 in_progress до B, остальные14 planned; следующий DG02. Root site/, hooks/trust, feature JSON/runtime/Git не изменены. Review: self_review + independent scoped translation/test review, findings resolved.

## Группы документации — исторический этап планирования, 15.11.2026

В [плане DOCS-01–16](docs/planning/documentation-architecture-2026-11-15.md) сохранены 7 групп DG01–DG07. DG01 первым устраняет links/localization/build и устаревшие проверки: DOCS-16/A + DOCS-13/A; их финальные этапы остаются DG07/DG06. 16 задач / 18 этапов, статусы planned; исходные AC/Depends/Blocks сохранены. Matrix/source-docs 3/3/check_docs/diff и сохранность карточек, membership, stage DAG, first gate — passed; self_review. Ни исправления, ни написание разделов не выполнялись. Ранее выявленные site/archive/build gaps остаются открыты. Следующий шаг при отдельном запросе реализации — DG01.

## Перенос planning и аудит документации — 15.11.2026

42 файла перенесены в `docs/planning`; [карта](docs/planning/relocation-2026-11-15.json) и [backlog PAOS-DOCS-01–16](docs/planning/documentation-architecture-2026-11-15.md) владеют деталями. Исправлены references и path-dependent checks; app features не менялись. 120 focused tests passed; source/matrix/diff проверки пройдены. Архив 98/6 failures, preview site 7/4 failures; strict build exit1 (repository-only ссылки и 8 EN gaps). Полные результаты — evidence-раздел backlog; website publication не готова. Дальнейшая работа: DOCS-01 → доменные документы; FUNC/Web statuses и их семь групп сохранены.

## Проверки по изменённому контракту — 15.11.2026

`PAOS-SCOPED-VERIFICATION-2026-11-15`: текущий маршрут в TEST; source docs отделены от opt-in site/archive, повторные eval CLI и per-write advisories убраны. Default document size advisory; explicit limits, permission/data guards и recovery сохранены. [Изменения, focused checks и ограничения](research/product-agent-os-scoped-verification-2026-11-15.md). Общий suite и новая сборка сайта не запускались; fresh-session loading не заявляется.

## Функциональная матрица после V3 — 15.11.2026

Обновлена [матрица и evidence](docs/planning/functional-remediation-2026-11-15.md): 34 FUNC задачи распределены ровно по одному разу в 7 delivery groups; три M5 ссылки отдельно. Исходные AC/Depends/Blocks/order/status/estimates сохранены; добавлены group membership, cross-group edges, внутренние ветки, UI/UX outcomes, ownership и exit gates. Старт определяется задачей, полное закрытие G07 требует G01–G06. Matrix/scoped-docs/diff и MD/JSON membership/DAG/preservation passed; source-docs tests 3/3; предыдущие PoC-planning receipts сохранены. Реализация/PoC/runtime не запускались.

## MD-отчёты и чтение — 15.11.2026

`PAOS-REPORT-READ-FIX-2026-11-15`: current-host MD create/update/update + neighboring deny подтверждены; full1453/skip1, focused209, fixture91/91, transcript26/26. Исправлен также document-size gate для Python hook с сохранением explicit limits. [Evidence и все failed attempts](research/product-agent-os-report-read-fix-2026-11-15.md). Hook definitions/trust не менялись; fresh-session activation отдельно. Остальные ограничения правил проанализированы, не сняты.

## Desktop UI/UX — внедрение 13.11.2026

V3 repair: сетки и внутренние экраны перенесены; visual review85×2, final web500 и V3 browser378 passed; functional team/workflow51 passed. UI-10 motion/reduced motion проверены. [План](docs/planning/2026-11-13-v3-ui-implementation-plan.md), [evidence](design/2026-11-13-v3/implementation-evidence.md). UI-01–UI-12 in_progress до приёмки; usage unavailable, existing Chrome final reload не наблюдался (Debugger unattached). Backend/API/providers не менялись.

## Startup UX — 13.11.2026

Убраны ручной код и MessageBox; protected browser bootstrap, legacy-service restart fence. Native/browser28, Web487, Python1450(skip1), docs105, evals91/26 passed; [owning report](research/product-agent-os-web-m1-execution-2026-11-11.md#запуск-без-ручного-сопряжения--2026-11-13). M5 planning byte-preserved; user service не останавливался. Следующий шаг — штатный Quit старого экземпляра и обычный запуск с тем же профилем.

Settings,13.11.2026: Settings: native folder/New folder, автозаполнение/scan и понятный App draft/Send реализованы. Web495, chooser4 и actual App/browser17 passed; [current evidence/limits](research/product-agent-os-web-m1-execution-2026-11-11.md). Native URI opening на owner desktop/human acceptance отдельно. M5 planning сохранён; старый service не останавливался.

13.11.2026: service_unhealthy профиля manual-review устранён по отдельному разрешению: stale reservation сохранена под backup-именем, DB bytes до startup сохранены, новый actual /health healthy. Приложение оставлено работающим. [Диагностика, approval и границы](research/product-agent-os-web-m1-execution-2026-11-11.md). Production source без изменений.

## GAP-06 acceptance и исправление проверок — 2026-11-10

GAP-06 принят владельцем; T34 и fresh-session activation отдельно открыты. Исправления locally verified: full 1450 tests (skip 1), fixtures 91/91, transcripts 26/26; актуальные проверки: [owning evidence](research/product-agent-os-audit-closeout-tooling-2026-11-10.md).

## PAOS-AUD-G9 — закрыта после приёмки T17

T10 принят владельцем; T11–T16 реализованы и локально проверены; T17 owner accepted; G9 closed. Baseline сохранён до edits; текущие проверки и границы — [G9 execution report](research/product-agent-os-g9-execution-report.md). Проверки и comparison приняты владельцем вместе с ограничениями model behavior. Fresh-session activation отдельно.

## PAOS-AUD-G9 — результаты для приёмки

G8-T14/G8 owner accepted. G9 T01–T09 локально реализованы; T10 technical packet owner accepted (10.11.2026). Ran 1435 tests in 803.716s, OK (skip 1); fixtures 91/91, transcripts 26/26, compatibility compatible, strict MkDocs preview passed; 3/3 comparison pilots; final docs/lifecycle/status 130 tests OK, matrix/links/projection checks passed. [Отчёт и failed attempts](research/product-agent-os-g9-execution-report.md), [результаты](docs/superpowers/specs/paos-aud-g9-project-formation-results.json). Existing documents остаются companion proposals; provider/host/cache/Git/real-target actions отсутствуют. Fresh-session activation отдельно. Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated; AGENTS/prod_test not_applicable.

## PAOS-AUD-G8 — текущая реализация, 2026-11-10

Реализованы document/readiness contracts, scoped generation, preserve-on-regeneration, actual-context validation, byte budgets, lossless compaction с journal/recovery, navigation/provenance и terminal read-only regression. Три synthetic pilots пройдены; full unittest 1409 (skip 1), final selector checks 38, fixture 91/91, transcript 26/26, compatibility и strict MkDocs прошли. Receipts и границы проверки находятся в [execution report](research/product-agent-os-g8-execution-report.md). REQUIREMENTS historical block: 15 423 original bytes сохранены, root 48 567 → 33 375 bytes до обновления текущего scope. Git/provider/real-target/host activation actions отсутствуют. Текущую audit matrix не разделяли: владелец отложил split T09. Приёмка T14 получена. Владелец оставил research matrix целой; actual apply не выполнен. Fresh-session activation остаётся открытой отдельно.

Уточнение владельца 10.11.2026: подробные матрицы в `docs/planning/` сохраняются целиком, default 40k size trigger исключён; оглавления/control-plane и explicit per-file limits сохраняют ограничения. Audit matrix в `research/` остаётся целой; split отложен, прежний preview не разрешён. G8-T14 и закрытие G8 явно приняты владельцем; fresh-session activation отдельно.

Текущий завершающий прогон после исключения docs/planning: full unittest 1414 / 1321.762s, OK (skip 1), exit 0; docs handoff 105 / 19.108s; fixture 91/91, transcript 26/26, compatibility passed. Strict MkDocs завершился за 38.95s. Все 48 audit cards сохранены, current-state projection: 65 строк без ошибок. T14 — owner_accepted; технические проверки завершены, приёмка владельца получена отдельным решением.

## Старт Web M1 — 2026-11-10

M5, 13-11-2026: по решению владельца PAOS-0047/0052/0053 объединены в [M5 / план v0.9](docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md#paos-m5); все planned, 60ч, прежние ID/order/dependencies/actual time сохранены. MD/JSON/PRD/architecture/auth/registry синхронизированы. Проверки текущего запуска: docs105/105 (11.802s), matrix/state/docs/diff exit0; preservation passed — другие53MDcards побайтно и JSON objects без изменений. Финальные receipts/source hashes — `.tmp/paos-m5-plan/results.json`; baseline/recovery сохранены в `.tmp/paos-m5-plan/`. Оценки прежние: M5=60ч, общий объём776ч; до M4 включительно716ч с8ч POST_M1 review. Следующий шаг — team design0052; SIWC отдельно после admission. Без runtime/provider/hosting/transfer/Git действий.

PAOS-0030: переносимый package/CLI и согласованный codex_docs copy pilot выполнены;88actual checks/3phases + native Cancel, Web482. Astra/medium mapping/review: P2 shared reservation исправлен; actual startup выявил missing parser/preferences closure и internal preference relocation, исправлено без изменения native pin. [Owning evidence](research/product-agent-os-web-m4-0030-execution-2026-11-12.md). Следующая0052 отдельным scope; AUTH-G1–G6 no-go коммерческого выпуска сохраняется.

Исторический срез до PAOS-0030 (provenance сохранён): PAOS-0029: доступны keyboard Kanban/workflow/task tabs, RU/EN light/dark, modal/mobile focus, длинные узкие layouts. Matrix1311/280views, core136/20 и states289/60 passed; Astra/medium mapping/review, два P2 стенда исправлены; поздний mobile fix проверен root. [Owning evidence](research/product-agent-os-web-m4-0029-execution-2026-11-12.md). Следующая0030: отдельный pilot scope и повторный AUTH review; no provider/Git/install/release actions.

Исторический срез до PAOS-0029 (provenance сохранён): PAOS-0028: ten PRD scenarios и полный current App route проверены; устранены missing agent Bug creation и S09/S22 revision churn. Astra/medium research/review + actual worker завершены; source-bound receipts в [owning report](research/product-agent-os-web-m3-0026-execution-2026-11-12.md). Следующая PAOS-0029 отдельным scope; no provider/Git/install/release actions.

Исторический срез до PAOS-0028 (provenance сохранён): PAOS-0026 реализована: Decisions/S22, shared S09 response, private durable history, diff/scope/evidence и autonomy observation. Astra/medium research/review завершены;2 замечания исправлены и проверены. [Current receipts и ограничения](research/product-agent-os-web-m3-0026-execution-2026-11-12.md). Следующая PAOS-0028 отдельным scope; unknown native outcomes не replay, human/commercial/release отдельно.

Исторический срез до PAOS-0026 (provenance сохранён): PAOS-0025 реализована: checkpoint recovery/receipts/history, повторная квалификация exact broker binding после restart, queue running projection, timeout/cancel ACK. Astra/medium research/review завершены; current full/native/browser/actual receipts и gaps находятся в [owning report](research/product-agent-os-web-m3-0025-execution-2026-11-12.md). Следующая0026 отдельным scope. Unknown dispatch сохраняет ownership; human/commercial/release отдельно.

Исторический срез до PAOS-0025 (provenance сохранён): PAOS-0024 реализована: queue + immutable assignments, atomic dependencies/hard WIP/ownership, real parallel roots cap4 при project1. Web443; Python1450(skip1); fixtures91/transcripts26; browser88/native49/actual App46 passed. Astra/medium review P2cap/reserved roots и drive-root overlap исправлены. [Evidence и limits](research/product-agent-os-web-m3-0024-execution-2026-11-12.md). Следующая0025 отдельным scope. Human/commercial/release отдельно; старые receipts сохраняют provenance.

Исторический срез до PAOS-0024 (provenance сохранён): PAOS-0037: pinned recipes, bounded retry/join, task ownership, policy pin и Manual0 реализованы; [evidence](research/product-agent-os-web-m3-0037-execution-2026-11-12.md). Web433, Python1450(skip1), fixtures91, transcripts26, browser/native57 и actual App46/два шага passed. Astra/medium review: два P2 и recovery linking исправлены; startup race найдена full suite и исправлена. Следующая PAOS-0024 отдельным scope. Human/commercial/release acceptance отдельно; исторические receipts ниже сохраняют provenance.

Исторический срез до PAOS-0037 (provenance сохранён): Текущий срез 12.11.2026 — PAOS-0023: project policy, explicit opt-in, server budgets/deadline/stop и pause; [evidence и пределы](research/product-agent-os-web-m3-0023-execution-2026-11-12.md). GPT-6 Astra / medium выполнили boundary research/frontend и independent review; replay-Pause finding воспроизведён и исправлен. Production browser/native47 passed, synthetic worker; actual model не вызывался. Следующий маршрут — PAOS-0037 после обязательных gates. Исторические записи ниже сохраняют свой provenance.

Текущий handoff PAOS-M2: PAOS-0019/0020/0021/0022/0027 technical implemented_locally_verified_app_active;26/26 вместе с [M2b](research/product-agent-os-web-m2b-execution-2026-11-12.md) (PAOS-0036/0009–0018) и [first10 M2](research/product-agent-os-web-m2-execution-2026-11-11.md). [M2c evidence](research/product-agent-os-web-m2c-execution-2026-11-12.md) владеет receipts/hashes/7fixed findings/RED/failures. App consumer обязателен, lexical subset/partial coverage явные, document proposals staged-only; installed npm runtime_mismatch fail-closed, exact cached native tuple отдельно. Schema3 SQL1/2 checksums, backup inactive, recipes metadata/native loaded unknown сохранены. M3/T1, human/commercial/release/AUTH-G1–G6/C46-01–08/PAOS-0030 отдельно; [PAOS-0046 review](research/product-agent-os-web-commercial-review-2026-11-11.md). Rollback только свои hunks; M1/старые receipts не переоткрыты.

Результат M1 до PAOS-0046: Текущий handoff 2026-11-11: M1 technical18/18 в выбранном App-active маршруте. Actual App+offline native broker105, task39/data25/headless33/Web306/strict/build/manifest6 passed; source149162. Исправлены WebSocket framing/endpoint diagnosis, capability redaction/cleanup, mode-selection restart, cutover backupId replay, подробная durable History/comment privacy и TaskForm summary corruption. GPT-6-Astra/high independent review closed_allowed в bounded scope; failed receipts/owner rejection сохранены. Активный App consumer необходим; whole-App sandbox, Desktop daemon, automatic wakeup и host quota не доказаны; human/commercial/release отдельно. Следующая задача PAOS-0046. [Execution report](research/product-agent-os-web-m1-execution-2026-11-11.md).

Датированный baseline 10 ноября:

PAOS-0001 реализован в границах адаптера. Persisted `thread/list` подтвердил 1/1/0/2 и project scope; свежая `vscode` история без preview остаётся partial. На текущем хосте `mxc` и `unelevated` вернули `ready`. MXC показал `availability: false`, а `command/exec` не запустил команду. PAOS-0054 остаётся `blocked`. Локальный probe требует подтверждённую пару write/deny. [Результаты и открытые проверки](research/product-agent-os-web-m1-initial-qualification-2026-11-10.md).

PAOS-0002 и PAOS-0003 реализованы в границах локальных контрактов. PAOS-0004 и PAOS-0040 имеют локально проверенную основу, integration и UI остаются открытыми. В PAOS-0039 проверена политика локального preview; AUTH-G1 ждёт коммерческого решения владельца. Статусы и команды закреплены в [карточках Web-плана](docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md) и JSON.

Продолжение M1: PAOS-0004 получил форму с восстановлением настроек и обработкой ошибок, PAOS-0040 подтвердил резервирование на двух синтетических процессах. PAOS-0054 проверил форму закреплённого протокола, семантику событий и файловые SQLite-возможности. Текущий runner подтвердил AppContainer/restricted token, точная стадия отказа PSEC неизвестна. Подтверждённого native write/deny нет, PAOS-0045 открыта. [Проверки и остаточные границы](research/product-agent-os-web-m1-initial-qualification-2026-11-10.md).

Ранее квалифицированные компоненты PAOS-0041, PAOS-0042 сохраняют исходные receipts; их исторический scope не переопределён новым маршрутом.

Исторические scope anchors PAOS-0031 сохраняют свой provenance.

## Подготовка control-plane к Web M1 — 2026-11-10

Source status: documentation maintenance; implementation_not_started.

PAOS-WEB-CONTROL-PLANE-PREP-2026-11-10: текущие scope/queue/checks/evals/handoff сведены к PRD v0.7 и execution v0.8. Предыдущие Web receipts и старый handoff перенесены в [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md); история и source owners сохранены. Это новый maintenance run, прежние test counts не являются его результатами.

Control-plane sync: REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md — update_required и обновлены. AGENTS.md — not_applicable: durable правила и claim ceiling достаточны; prod_test.md — not_applicable: Batch 39 evidence не менялось. Реализация, плановые task statuses, hooks/config и чужие session markers не изменялись.


## PAOS-AUD-G7 — closed / owner accepted, 2026-11-10

T08 завершена: владелец принял T06 и итоговое решение; G7 T01–T08 owner_accepted. Current docs 105 tests passed; frozen hashes, docs/matrix/state/diff passed. T07 runtime/model evidence reused unchanged. Fresh-session открыта отдельно. [Evidence](research/product-agent-os-g7-execution-report-2026-11-09.md).

## PAOS-AUD-G6 — 2026-11-09

G6 partially_verified: GAP-06 implemented / owner accepted 10.11.2026; все три synthetic local pilots приняты владельцем. HOST-01 не является их зависимостью. T34 no-go и fresh-session activation HOST-01/HOST-02 остаются открытыми отдельно; manual_only сохраняется. [Результаты](docs/superpowers/specs/paos-aud-g6-pilot-results.json).

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G5 — 2026-11-09

G5 F13/F14/F17 implemented_locally_verified: offline installer исправлен через RED/GREEN; README обновлён; local site rebuilt; 105 docs tests, 220 routes, 93 Mermaid renders passed. Self-review; no dependency install/publication/host activation. Следующая группа — G6. Текущий machine pointer — PLAN.md.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G4 — 2026-11-09

G4 F05/F09/F10/F15 implemented_locally_verified. Full final: 1326 tests, 540.818 s, OK (skipped=1), exit 0; final focused 253 OK; template contracts 95 OK; fixtures 91/91; transcripts 26/26; compatibility exit 0, local structure only. Self-review завершён. Inline intake, conditional references и inventory reuse проверены локально; следующий G5. Host/behavioral evaluation остаётся G6.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G3 — 2026-11-09

PAOS-AUD-G3: F03/F08/F16 implemented_locally_verified. Full unittest: 1320 tests, 725.771 s, OK (skipped=1); final focused 78 tests OK; fixture 91/91; transcript 26/26; compatibility passed (local structure only). Единственный current pointer — PLAN.md; B42/B45 preserved. Self-review завершён. Следующая группа — G4; semantic source review и actual host/promotion остаются отдельными gates.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G2 — 2026-11-09

PAOS-AUD-G2: F01/F02/F04 implemented_locally_verified: full 1305 tests OK (1 skip), final affected+docs 122 OK и final contracts 22 OK; fixture 91, transcript 26, compatibility/docs/hooks/diff passed. MCP wrapper, typed support/observation и read-only diagnostics добавлены; distribution/host/model promotion остаются отдельными gates. G1 и параллельная Web-документация сохранены. Self-review завершён; следующий шаг — G3.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## PAOS-AUD-G1 — 2026-11-09

PAOS-AUD-G1 локально закрыта: F06 command/patch guard, F12 hooks discovery/merge, F11 rules proposal, F07 exact ACL repair и F18 pinned report_authoring. Full discovery: 1297 tests, one skip, exit 0; affected 216 и final 67 после последнего alias fix passed; fixture 91/91, transcript 26/26, docs 100/100. Compatibility needs_review — прежний G2 gap. Hooks definitions/trust, реальные ACL, provider, target apply и Git не менялись. Следующая группа G2; host acceptance остаётся G6.

[Owning plan и evidence](docs/planning/product-agent-os-audit-remediation-task-plan-2026-11-09.md).

## Session lifecycle repair — 2026-11-09

`PAOS-SESSION-LIFECYCLE-2026-11-09`: implemented_locally_verified. Active/package PreToolUse, SessionStart and Stop select a session-bound marker; exact bootstrap replaces mention-based exemption. Full discovery: 1288 tests, one skip, exit 0; final focused: 236 passed; fixtures 91/91 and transcripts 26/26 (last Windows-case correction covered by focused suite). Hook validators, docs and diff checks pass. Current-host foreign-marker write denied, probe absent; own writes succeeded. Compatibility remains needs_review for existing legacy MCP format. [Owning record](research/product-agent-os-session-lifecycle-fix-2026-11-09.md) records RED/retests, provenance and fresh-host gap. No hook definitions/trust, sandbox or Web implementation change.

<!-- product-agent-os:start runlog -->

## Purpose

`RUNLOG.md` is the compact current-cycle handoff layer. It records latest routing, current evidence summary, residual risks and pointers. Detailed historical ledgers and batch marker banks belong in `docs/product-agent-os/control-plane-current-state.md`, source backlogs, evidence packets, registry entries and `prod_test.md`.

## Documentation refresh handoff — 2026-11-03

Task `PAOS-DOCS-REFRESH-2026-11-03`: documentation_implemented_locally_verified (20/20). Owner authorized saving the detailed plan and applying all 20 documentation corrections, checks and status updates. RU/EN plan validators passed at creation (exit 0). Initial combined suite: 224 tests, 15 failures/33 errors, including TEMP permissions, new-page counters and lifecycle pointer hardcoded to the August plan; both hook validators and docs checker passed. Source pages were refreshed through OpenAI Developer Docs. Agent validator still fails on the pre-existing sandbox_mode/default_permissions mismatch. No runtime/config/model/profile change is authorized or performed. Detailed evidence and final status are recorded in the [owning plan](docs/planning/2026-11-03-gpt6-documentation-refresh.md). Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG update_required and updated; prod_test.md not_applicable. No root-file overflow occurred.

The stale upper Batch 45 planning pointer was reconciled with its existing A06/task-group evidence: T28/T29 locally complete, T30 next; no Batch 45 implementation was performed.

Final documentation checks: docs 100/100, task-plan lifecycle 5/5, lifecycle hooks 25/25, infrastructure templates 94/94; both hook validators, docs checker, RU/EN plan validators, task-state consistency and diff check passed. Strict preview MkDocs exit 0. Hooks used isolated OS TEMP outside the repository after fixture/root discovery interference. Source review: 20 official pages; examples: 10 TOML/JSON blocks; 17 pre-existing dirty files preserved by hash. Only test inventory metadata was updated for three new pairs; no assertions weakened. Agent validator remains a known separate exit-1 diagnostic; no model/config/runtime promotion.

## Current Handoff

- Выполнена подготовка документационного control-plane под Web M1; implementation_not_started. Все 56 задач матрицы сохраняют planned, фактические start/end/duration — null.
- Следующий маршрут после запроса на реализацию: PAOS-0001 «Контракты и адаптеры проекта» → PAOS-0054 «Контракт совместимости M1 и runtime manifest». Входы: PRD §17, architecture §21, wireframes v0.7, [Web-план v0.8](docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md) и его JSON.
- PAOS-0054 должен подтвердить exact versions/hashes/schema/capabilities до зависимых consumers; при unsupported tuple зависимые задачи останавливаются и возвращаются на design review.
- PAOS-0045 принимает M1 по полной применимой матрице; PAOS-0046 — сразу после M1, PAOS-0036 — M2. Старые Batch/Track follow-ups не являются неявными prerequisites Web.
- Текущая проверка и предел доказательств: [аудит и архив control-plane](research/product-agent-os-control-plane-maintenance-2026-11-10.md). Исторические результаты не пересчитывались и не означают runtime/commercial acceptance Web.
- Предыдущий большой handoff перенесён в архив целиком; Source-Owned History Map ниже сохраняет owning artifacts. Batch 35 / Batch 38: `T10-LIVE-M41` — `owner_closed_no_op_git_release_pr`; `blocked_pending_explicit_cache_mutation_approval` — исторический статус. `B45-POSTQ4-T16-T22-A01`, `B45-POSTQ4-T17-A01`, `T14 is positive current-best-quality signal only` остаются historical/advisory evidence; no git stage/commit/push/PR.

## Source-Owned History Map

Distribution map: `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `AGENTS.md`, `docs/product-agent-os/control-plane-current-state.md`, `docs/sources/registry.md`, `docs/planning/product-agent-os-track-8-detailed-backlog.md`, `docs/planning/product-agent-os-track-9-backlog.md`, `docs/planning/product-agent-os-track-10-backlog.md`, `docs/sources/product-agent-os-batch35-approval-packet-draft.md`, `docs/planning/2026-06-20-track-11-documentation-architecture-refresh.md`, `docs/superpowers/specs/` and `prod_test.md`.

| History class | Source owner |
| --- | --- |
| Product-Agent OS Track 10 Task 26 Batch 35 approval-bound real testing execution matrix; no git stage/commit/push/PR; historical `done_through_m40` context | `docs/sources/product-agent-os-batch35-approval-packet-draft.md`; `docs/planning/product-agent-os-track-10-backlog.md` |
| B37/B38/B40/B41/B42 marker history | `docs/planning/product-agent-os-track-10-backlog.md`; `docs/product-agent-os/control-plane-current-state.md` |
| Batch 39 attempt/failure/fix/retest ledger | `prod_test.md`; B39 packets under `docs/superpowers/specs/` |
| Batch 44 Self-Learning Loop | `docs/planning/2026-06-20-track-11-documentation-architecture-refresh.md`; `docs/product-agent-os/self-learning-loop.md`; B44 packets |
| Batch 45 Professional Code Authoring | `docs/planning/2026-06-20-track-11-documentation-architecture-refresh.md`; `docs/product-agent-os/coding-standards.md`; B45 packets |
| Documentation refresh and DOC-M25 generated-site evidence | Track 11 plan; `docs/sources/registry.md`; DOC-M25 packet |
| Lifecycle hooks and control-plane sync | `.codex/config.toml`; `.codex/workflows/task-plan-lifecycle.md`; `.codex/workflows/control-plane-sync.md`; lifecycle hook packet |

## Current Product-Agent OS State

Исторические записи и результаты ниже относятся к указанным срезам. Они не меняют очередь Web M1 и не являются проверками текущего запуска. При расхождении используются текущие owning artifacts; перенос истории не закрывает оставшиеся gates.


| Workstream | Status | Notes |
| --- | --- | --- |
| Track 9 / Track 10 history | Source-owned historical context. | Use detailed backlogs and registry for historical claims. |
| Batch 39 | Owner-feedback route only. | Release readiness, runtime/browser proof and promotion are not claimed. |
| Batch 41 | Generated-artifact acceptance evidence through S9. | Release readiness, target apply safety, automation promotion and Cosmos.gl/WebGL runtime proof are not claimed. |
| Batch 42 | Planned-only. | Execution needs owner route decision. |
| Batch 44 | Staged/manual evidence through S7. | Promotion/automation decision remains pending. |
| Batch 45 | Advisory-only/no-go after T21 strict-schema abort and T22-A02; A03 is handoff readiness, A04 locally verifies T23/T24 and A05 locally verifies T25-T27 only. | Supersedes the historical Start B45-S9-C/T28 pointer: A04-A06 locally implement/focused-verify T23-T29; next is T30. T30-T34 remain dependency-ordered and T34 requires local readiness plus new exact approval. Runtime/browser/target/CI routes remain separately approval-bound. |
| Control-plane files | Compact current pointers. | Size pressure triggers `overflow_refactor_required`, not skipped updates. |

## Verification Runbook

For docs/control-plane edits, run:

```powershell
python -m unittest tests.product_agent_os.test_product_agent_os_docs -v
python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v
python -m unittest tests.product_agent_os.test_lifecycle_hooks -v
python -m unittest tests.product_agent_os.test_infrastructure_templates -v
python tools\check_docs.py
git diff --check
```

Strict MkDocs is required when navigation, Mermaid diagrams, Markdown extensions, MkDocs config, localized nav, search/sitemap behavior or generated `site/` evidence changes.

## Residual Risks

Web M1: PAOS-0054 native-offline tuple/driver/capabilities и synthetic migration/restore проверены; native vault/local auth проверены; actual provider/browser/owner acceptance и commercial gates остаются открытыми. Остальные риски ниже сохранены из прежних срезов и проверяются у их owners перед отдельным запуском. Указанные в них control-plane sync решения относятся к тем срезам.

- Batch 39 owner-feedback results and any runtime/browser pilot remain pending.
- `B38-PILOT-NF01` target apply remains blocked by source-policy and target-artifact gaps.
- Batch 40 completion-skeptic automation is still `manual_only` and `not_promoted`.
- Batch 41 has generated-artifact proof, not release/target-apply safety; Cosmos.gl/WebGL runtime remains unresolved.
- Batch 44 has no active automation, hidden telemetry, real session import, provider/model call, target mutation or auto-apply proof.
- Batch 45 remains advisory-only/no-go; A04 proves only the T23/T24 local contract gate, not implementation quality, CLI/runtime activation or promotion. Schema repair alone could recreate the self-scored, ceremony-heavy eval unless T25-T33 close. Control-plane sync: `PLAN.md`, `TEST.md`, `RUNLOG.md`, Track 11 and both registries updated; `REQUIREMENTS.md`, `EVALS.md` and `prod_test.md` are `not_applicable` because A04 changed neither product scope/eval thresholds nor Batch 39 evidence.
- GPT-5.6 remediation remains `implemented_with_gaps`: fresh-session `SessionStart` proof, same-effort/one-lower-effort behavioral quality/cost/latency evidence and cross-host portability of 18 user-level absolute skill paths are pending.
- Lifecycle hook hashes changed and therefore need explicit `/hooks` review/trust plus a fresh-task activation check; until then the claim is `implemented_not_runtime_verified`, and direct script benchmarks must not be promoted to App latency evidence.
- Historical detail has been intentionally moved out of root control-plane files; broad historical claims must cite source backlogs, registry or evidence packets.

<!-- product-agent-os:end runlog -->

Текущий slice: T10 принят владельцем; T11–T16 проверены; T17 принят; G9 закрыта. Baseline `eb4a74688c9df96e2481e653cd144b2a07f39d03` сохранён до edits; команды и результаты — [G9 report](research/product-agent-os-g9-execution-report.md). Fresh-session activation отдельно.
