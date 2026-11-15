# Справочник endpoints

Source status: repository_source / static_contract_inventory; 15.11.2026.

Владелец: maintainers local-service/API; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении handler, client, delegate service или тестов. [Backend](../backend/index.md); [доступ и ошибки](errors.md); [события](events.md).

Каждый browser-маршрут `/api/v1` ниже требует loopback session и проверки same-origin; для методов кроме GET/HEAD дополнительно требуются `Origin` и `x-paos-csrf`. Исключения `/health`, `/launch`, bootstrap и `/agent/v1` перечислены отдельно. Прочерк означает отсутствие application body/query, а не отсутствие HTTP headers. Для JSON-запросов необходим `application/json`; поля в таблице — уровень handler, детальные ограничения и возвращаемые типы принадлежат ссылкам на implementation/contracts ниже. Тип клиента `Record<string, unknown>` не является полной опубликованной схемой. По умолчанию успешный JSON возвращает 200; binary download и HTML bootstrap — исключения. Сопоставление ошибок — в [errors](errors.md).

К каждому маршруту применяются только указанные ограничения pagination, revision и idempotency; если они не указаны, HTTP handler не вводит их сам. Domain services могут требовать дополнительные revision/cursor/idempotency: их исходные контракты ниже авторитетны; неизвестное обязательное поле нельзя считать необязательным. Даже корректный mutation может получить `MIGRATION_BUSY`. Таблица описывает исходники, не новый live-прогон.

