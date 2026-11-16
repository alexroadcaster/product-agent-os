# Локальный пакет Product-Agent OS

Source status: project-authored / local packaging contract, PAOS-0030; FUNC-G06 managed delivery contract, 16.11.2026; current qualification belongs to the owning functional matrix.

Переносимый каталог содержит launcher, local-service, contracts, Web dist и SHA-256 manifest. Node/Codex binaries, profiles, credentials и workspaces не включаются. Для карты исходников копируются только установленные и закреплённые Rolldown1.2.18, Win32/x64 native binding1.2.18, pluginutils1.1.0 и oxc types0.156.0; остальной node_modules не включается. Требования Node/OS/SQLite закреплены manifest; несовпадение останавливает Start. Native qualification и доступ к модели проверяются отдельно. Signed installer, системная установка и допуск коммерческого распространения не заявлены.

## Управляемый private local-pilot installer — FUNC-G06 / F17

Канал — `private_local_pilot`, формат — user-space установка portable каталога через Node CLI, подпись — `unsigned`. SHA256/releaseId проверяют integrity, не личность издателя. Node/Windows/SQLite prerequisites уже должны соответствовать exact manifest; автоматической установки runtime, системной интеграции и публичного/коммерческого выпуска нет. AUTH/licensing gates сохраняются.

Один `--home` заменяет ручной выбор каталогов версий, профилей, backups и selection. Все пути абсолютные, локальные и непересекающиеся с package; releaseId получают из отдельно проверенного build receipt.

| Действие | Команда после `node apps/desktop-local/main.mts` |
| --- | --- |
| Первая установка | `setup --home <managed-home> --package <package> --expected-id <reviewed-release-id> --expected-selection none` |
| Проверка состояния | `managed-status --home <managed-home>` |
| Обновление | `update --home <managed-home> --package <new-package> --expected-id <new-reviewed-release-id> --expected-selection <current-digest>` |
| Откат | `rollback --home <managed-home> --expected-id <previous-reviewed-release-id> --expected-selection <current-digest> --backup <compatible-snapshot-under-home-backups>` |
| Запуск выбранной версии | `managed-start --home <managed-home>` |

`managed-status` возвращает текущую selection/digest, фазу операции и nextAction. Перед update/rollback завершите owned service штатным Quit. Update автоматически создаёт backup текущего профиля и restore целевой версией в новый профиль; source maintenance reservation удерживается до selection commit. Новый профиль также reserved до commit. Tuple mismatch проверяется до установки/selection, schema mismatch — при restore. Старые профили, версии и backups сохраняются, in-place downgrade отсутствует.

Rollback принимает совместимый snapshot явно: он задаёт границу восстановленных данных. Чтобы сохранить post-update изменения, сначала создайте свежий backup через низкоуровневую `backup` команду ниже и передайте его в rollback; несовместимость не обходится. Потеря финального operation receipt после commit отражается как `selection_committed_receipt_pending`, а не обещание неизменённой selection. При process death оставшийся operation.lock требует сверки; команды не удаляют его и не воспроизводят операцию автоматически.

Сценарий clean Windows profile в F17 — disposable PAOS profile и fresh user-space environment на текущей Windows account, без создания нового account/SID. Launcher передаёт только разрешённые home/temp path variables в service child, без provider secrets/NODE_OPTIONS. Native-window, SmartScreen/signature trust, model access и human acceptance требуют отдельных evidence.

Низкоуровневые команды ниже сохраняются для диагностики и явного выбора snapshot. Qualification и ограничения находятся в исходном workspace: `docs/planning/functional-remediation-2026-11-15.md`, раздел FUNC-G06; документация не входит в portable artifact.

CLI: `node apps/desktop-local/main.mts <command> <flags>`. Пути абсолютные, локальные, без linked ancestors и node_modules.

| Команда | Обязательные flags |
| --- | --- |
| pack | `--source`, `--output` (новый каталог) |
| verify | `--package`, `--expected-id` (отдельно проверенный releaseId) |
| install | `--package`, `--destination` (новый каталог), `--expected-id` |
| select | `--state`, `--install`, `--expected-id`, `--profile`, `--expected-selection` (`none` для первого выбора) |
| status / start | `--state` |
| backup | `--install`, `--expected-id`, `--profile`, `--output` (существующий каталог) |
| restore | `--install`, `--expected-id`, `--backup`, `--profile` (новый каталог) |

Для обновления и rollback остановите owned service, сделайте backup, восстановите его в новый профиль целевой версией, выполните select с текущим digest. Старые application/profile каталоги сохраняются. Schema/hash ошибки не обходятся. Snapshot может исключить изменения после его времени; snapshot выбирает оператор. Backup содержит SQL/referenced blobs, исключая repository files, credentials, runtime threads/auth и profile identity. Новый профиль переподключается отдельно.

Start использует native окно launcher; pairing code идёт IPC/stdin, без URL/stdout. `service-instance` или `operation.lock` требуют сверки завершения, а не принудительного удаления. Удаление старых версий, retention, auto-update и публикация автоматически не выполняются.

Select/backup/restore используют атомарную reservation `profile/service-instance`, общую с native launcher; запуск через другой selection state также блокируется на время maintenance. Удаляется только собственная пустая reservation с проверкой filesystem identity. При неуспешном restore непустой новый профиль сохраняется для сверки, его файлы автоматически не удаляются.

Web bundle содержит React, React DOM и Scheduler; их точные MIT notices приведены в `THIRD_PARTY_NOTICES.txt`. Runtime parser сохраняет LICENSE и THIRD-PARTY-LICENSE установленного Rolldown и лицензии его dependencies. Полный аудит transitively linked native компонентов, собственная лицензия PAOS и коммерческая квалификация остаются выпускными gates. Внутренний пакет не предоставляет права публичного распространения, доступ к подписке или моделям. Исходники не защищены от редактирования ОС: «immutable» означает отсутствие in-place update и обязательную проверку digest.
