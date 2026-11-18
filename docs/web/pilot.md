# Локальный пакет и пилот Web

Настройки, 13.11.2026: «Выбрать папку проекта» открывает Windows Explorer с выбором/созданием папки. Затем «Добавить проект» регистрирует её и показывает bounded scan JS/TS и project sources; unsupported/partial coverage — на Карте. Отмена ничего не добавляет. «Подключить Codex App» открывает draft: отправьте подготовленный запрос в Codex App и вернитесь; attached worker обновит статус. Одно открытие окна не означает подключение или model access. Для обновления остановите прежний экземпляр штатным Quit, выполните `npm run build:web` и запустите launcher с тем же профилем. [Контракт и текущие проверки](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m1-execution-2026-11-11.md).


Source status: project-authored / PAOS-0030 local delivery contract; technical receipts belong to the owning execution report.; FUNC-G06 current contract, locally_verified_with_explicit_limits, 16.11.2026.

Пакет предназначен для локальной инженерной работы на закреплённом Windows/x64 host tuple. Он содержит launcher, local-service, contracts, собранный Web UI и минимальный runtime parser. Node и Codex binaries, профиль, credentials и workspace в него не входят. Собственная лицензия PAOS, admission и коммерческие условия остаются отдельными gates; локальная сборка не разрешает внешний выпуск.

## FUNC-G07 / F23 — протокол продуктовой приёмки, редакция 1 {#func-g07-pilot-protocol}

