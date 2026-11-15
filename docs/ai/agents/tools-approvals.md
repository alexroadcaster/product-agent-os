# Инструменты, approvals и Stop

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: runtime/agent owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении селектора, gateway, контрактов, границ исполнения или связанных тестов. Описанные тесты — маршруты проверки, не новый прогон; фактическая активация и human acceptance требуют отдельного evidence.

## Browser и private channel

[application.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/http/application.mts) обслуживает browser API с session/origin/CSRF. [app-agent-channel.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-channel.mts) отдельно принимает POST на loopback origin с instance capability и проверками host/origin, content type и размера. Cookie браузера не предоставляет право attach/claim/report; capability и lease tokens нельзя помещать в URL, docs или отчёты. Граница снижает смешение полномочий, но не доказывает изоляцию произвольных native клиентов.

## Mediated command

В [app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) worker в execution job предлагает operation; она имеет ID, digest, generation, expiry и состояние awaiting_approval. Approve проверяет run/binding/generation, срок, текущее состояние, ownership и task/autonomy boundaries. Повтор того же решения возвращает существующее состояние, конфликт отклоняется. При accept повторно проверяется lease, затем начинается dispatch через [sandbox-broker.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/sandbox-broker.mts); decline/cancel не запускают команду. Условия и action-level API — [API endpoints](../../api/endpoints.md).

Broker scope относится к PAOS-mediated commands; собственные инструменты App host не становятся автоматически ограничены этим broker. Заявленный hostIdentity attested, не cryptographic. Выполнение/вывод broker и file observations имеют собственную coverage; предложение, approval и завершение различаются. [policy.ts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/web/src/api/policy.ts) — UI preflight, server остаётся владельцем проверки.

## Stop и неопределённость

Stop queued job может дать interrupted, для уже активного — cancel_requested и cooperative interrupt. Нельзя утверждать завершение до соответствующего наблюдения. При recovery_required неизвестная native operation не replay; `cancel_undispatched` возможен только при доказанном отсутствии dispatch и действующей привязке worker/generation. [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts), [app-agent-channel.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-channel.test.mts), [recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/recipe-recovery.test.mts) — тестовые маршруты, не новый запуск. Подробности: [backend recovery](../../backend/recovery.md).
