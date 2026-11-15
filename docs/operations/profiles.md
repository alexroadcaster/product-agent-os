# Профили и владение путями

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: runtime/operations owner + docs-maintainer. Область: local desktop package на `259977f3b257ba7fc0e932396f8963262bd327ad`; обновлять при изменении launcher, CLI, snapshot или release gates. Ссылки на тесты — маршруты проверки, не новый прогон. Реальные профили, credentials и provider не исследовались.

[Distribution](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/desktop-local/distribution.mts) разделяет install, profile и control state; локальные абсолютные пути проверяются на ссылки, взаимные пересечения и физическую identity. [Profile identity](../security/auth-credentials.md) отдельно определяет namespace credentials: копирование или restore данных не переносит его автоматически. Workspace не включается в пакет или backup.

Выбор хранит releaseId, profile и digest. Первый выбор требует `--expected-selection none`; последующий использует digest текущего status. CAS защищает от незамеченного изменения selection. `select`, backup и restore используют общую с launcher reservation профиля, включая параллельный запуск с другим control state. Занятый или невыясненный профиль не следует считать свободным.

Профиль при restore создаётся новым, старый сохраняется. Workspace bindings не переписываются; credentials и runtime auth подключаются заново, approvals становятся stale, незавершённые runs/outbox — recovery_required. Проверки [desktop-local](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/desktop-local.test.mts) и [backup](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/storage-backup.test.mts) используют synthetic данные; фактическая сохранность конкретного профиля требует отдельного подтверждения. Не храните реальные пути и секреты в диагностическом отчёте.
