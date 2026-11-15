# Backup, обновление и rollback

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: runtime/operations owner + docs-maintainer. Область: local desktop package на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении launcher, CLI, snapshot или release gates. Ссылки на тесты — маршруты проверки, не новый прогон. Реальные профили, credentials и provider не исследовались.

Сначала штатно остановите owned service и подтвердите результат owned launcher; CLI status показывает selection и digest, а не факт остановки сервиса. [CLI](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/main.mts) задаёт два отдельных вызова:

- `node apps/desktop-local/main.mts backup --install <install> --expected-id <reviewed-id> --profile <stopped-profile> --output <existing-backup-directory>` создаёт проверяемый snapshot SQL и связанных blobs.
- `node apps/desktop-local/main.mts restore --install <target-install> --expected-id <target-id> --backup <snapshot> --profile <new-profile>` проверяет snapshot и восстанавливает только в новый профиль.

Для обновления: backup → проверить целевой package → установить его в новый целевой каталог (или использовать уже проверенный target install) → restore в новый профиль целевой версией → select с текущим `--expected-selection <digest>` → start. Для rollback выберите совместимый snapshot и восстановите прежней версией в ещё один новый профиль, затем select с текущим digest. Не открывайте текущую БД старым кодом in-place и не обходите ошибки schema/hash. Snapshot отражает своё время: более поздние изменения могут отсутствовать.

Backup исключает файлы проекта, credentials, runtime auth и threads; после restore нужна повторная привязка. Старые версии, профили и исходный backup сохраняются; неуспешный непустой новый профиль остаётся для сверки. Автоматического retention/удаления нет. [Storage contract](../db/backup-restore.md), [distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts), [tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/storage-backup.test.mts). Исторические тесты не доказывают восстановление конкретных пользовательских данных.
