# Локальный пакет Product-Agent OS

Source status: project-authored / local packaging contract, PAOS-0030.

Переносимый каталог содержит launcher, local-service, contracts, Web dist и SHA-256 manifest. Node/Codex binaries, profiles, credentials и workspaces не включаются. Для карты исходников копируются только установленные и закреплённые Rolldown1.2.18, Win32/x64 native binding1.2.18, pluginutils1.1.0 и oxc types0.156.0; остальной node_modules не включается. Требования Node/OS/SQLite закреплены manifest; несовпадение останавливает Start. Native qualification и доступ к модели проверяются отдельно. Signed installer, системная установка и допуск коммерческого распространения не заявлены.

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