| Метод и путь | Запрос / query | Ответ | Побочный эффект / fence |
| --- | --- | --- | --- |
| `GET /health` | — | instanceId, build, alive, sourceReaderReady, runtimeCapable, browserLaunchVersion | только health |
| `GET /launch` | прямая навигация Fetch Metadata | HTML bootstrap or 303 | HTML bootstrap или 303 |
| `POST /bootstrap/launch` | JSON proof и launch cookie | csrfToken, instanceId, actorId + session cookie | одноразовый proof потребляется |
| `POST /bootstrap/exchange; POST /api/v1/bootstrap/exchange` | JSON code | csrfToken, instanceId, actorId + session cookie | pairing code потребляется |
| `POST /agent/v1/{attach,heartbeat,claim,report,command,operation,progress,reconcile,task-create}` | JSON capability; Bearer token | action result or agent error | закрытый канал, browser cookie не даёт доступ |
| `GET /api/v1/session` | — | actorId, csrfToken, instanceId | principal сессии |
| `POST /api/v1/quit` | — | 202 status=quit_requested | запрашивает остановку owner |
| `POST /api/v1/logout` | — | revoked | отзывает сессии и launch proof |
| `GET /api/v1/preferences` | — | locale, theme | чтение настроек профиля |
| `PUT /api/v1/preferences` | locale, theme | saved preferences | запись настроек |
| `POST /api/v1/desktop/project-folder` | requestId, необязательный initialDirectory | cancelled or workspaceRoot | native picker; повтор requestId требует идентичный payload |
| `POST /api/v1/connection/app-handoff` | requestId | opened, requiresSend, verified, state | открывает draft; не отправляет; повтор requestId требует идентичный payload |
| `GET /api/v1/connection` | — | connection state | чтение статуса |
| `POST /api/v1/connection` | route?, connectionId, apiKey?, remember? | connection state | подключает выбранный route; credentials чувствительны |
| `DELETE /api/v1/connection` | — | connection state | отключает |
| `GET /api/v1/runtime/state` | projectId?, sessionId? | runtime snapshot, pending approvals | может синхронизировать наблюдаемые решения |
| `POST /api/v1/runtime/{bindings,send,interrupt,approve,reconcile}` | JSON выбранного действия | runtime/decision result | dispatch / interrupt / approval; нет implicit fallback |
| `GET /api/v1/projects` | — | items of id, name, keyPrefix, authorityMode, authorityEpoch, streamGeneration | список зарегистрированных проектов |
| `POST /api/v1/projects` | name, workspaceRoot, keyPrefix?, legacySource?, requestId?, scan? | 201 id/name/keyPrefix/authorityMode/authorityEpoch, optional scan | регистрация; scan может быть partial; requestId необязателен |
| `GET /api/v1/projects/{projectId}` | projectId | id/name/keyPrefix/authorityMode/authorityEpoch/streamGeneration | чтение проекта |
| `GET /api/v1/projects/{projectId}/sources` | projectId | bounded source coverage | ограниченный список источников |
| `GET /api/v1/projects/{projectId}/sources/{name}` | name | relativePath/content/sha256/coverage/redacted | ограниченное чтение источника, не всего дерева |
| `GET /api/v1/projects/{projectId}/catalogs` | projectId | agents, skills, graph, coverage | ограниченный read-only каталог |
| `GET /api/v1/projects/{projectId}/entities` | kind?, parentId?, limit?, offset?, order? | items, hasMore | limit 1–100, default50; приватные kinds исключены |
| `GET /api/v1/projects/{projectId}/entities/{id}` | ID сущности | stored entity | settings/run/approval запрещены |
| `POST /api/v1/projects/{projectId}/commands` | idempotencyKey, expectedAuthorityEpoch, changes[] | write result | проверка revision/authority; запись |
| `POST /api/v1/projects/{projectId}/tasks/{taskId}/check` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, outcome, note? | check receipt | записывает ручной check |
| `POST /api/v1/projects/{projectId}/tasks/{taskId}/accept` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, checkId, accepted, note? | acceptance result | приёмка отдельно от check |
| `GET /api/v1/projects/{projectId}/search` | q, offset? | items, coverage, generation, hasMore | FTS; limit50, приватные kinds исключены |
| `POST /api/v1/projects/{projectId}/search/rebuild` | JSON-объект | status, coverage | перестраивает индекс; возможна отмена |
| `GET /api/v1/projects/{projectId}/{events,history}` | cursor? | items, generation, nextCursor | подписанный cursor; replay и неизменяемый audit различаются |
| `POST /api/v1/projects/{projectId}/imports/preview` | sources[] либо sourceName + content; sourceRelativePath? | stageId, parserVersion, sourceDigest, proposal, sources, items, blocked | записывает staging document; не чистое чтение |
| `GET /api/v1/projects/{projectId}/imports/source-status` | — | authorityMode, items | чтение статуса источников |
| `POST /api/v1/projects/{projectId}/imports/commit` | stageId, sourceDigest, expectedAuthorityEpoch, idempotencyKey, currentSource? | receipt, sourceDigest, backupId, mappingCount | cutover с проверкой authority |
| `GET /api/v1/projects/{projectId}/imports/export` | — | reverse-transfer document | чтение reverse transfer |
| `POST /api/v1/projects/{projectId}/{backups,task-manager/export}` | — | format, scope, restoreEndpoint, backupId, manifest, rotationCandidateIds, retention | создаёт backup всего local profile |
| `POST /api/v1/projects/{projectId}/backups/rotation` | candidateIds[] | rotatedBackupIds, retention | удаляет выбранные управляемые backups |
| `POST /api/v1/projects/{projectId}/{restores,task-manager/import-backup}` | backupId | restoreId, requiresRestart, activeProfileChanged=false | staged restore; активный профиль не меняется |
| `GET /api/v1/projects/{projectId}/decisions` | kind?, state?, sessionId?, offset?, limit? | DecisionsPage | синхронизирует наблюдаемые решения |
| `POST /api/v1/projects/{projectId}/decisions` | параметры decision | DecisionView | создаёт решение; migration freeze |
| `GET /api/v1/projects/{projectId}/decisions/{id}` | ID решения | DecisionView | чтение |
| `POST /api/v1/projects/{projectId}/decisions/{id}/respond` | параметры ответа | DecisionResponse | ответ; migration freeze |
| `GET /api/v1/projects/{projectId}/graph/status` | — | GraphStatus | статус индекса |
| `POST /api/v1/projects/{projectId}/graph/rebuild` | JSON-объект | GraphStatus | перестраивает локальный индекс |
| `GET /api/v1/projects/{projectId}/graph` | revision, query?, depth?, nodeId?, edgeTypes?, limit?, cursor? | GraphPage | ограниченный граф и partial coverage |
| `GET /api/v1/projects/{projectId}/graph/source` | revision, fileId, start?, end? | GraphSourceExcerpt | ограниченный фрагмент исходника |
| `GET /api/v1/projects/{projectId}/graph/nodes/{id}` | revision | GraphNodeDetail | узел заданной revision |
| `GET /api/v1/projects/{projectId}/graph/nodes/{id}/impact` | revision/query по code-index service | GraphImpact | ограниченный impact |
| `GET /api/v1/projects/{projectId}/scheduler` | — | QueueSnapshot | чтение scheduler |
| `POST /api/v1/projects/{projectId}/scheduler/{preview,enqueue,pause,resume,reorder,cancel,pause-entry,resume-entry}` | JSON выбранного scheduler-действия | QueuePreview or entryId?/revision | preview или изменение очереди; migration freeze |
| `GET /api/v1/projects/{projectId}/execution-recipes` | — | items: RecipeExecutionView[] | список выполнений |
| `POST /api/v1/projects/{projectId}/execution-recipes/{preview,start}` | параметры recipe | RecipePreview or RecipeExecutionView / manual target | preview/start; migration freeze |
| `GET /api/v1/projects/{projectId}/execution-recipes/{id}` | ID исполнения | RecipeExecutionView | чтение исполнения |
| `POST /api/v1/projects/{projectId}/execution-recipes/{id}/{pause,resume,cancel,reconcile}` | JSON команды | RecipeExecutionView | переход исполнения; migration freeze |
| `GET /api/v1/projects/{projectId}/autonomy` | — | AutonomySnapshot | чтение policy |
| `POST /api/v1/projects/{projectId}/autonomy/preview` | policy, expectedRevision | AutonomyPreview | валидация preview |
| `POST /api/v1/projects/{projectId}/autonomy/{save,resume,pause}` | параметры policy/command | AutonomySnapshot; pause may include interrupts | сохранение или переход; migration freeze |
| `GET /api/v1/projects/{projectId}/task-manager` | — | ManagerSnapshot | чтение проекции задач |
| `POST /api/v1/projects/{projectId}/task-manager/commands` | action, idempotencyKey, expectedAuthorityEpoch, поля действия / expectedRevision | result; may include pendingStop | запись tasks/links/workflows; freeze и revision |
| `POST /api/v1/projects/{projectId}/task-manager/links/{id}/stop` | JSON-объект | pending stop status | запрос остановки runtime |
| `POST /api/v1/projects/{projectId}/task-manager/reference` | taskId, relativePath, revision? | availability, relativePath, revision?, expectedRevision?, reason?, content?, redacted? | ограниченная ссылка на источник |
| `POST /api/v1/projects/{projectId}/tasks/{taskId}/attachments` | filename, mediaType, base64, expectedRevision, expectedAuthorityEpoch, idempotencyKey | upload result | запись управляемого blob |
| `GET /api/v1/projects/{projectId}/tasks/{taskId}/attachments/{id}` | taskId, attachmentId | binary download | чтение вложения |
| `GET /api/v1/projects/{projectId}/team/runs/{id}` | ID run | id, sessionId, taskId, status, mode, route, timestamps, assetPins, workflow, coverage, source | redacted persisted run |
| `GET /api/v1/projects/{projectId}/team/catalog` | — | TeamCatalog | чтение team assets |
| `POST /api/v1/projects/{projectId}/team/generation` | параметры генерации | generation result | начало генерации зависит от runtime |
| `GET /api/v1/projects/{projectId}/team/generation/{id}` | ID генерации | generation result | чтение генерации |
| `GET /api/v1/projects/{projectId}/team/skills/discovery` | q? | discovery result | чтение каталога skills |
| `POST /api/v1/projects/{projectId}/team/skills/source-preview` | sourceRootId, relativePath | source preview | ограниченное чтение |
| `POST /api/v1/projects/{projectId}/team/skills/generation` | параметры генерации | generation result | начало генерации skill |
| `GET /api/v1/projects/{projectId}/team/skills/generation/{id}` | ID генерации | generation result | чтение |
| `POST /api/v1/projects/{projectId}/team/skills/generation/{id}/apply` | параметры proposal | apply result | запись; migration freeze |
| `POST /api/v1/projects/{projectId}/team/proposals/preview` | JSON proposal | AssetPreview | предпросмотр |
| `POST /api/v1/projects/{projectId}/team/proposals/apply` | JSON proposal, idempotencyKey по contract | assetId, version | применение; migration freeze |
| `GET /api/v1/projects/{projectId}/team/metrics` | from, to | metrics result | чтение |
| `POST /api/v1/projects/{projectId}/team/assets/{id}/copy-preview` | JSON-объект | copy preview | предпросмотр |
| `GET /api/v1/projects/{projectId}/team/assets/{id}` | ID asset | AssetProfile | чтение |
| `GET /api/v1/projects/{projectId}/team/assets/{id}/history` | ID asset | assetId, versions | чтение истории |
| `GET /api/v1/projects/{projectId}/team/assets/{id}/export` | ID asset | export object | чтение экспорта |
| `GET /api/v1/projects/{projectId}/team/assets/{id}/resources/{path}` | version? | binary download | чтение ресурса |
| `GET /api/v1/projects/{projectId}/sessions/catalog` | q?, archived?, status?, taskId?, agentId?, source?, limit?, cursor?, anchor? | catalog result | чтение |
| `GET /api/v1/projects/{projectId}/sessions/search` | q, limit?, cursor?, anchor? | search result | чтение |
| `GET /api/v1/projects/{projectId}/sessions/{id}/transcript` | limit?, cursor?, anchor? | transcript result | чтение сессии |
| `GET /api/v1/projects/{projectId}/artifacts` | q?, kind?, taskId?, limit?, cursor? | ArtifactPage | ограниченный snapshot |
| `GET /api/v1/projects/{projectId}/artifacts/{id}` | version? | ArtifactDocument | чтение документа |
| `POST /api/v1/projects/{projectId}/artifacts/proposals/preview` | параметры proposal | preview result | предпросмотр |
| `POST /api/v1/projects/{projectId}/artifacts/proposals` | параметры proposal | proposal result | сохранение proposal; migration freeze |


