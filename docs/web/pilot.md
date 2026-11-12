# Локальный пакет и пилот Web

Source status: project-authored / PAOS-0030 local delivery contract; technical receipts belong to the owning execution report.

Пакет предназначен для локальной инженерной работы на закреплённом Windows/x64 host tuple. Он содержит launcher, local-service, contracts, собранный Web UI и минимальный runtime parser. Node и Codex binaries, профиль, credentials и workspace в него не входят. Собственная лицензия PAOS, admission и коммерческие условия остаются отдельными gates; локальная сборка не разрешает внешний выпуск.

## Подготовка и установка

1. Соберите Web UI командой `npm run build:web` из исходного workspace. Используйте уже согласованные зависимости и Node.
2. Вызовите `node apps/desktop-local/main.mts pack --source <absolute-source> --output <new-absolute-package>`. Команда создаёт каталог и `distribution.json`: releaseId, SHA-256 каждого файла, runtime dependencies и точные Node/OS/SQLite prerequisites. Она не меняет исходники, PATH или registry и не запускает сервер.
3. Отдельно проверьте build receipt и его releaseId. Self-hash не подтверждает издателя. Выполните `verify --package <package> --expected-id <reviewed-release-id>` тем же CLI. Не принимайте digest из непроверенного пакета как независимое подтверждение.
4. Выполните `install --package <package> --destination <new-install-directory> --expected-id <reviewed-release-id>`. Назначение должно быть новым; существующая версия не перезаписывается. Копируются только файлы manifest, затем сверяются hashes.
5. Создайте отдельный пустой профиль. Для первого выбора выполните `select --state <control-directory> --install <install-directory> --expected-id <reviewed-release-id> --profile <profile-directory> --expected-selection none`. Каталоги install, profile и control не должны пересекаться.
6. `status --state <control-directory>` показывает текущую selection и digest. `start --state <control-directory>` проверяет пакет и host prerequisites, затем вызывает существующий native launcher. Несовпадение не приводит к автоматической установке или fallback. Пакет нельзя размещать под node_modules: Node не выполняет там TypeScript source entrypoints.

Все filesystem paths в командах — абсолютные локальные пути. CLI находится внутри установленной версии по `apps/desktop-local/main.mts`; после переноса исходный checkout не нужен. Native окно передаёт pairing code через IPC/stdin, без URL/stdout. После Cancel сервер штатно останавливается. Обычный OK открывает локальный UI в системном браузере; этот путь может использовать существующий browser profile, поэтому для автоматических проверок применяются disposable browser profiles.

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