Source status: project-authored protocol proposal, 16.11.2026; participants_not_defined; consent_not_observed; human_pilot_not_started. Владелец сообщил, что участники пока не определены. F23 — `awaiting_user_decision` («Ожидание решения пользователя»); технические проверки F19/F24 не заменяют этот gate. [Карточки и текущие статусы](../planning/functional-remediation-2026-11-15.md#func-g07-results).

Это подготовленный протокол для согласования до первого наблюдения. Владелец выбирает пять участников, наблюдателя и владельца данных; P01–P05 — будущие псевдонимные слоты, а не проведённые сессии. Требуются добровольный opt-in, согласованные сценарии, baseline и срок хранения. Один владелец может дать exploratory feedback, но n=1 не пересчитывает цели4/5 и3/5 из PRD. При отсутствии участников запуск и product acceptance не заявляются.

Решение владельца 16.11.2026: пользователь самостоятельно проверяет результат и даёт обратную связь. Следующее действие — обратная связь и решение пользователя. Исходные AC и протокол ниже сохранены как предложение для последующего решения владельца; передача проверки не означает приёмку или закрытие.

### Границы и данные

Предлагаемый scope — локальный UI на зафиксированных build/fixture revisions, синтетические проекты, без credentials, production data и provider/model calls. До пилота отдельно согласуются потребности доступности, язык и устройство. Подготовка и запуск локального сервиса фиксируются отдельно от времени поиска решения. В итогах сохраняются только participant ID, время, исход, помощь, ошибки и ссылки на обезличенные receipts. Имена, контакты, тексты частных задач, код, абсолютные личные пути, chat logs, pairing/session secrets, аудио и видео не собираются.

Предложение retention — удалить подробные локальные записи вручную через30дней после owner decision, сохранив только согласованные обезличенные агрегаты. Это не действующая automation/TTL. Владелец данных, конкретная дата удаления, withdrawal procedure и scope согласия заполняются до сбора. До opt-in каталога с human receipts не создаётся. При отзыве прекратить сбор и исполнить согласованное удаление; отсутствие наблюдения остаётся missing, не success. Публикация и передача записей внешнему сервису требуют отдельного решения.

### Baseline и нейтральные сценарии

По PRD baseline выполняется **до UI**. Предлагается `md_readonly`: обычный редактор/поиск и те же синтетические MD/source данные без интерфейса PAOS. Это не actual chat/model baseline. Если нужен интерактивный chat, сначала требуется отдельный согласованный маршрут и authority. Для уменьшения запоминания подготовить равносложные A/B задачи: P01/P03/P05 — MD-A → UI-B, P02/P04 — MD-B → UI-A. Порядок обучения baseline→UI, прошлое знакомство и различие задач остаются confounders; преимущества продукта заранее не предполагаются. Наблюдатель хранит правильные ответы отдельно и не подсказывает названия вкладок.

| Сценарий | Нейтральное задание участнику | Наблюдение |
| --- | --- | --- |
| Первое открытие / возвращение | «Вы вернулись после перерыва. Определите текущую работу, blocker, основание статуса и следующий шаг» | Все три ответа: task, blocker/next action, evidence level; время без помощи |
| Обычный файл | «Добавьте выбранную папку и найдите файл, который нужно изменить» | Folder selection/cancel, дерево вне Control-plane; видимость ≠ indexing ≠ execution |
| Карта и данные | «Найдите место изменения хранения поля и объясните выбранный источник» | Map → schema/table/ERD → usages → source line; confirmed/inferred/unresolved и неподдерживаемая семантика |
| Ограниченное покрытие | «Достаточно ли доступных данных для следующего действия? Объясните» | Empty, excluded, unsupported, partial; не называть проект полностью проанализированным |
| Конфликт / устаревание | «Источник изменился. Продолжите, сохранив работу» | Stale revision, draft preservation, допустимый refresh/retry |
| Остановка / возврат | «Прервите действие и вернитесь после перезапуска» | Cancel/retry/restart, неизвестный исход не приравнивать выполнению |
| Приёмка | «Что вы можете принять на основании этих данных, и почему?» | Checks/run evidence отдельно от owner acceptance; verified трактуется в своём scope |

После timed попытки спросить о **конкретном прошлом опыте**: как участник находил это раньше, что потребовало помощи и какой источник привёл к решению. Не спрашивать «нравится ли PAOS» и не подсказывать правильный ответ до фиксации ошибки. Ошибка остаётся в receipt после объяснения; повтор относится к новой диагностической попытке.

### Метрики и правила решения

Основная гипотеза: минимум4из5 участников за180секунд первой попытки без помощи правильно называют текущую задачу, blocker/следующий шаг и evidence level. Ошибка, timeout, помощь и missing остаются в знаменателе; повтор не заменяет первую попытку. Время запуска сервиса указывается отдельно. Baseline/UI сравниваются по успешности и времени на сопоставимых сценариях; технический benchmark не является human measurement.

Вторая гипотеза: минимум3из5 **разных** участников повторно используют продукт для **другой реальной задачи** в индивидуальном окне `first_use_at + 14 days`. Запланированный технический клик и повтор fixture не считаются reuse. До завершения окон не записывать их как прошедшие. Обезличенный reuse receipt фиксирует факт другой работы без её приватного содержимого; отсутствие подтверждения остаётся unobserved. Ни одного такого наблюдения сейчас нет.

Guardrails: ноль ложных трактовок `verified` и ноль потерь данных. Ошибки, отказы и несоответствия протоколу записываются вместе с успехами. При изменении UI/build создать новую revision и сохранить прежние результаты; не перезаписывать неуспешную попытку. Если число участников/сценарии/срок меняются, сохранить исходные AC и оформить отдельное решение владельца; это не закрывает обязательный исходный F23 автоматически.

### Форма будущего receipt и owner decision

Поля receipt пока **не заполнены**: `protocol_revision`, `build_or_release_id`, `fixture_revision`, `participant_id`, `prior_familiarity`, `consent_scope`, `consent_observed_at`, `observer_id`, `data_owner`, `baseline_mode`, `baseline_variant`, `ui_variant`, `scenario_id`, `started_at`, `elapsed_seconds`, `current_task_correct`, `blocker_next_action_correct`, `evidence_level_correct`, `assistance`, `outcome`, `misinterpretation`, `data_loss_observed`, `protocol_deviation`, `first_use_at`, `reuse_window_end`, `distinct_real_task_reuse_observed_at`, `reuse_evidence_ref`, `retention_delete_at`. `null` означает «не наблюдалось», а не ноль, согласие или успех.

После согласия подробные локальные receipts могут храниться в ignored `.docs-tools/reports/func-g07/human-pilot/`; canonical docs получают только согласованные агрегаты и решение. Owner form: revision/build/fixture, actual cohort и согласия, baseline comparison, numerator/denominator и missing, ошибки/потери, реальные reuse windows/evidence, решение `accept` / `reject` / `further_evidence_required`, owner/date. Сейчас decision=`not_observed`, cohort=`not_defined`. Следующий шаг — самостоятельная проверка пользователя, его обратная связь и решение; исходный протокол сохранён для этого решения. Рассылка, schedule и provider вызовы этим документом не запускаются.

## FUNC-G06 / F17 — управляемая локальная поставка

Текущее дополнение — private_local_pilot managed installer с setup/update/rollback и одним managed-home. CLI выводит каталоги versions/profiles/backups, проверяет ожидаемые release/selection identities и сохраняет старые версии и исходные bytes профилей. Maintenance охватывает transfer; managed-start использует порядок home→selection lock, поэтому unresolved home operation запрещает запуск. См. [команды установки](../operations/install-start-stop.md) и [решения/evidence G06](../planning/functional-remediation-2026-11-15.md#func-g06-results).

Qualification запускает actual relocated installations A/B/A через production NativeLauncher IPC и local-service в fresh disposable user-space environment. Window host — управляемый browser callback, это не actual native-window/SmartScreen test. Real HTTP readback task/comment/attachment/preferences, installed HTML markers, разные profile identities и явно свежий rollback snapshot подтверждают данные и activation выбранного пути; checkout fallback и provider calls отсутствуют. SQL session-message preservation отдельно проверена F22.

Hashes исходных файлов сохраняются; новые empty WAL/derived SHM фиксируются отдельно по [контракту SQLite backup](../db/backup-restore.md). Это не новый OS account/SID и не коммерческий/публичный release. Исходный pilot12.11.2026 ниже остаётся историческим evidence, а не новым прогоном.

## Подготовка и установка

1. Соберите Web UI командой `npm run build:web` из исходного workspace. Используйте уже согласованные зависимости и Node.
2. Вызовите `node apps/desktop-local/main.mts pack --source <absolute-source> --output <new-absolute-package>`. Команда создаёт каталог и `distribution.json`: releaseId, SHA-256 каждого файла, runtime dependencies и точные Node/OS/SQLite prerequisites. Она не меняет исходники, PATH или registry и не запускает сервер.
3. Отдельно проверьте build receipt и его releaseId. Self-hash не подтверждает издателя. Выполните `verify --package <package> --expected-id <reviewed-release-id>` тем же CLI. Не принимайте digest из непроверенного пакета как независимое подтверждение.
4. Выполните `install --package <package> --destination <new-install-directory> --expected-id <reviewed-release-id>`. Назначение должно быть новым; существующая версия не перезаписывается. Копируются только файлы manifest, затем сверяются hashes.
5. Создайте отдельный пустой профиль. Для первого выбора выполните `select --state <control-directory> --install <install-directory> --expected-id <reviewed-release-id> --profile <profile-directory> --expected-selection none`. Каталоги install, profile и control не должны пересекаться.
6. `status --state <control-directory>` показывает текущую selection и digest. `start --state <control-directory>` проверяет пакет и host prerequisites, затем вызывает существующий native launcher. Несовпадение не приводит к автоматической установке или fallback. Пакет нельзя размещать под node_modules: Node не выполняет там TypeScript source entrypoints.

Все filesystem paths в командах — абсолютные локальные пути. CLI находится внутри установленной версии по `apps/desktop-local/main.mts`; после переноса исходный checkout не нужен. Launcher сразу открывает `/launch` в системном браузере, без диалогов и ручного кода. Одноразовый HttpOnly challenge и same-origin POST создают session; URL/stdout не содержат секретов. Вход требует Fetch Metadata прямой пользовательской навигации; native HTTP clients этим не изолируются. Старый service сообщает `service_restart_required`: завершите прежний экземпляр через Quit и повторите запуск с тем же профилем. Закрытие вкладки оставляет backend работающим; используйте Quit в приложении. Default browser может использовать существующий profile; автоматические проверки используют disposable profiles. [Контракт и evidence](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-m1-execution-2026-11-11.md#%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA-%D0%B1%D0%B5%D0%B7-%D1%80%D1%83%D1%87%D0%BD%D0%BE%D0%B3%D0%BE-%D1%81%D0%BE%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F--2026-11-13).

Для графа включены закреплённые Rolldown1.2.18, Win32/x64 binding1.2.18, pluginutils1.1.0 и oxc types0.156.0. Их версии сверяются с package-lock, файлы и notices — с manifest. Полный node_modules и build toolchain не поставляются. React/React DOM/Scheduler notices находятся в `apps/desktop-local/THIRD_PARTY_NOTICES.txt`; лицензии parser сохраняются рядом с его package. Полнота transitive native license audit остаётся выпускным gate.

## Backup, восстановление и rollback

| Операция | Контракт |
| --- | --- |
| backup | `backup --install <install> --expected-id <id> --profile <stopped-profile> --output <existing-backup-directory>` создаёт проверяемый snapshot SQL и referenced blobs. Не включает workspace files, credentials, runtime auth/threads или профильную identity |
| restore | `restore --install <target-install> --expected-id <target-id> --backup <snapshot-directory> --profile <new-profile>` проверяет schema, hashes, blobs, integrity/FK; существующий профиль не заменяется |
| обновление | Остановить owned service → backup → restore новой версией в новый профиль → select с текущим `--expected-selection <digest>` → start |
| rollback | Выбрать совместимый snapshot → restore прежней версией в ещё один новый профиль → select с текущим digest → start. Обе версии и предыдущие профили сохраняются |

Выбор snapshot определяет границу данных. Для сохранения изменений после обновления сначала сделайте новый snapshot и проверьте его совместимость с прежней версией. Не открывайте старым кодом текущую БД «на месте» и не редактируйте schema manifest ради обхода отказа.

Select/backup/restore занимают общую с launcher атомарную reservation `profile/service-instance`; конкурентный запуск через другой control directory также отказывается. Не удаляйте reservation или `operation.lock`, пока не сверено завершение владельца. Неоднозначное завершение требует ручной сверки. Источник backup и старые профили сохраняются; автоматическая очистка версий/retention не выполняется.

Restore меняет stream generation, помечает approvals как stale, незавершённые runs/outbox — recovery_required. Новая физическая profile identity не наследует credential namespace. Переносится только внутренняя запись `_paos_profile`, чтобы настройки интерфейса соответствовали новому каталогу; bindings реальных workspace не меняются. Повторное сопряжение обязательно. При ошибке непустой новый профиль остаётся для диагностики, активная selection не переключается.

## Согласованный пилот и пределы выводов

Для PAOS-0030 владелец отдельно выбрал копию codex_docs, оригинал — read-only в течение пилота. Используется ограниченный снимок14реальных файлов: control-plane, UI/task/workflow/graph source и руководство доступности. В копии создаются pilot task, комментарии и синтетический attachment; проверяются PLAN reader, lexical graph, переключение языка/темы и перенос данных через два content revisions и rollback. Hashes оригиналов сравниваются до/после пилота; исходный проект не редактируется этим сценарием. Поздние control-plane изменения самой задачи учитываются отдельно.

Технические наблюдения доказывают конкретные действия и сохранность проверенных данных. Они не доказывают удобство для широкой аудитории, полезность на всех проектах, качество модели, human product acceptance или production readiness. Эти выводы остаются гипотезами до отдельной оценки владельцем. Provider calls и реальные secrets не нужны для этого пилота. AUTH-G1–G6 повторно сверены; нерешённые коммерческие/лицензионные/account/privacy/support gates сохраняют запрет соответствующего выпуска.

Evidence из корня репозитория: `research/product-agent-os-web-m4-0030-execution-2026-11-12.md`, companion results JSON и `docs/release/web-m4-local-release.json`. При ошибке сохраните код отказа, releaseId и redacted receipt; не копируйте pairing code или credentials в отчёт. Ответственный за локальный incident — maintainer workspace; коммерческие SLA и support обязательства здесь не устанавливаются. См. также [доступность Web](accessibility.md) и [границы runtime](../diagrams/runtime-decision-map.md).
