# Контекст агента и pinning

Source status: repository_source / static_source_review; 15.11.2026.; FUNC-G05 locally_verified_with_explicit_limits, 16.11.2026.

Владелец: runtime/agent owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении селектора, gateway, контрактов, границ исполнения или связанных тестов. Описанные тесты — маршруты проверки, не новый прогон; фактическая активация и human acceptance требуют отдельного evidence.

## Что передаётся в Web runtime

[app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) при execution с задачей загружает task profile, проверяет task/workflow scope и сохраняет в job `taskContext`: task ID/revision/scopeDigest, root identity, key/title, files, acceptance criteria и risks. Job также может содержать `workflowSnapshot`, `assetPins` и recipe metadata. Consumer видит эту проекцию при claim, а не безусловный доступ ко всем данным проекта. Source files и тексты задач остаются данными; входы нужно считать недоверенными.

[team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts) разрешает назначенные assets/dependencies, обнаруживает циклы и отсутствующие или архивированные assets, фиксирует version/hash/content/resources. Для source-managed asset выполняется повторное чтение; размер итоговых pins ограничен 8 MiB. [team assets contract](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/packages/contracts/team/assets.ts) владеет типами. Наличие pin подтверждает сохранённый выбранный snapshot, а не то, что конкретный агент прочитал каждый ресурс.

## Configured, pinned, observed

| Состояние | Что подтверждает | Что не подтверждает |
| --- | --- | --- |
| configured / requested | Model/effort извлечены из agent asset в team service | Фактически использованные модель, effort или расход |
| pinned | Версия/hash и content ресурсов включены в зафиксированный run context | Исполнение или результат |
| observed | Отдельное записанное наблюдение с указанным coverage/source | Полную историю host или неподтверждённые метрики |

В исходнике pins `requestedModel`/`requestedEffort` могут быть заданы, а `observedModel`/`observedEffort` равны null. Отчёт team analytics указывает partial coverage и отсутствие host token/cost telemetry. Не превращайте unknown в ноль.

## Граница инструкций и данных

[m1-recipe.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/m1-recipe.mts) для отдельного coordinator пути цитирует сохранённый task context и user request как untrusted JSON, ограничивает сохранённый context 64 KiB и применяет переданную redaction. Это локальный source contract, не гарантия полного предотвращения prompt injection. [persisted.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/redaction/persisted.mts) и [privacy guidance](../../product-agent-os/privacy-supply-chain-retention.md) задают границы хранения; секреты не включаются в примеры. См. [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts) и [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/sessions-team.test.mts); runtime/providers здесь не запускались.

## FUNC-G05 — текущие контракты

F16 возвращает paos_profile_evidence_v1: configured описывает текущую model/effort/version/hash, pinned — immutable requested model/effort/version/hash каждого сохранённого run, observed=null с причиной selected_route_has_no_loaded_profile_attestation. loadedVersion остаётся null, даже после claim/report, импорта или обновления managed asset. PAOS pins не являются host attestation; обновление текущего профиля не переписывает старые pins. Публичный run DTO содержит только allowlist metadata, без content/lease/input. Поддерживаемый OpenAI App Server имеет отдельные thread/turn/skills API; текущий выбранный App-agent bridge не подключает эти history/attestation APIs. Приватные host JSONL/credential stores не читаются. [Официальный App Server](https://learn.chatgpt.com/docs/app-server).