## Поля и ограничения отдельных действий

Ниже минимальные поля и формы результатов для App-agent route и перечисленных service implementations. API BYOK имеет отдельный [live gateway](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/live-gateway.mts); нельзя предполагать, что его input и доступные действия идентичны. Знак вопроса обозначает условно необязательные значения. Private agent channel использует общие workerId/generation/leaseToken кроме attach; это не browser API.

| Действие | Обязательный / условный input | Результат / fence | Source |
| --- | --- | --- | --- |
| `runtime/bindings` | projectId, sessionId, mode (discussion/planning/execution) | bindingId, projectId, sessionId, mode, route | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L256-L282) |
| `runtime/send` | projectId, sessionId, bindingId, clientMessageId, input; taskId обязателен в execution; autonomy?, taskCreationApproved?; approval только в execution без autonomy; handler подставляет actorId как taskCreationInitiator и отклоняет поле от клиента | public job {id,bindingId,projectId,sessionId,state,mode,route}; same messageId/digest replay | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L283-L325) |
| `runtime/interrupt` | projectId, sessionId, bindingId, runId | public job; queued → interrupted, running → cancel_requested | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L340-L344) |
| `runtime/approve` | projectId, sessionId, bindingId, runId, generation, requestId, decision=accept/decline/cancel | operation view; scoped approval decision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L326-L339) |
| `runtime/reconcile` | projectId, sessionId, bindingId; optional runId/resolution=cancel_undispatched | public job or null; only undispatched cancellation | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L345-L354) |
| `agent/attach` | hostIdentity=codex_app, workerId, generation | workerId, generation, leaseToken, expiresAt | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L357-L362) |
| `agent/heartbeat` | workerId, generation, leaseToken | expiresAt, job, jobs | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L363-L364) |
| `agent/claim` | workerId, generation, leaseToken, runId? | job or null; claim transitions queued → running | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L365-L374) |
| `agent/report` | workerId, generation, leaseToken, runId, seq, idempotencyKey, status; text required if completed | runId, seq, state, route; replay only for identical key/digest | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L413-L428) |
| `agent/command` | workerId, generation, leaseToken, runId, operationId, argv[], timeoutMs? | operation view awaiting approval; timeout 1–30000ms | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L399-L411) |
| `agent/operation` | workerId, generation, leaseToken, runId, operationId | operation view | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L375-L380) |
| `agent/progress` | workerId, generation, leaseToken, runId, seq, text, phase | runId, seq; monotonic sequence | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L396-L398) |
| `agent/reconcile` | workerId, generation, leaseToken, runId | last report receipt or public job | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L375-L379) |
| `agent/task-create` | workerId, generation, leaseToken, runId, operationId, title, summary, acceptanceCriteria[] | taskId, runId, sessionId; owner-opted-in execution only | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts#L382-L395) |
| `scheduler/preview` | taskId, transitionId, mode=recipe, sessionId, roleBindings, expectedTaskRevision, reason | QueuePreview including previewDigest and queueRevision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L46-L47) |
| `scheduler/enqueue` | preview input + previewDigest, expectedRevision, expectedAuthorityEpoch, idempotencyKey | entryId, revision; receipt binds action+payload | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L67-L73) |
| `scheduler/pause, resume` | expectedRevision, expectedAuthorityEpoch, idempotencyKey | revision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L74-L75) |
| `scheduler/reorder` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, order[] | revision; order must be complete permutation | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L74-L76) |
| `scheduler/cancel, pause-entry, resume-entry` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, entryId | revision; entry state constraints | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts#L74-L80) |
| `execution-recipes/preview` | taskId, transitionId, mode, expectedTaskRevision, reason; sessionId and roleBindings for recipe mode | RecipePreview and previewDigest | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts#L33-L52) |
| `execution-recipes/start` | preview input + previewDigest, expectedAuthorityEpoch, idempotencyKey | RecipeExecutionView or manual result | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts#L143-L149) |
| `execution-recipes/{id}/pause,resume,cancel,reconcile` | expectedRevision, expectedAuthorityEpoch, idempotencyKey; reason? | RecipeExecutionView; action-specific recovery checks | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts#L151-L180) |
| `autonomy/preview` | policy, expectedRevision | AutonomyPreview incl previewDigest | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts) |
| `autonomy/save` | policy, previewDigest, expectedRevision, expectedAuthorityEpoch, idempotencyKey | AutonomySnapshot | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts#L42-L52) |
| `autonomy/pause, resume` | expectedRevision, expectedAuthorityEpoch, idempotencyKey | AutonomySnapshot; pause may include interrupts | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts#L42-L61) |
| `decisions POST` | kind=clarification/product, title, body, expiresInSeconds, expectedAuthorityEpoch, idempotencyKey; taskId?, sessionId?, proposedDiff?, evidenceIds? | DecisionView; 60–604800s expiry | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/decisions/service.mts#L112-L116) |
| `decisions/{id}/respond` | expectedRevision, expectedAuthorityEpoch, idempotencyKey, response; answer?, reason? | DecisionResponse; review/authority checks | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/decisions/service.mts#L79-L109) |


