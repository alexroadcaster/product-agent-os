# Подготовка, запуск и остановка

Source status: repository_source / static_contract_review; 15.11.2026.; FUNC-G06 managed delivery locally_verified_with_explicit_limits, 16.11.2026.

Владелец: runtime/operations owner + docs-maintainer. Область: local desktop package на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении launcher, CLI, snapshot или release gates. Ссылки на тесты — маршруты проверки, не новый прогон. Реальные профили, credentials и provider не исследовались.

Команды ниже — справочник [desktop CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts), а не результаты их запуска. Все пути — абсолютные локальные, без linked ancestors; package и install не размещают в node_modules. Предварительные условия host/runtime сверяются с manifest; не устанавливайте отсутствующие компоненты автоматически.

## FUNC-G06 / F17 — один managed-home

Новый private local-pilot user-space installer использует portable package без системной установки и автоматической установки runtime. Из пакета выполните `node apps/desktop-local/main.mts setup --home <home> --package <package> --expected-id <reviewed-id> --expected-selection none`. `managed-status --home <home>` возвращает selection/digest и фазу операции. Обновление: `update --home <home> --package <new-package> --expected-id <reviewed-id> --expected-selection <digest>`; откат: `rollback --home <home> --expected-id <previous-id> --expected-selection <digest> --backup <compatible-snapshot-under-home-backups>`. `managed-start --home <home>` запускает выбранную installation. Каталоги versions/profiles/backups выводятся из home.

Перед переключением выполните Quit owned service. Maintenance текущего профиля охватывает snapshot, restore и selection; для цели создаётся новый профиль. Старые профили/версии/backups сохраняются. Явно выбранный rollback snapshot определяет data cutoff: для сохранения post-update изменений нужен свежий совместимый backup. Неверные host tuple/schema, stale digest, live/residual reservations и tampered artifacts дают отказ без fallback. Потерянное подтверждение после commit диагностируется как selection_committed_receipt_pending. Unresolved locks требуют сверки, без автоматического удаления/replay. Низкоуровневые команды сохранены ниже.

| Действие | Команда из корня checkout/package, содержащего `apps/` |
| --- | --- |
| UI build | `npm run build:web` в checkout с согласованными зависимостями |
| Package | `node apps/desktop-local/main.mts pack --source <source> --output <new-package>` |
| Verify | `node apps/desktop-local/main.mts verify --package <package> --expected-id <reviewed-id>` |
| Install | `node apps/desktop-local/main.mts install --package <package> --destination <new-install> --expected-id <reviewed-id>` |
| Выбор | `node apps/desktop-local/main.mts select --state <control> --install <install> --expected-id <reviewed-id> --profile <profile> --expected-selection none` для первого выбора |
| Статус / старт | `node apps/desktop-local/main.mts status --state <control>`; `node apps/desktop-local/main.mts start --state <control>` |

Перед verify независимо проверьте releaseId: self-hash пакета не устанавливает издателя. Destination для pack/install должен быть новым; install/profile/control не пересекаются. Последующие select требуют текущий digest из status вместо `none`, иначе conflict. После переноса CLI доступен внутри установленного каталога. [Distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts), [launcher](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/launcher/launcher.ts), [тесты](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts).

Native launcher открывает браузер и запускает локальный сервис в рамках выбранного профиля. Закрытие вкладки не останавливает backend: используйте штатный **Quit** в приложении, дождитесь завершения owned service. Pairing/session данные не помещайте в URL или отчёты. Отказ host qualification, устаревший сервис или невыполненный Stop требуют диагностики, а не обхода проверок. См. [диагностику](troubleshooting.md) и [исторический pilot](../web/pilot.md).

Сохранность профиля означает неизменность исходных bytes базы/blobs/settings/credential files. Snapshot reads могут создавать отдельно зафиксированные empty WAL/derived SHM; полное равенство directory inventory не заявляется. Maintenance reservations координируют managed launchers и не являются OS sandbox против произвольных SQLite writers. [Backup contract](../db/backup-restore.md).