### Team и artifact proposals

| Action | Input | Result / fence | Source |
| --- | --- | --- | --- |
| `team/proposals/preview` | proposal, expectedRevision; proposal.kind/action/name/description/content/reason/dependencies; assetId for non-create | AssetPreview {proposal,baseRevision,diff,dependencyImpact,warnings,previewDigest} | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/contract.mts#L8-L43) |
| `team/proposals/apply` | proposal, expectedRevision, epoch, idempotencyKey, previewDigest | assetId, version; verifies exact preview and transaction fences | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/service.mts#L28-L37) |
| `team/generation` | description, sessionId, bindingId; targetAssetId?, idempotencyKey? | id, sessionId, runId, purpose, state | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/generation.mts#L5-L11) |
| `team/skills/generation` | mode=requirements/description, sessionId, bindingId, description?; requirements mode requires expectedRevision, startLine?, endLine? | id, runId, sessionId, state, generationKey, requirements, applyKey | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/skill-generation.mts#L21-L33) |
| `team/skills/generation/{id}/apply` | proposal, previewDigest, epoch; expectedRevision=0 and applyKey assigned by service | assetId, version; validates proposal/requirement revision | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/skill-generation.mts#L68-L75) |
| `artifacts/proposals/preview` | documentId, sourceVersion, body | documentId, sourceVersion, before, after, previewDigest, applied=false, policy=staged_only | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/artifacts/service.mts#L57) |
| `artifacts/proposals` | documentId, sourceVersion, body, previewDigest, epoch, idempotencyKey | id, staged=true, replayed; staged only, no target apply | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/artifacts/service.mts#L59) |

## Подробные service contracts и тесты

Ссылки содержат актуальную валидацию inputs, кратко перечисленных выше; генератор OpenAPI пока не выбран. Никакие скрипты репозитория или target project для инвентаря не запускаются.

| Область | Реализация | Контракт / тесты |
| --- | --- | --- |
| HTTP / auth | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) |
| UI client | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/api/client.ts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts) |
| Task manager | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/task-manager/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/issues/manager.ts) |
| Runtime / channel | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-channel.mts) |
| Graph | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/code-index/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/graph/code-graph.ts) |
| Decisions | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/decisions/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/decisions/decision.ts) |
| Scheduler | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/scheduler/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/scheduler/queue.ts) |
| Recipes | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/execution-recipes/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/execution-recipes/recipe.ts) |
| Autonomy | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/autonomy-policy/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/autonomy/policy.ts) |
| Team / assets | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/team/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/team/assets.ts) |
| Sessions | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/sessions/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/sessions/history.ts) |
| Artifacts | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/artifacts/service.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/artifacts/catalog.ts) |
| Storage / import | [source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) | [contract / tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/import-export/migration.mts) |

Graph query требует существующую совпадающую `revision`; pagination cursor привязан к revision и фильтрам. Для `graph/source` также необходим `fileId`, необязательны ограниченные `start`/`end` и свежий индекс. Decisions использует `offset`/`limit` (default 50, 1–100), а не graph cursor. Session history использует cursor фиксированного snapshot на 15 минут с `limit` 1–100; artifact snapshots тоже имеют scope cursor. См. [события](events.md).

`scan=true` при добавлении проекта выполняет текущую ограниченную проверку источников и перестроение графа, сообщая partial failures после зафиксированной регистрации. Это не полный файловый браузер или запланированное управляемое фоновое сканирование F26–F29. PoC и endpoints target DB/schema/code-table F30–F34 не реализованы этим API. Владелец будущих возможностей — [функциональный backlog](../planning/functional-remediation-2026-11-15.md).

Ограничения: изучены исходники и указанные тесты; provider, реальный профиль/БД, сетевой сервер и runtime приложения не запускались. [Registry](../sources/registry.md); [план Web](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md).
