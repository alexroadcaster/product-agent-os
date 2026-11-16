# Справочник endpoints

Source status: repository_source / current_source_contract_review; 15.11.2026.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

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


## FUNC-G03: текущий локальный контракт

Дополнение от 15.11.2026 описывает текущие `http/application.mts`, `project-files/service.mts`, `project-scans/service.mts` и `runtime/task-file-preflight.mts`; pinned DG03-ссылки ниже сохраняют историческую версию.

| Метод и путь `/api/v1` | Вход | Результат и граница |
| --- | --- | --- |
| `GET /projects/{id}/files` | `path`, `cursor?`, `limit?`, `filter?`, `query?` | Ленивая страница одной директории; `filter=all/control_plane`, поиск в текущей директории, default100/max200; coverage/reasons и access metadata |
| `GET /projects/{id}/files/read` | `path`, `revision?`, `line?` | `available/stale/forbidden/binary/too_large/unsupported/unavailable`; текст только для `available`, plain text с display redaction |
| `GET /projects/{id}/files/policy` | — | `version`, `policy`, `policyVersion` |
| `POST /projects/{id}/files/policy` | `policy`, `expectedVersion` | Profile-owned CAS; include/exclude/respectGitignore не отменяют hard deny |
| `GET /projects/{id}/scans` | — | Сохранённые latest/lastSuccessful и stage outcomes |
| `POST /projects/{id}/scans` | `requestId?`, `revision?` | 202; bounded background scan, request replay/coalescing и scope fences |
| `POST /projects/{id}/scans/{scanId}/cancel` | пустой JSON object | Отмена принадлежащего проекту scan |
| `POST /projects/{id}/scans/{scanId}/retry` | пустой JSON object | 202; новая попытка через idempotent retry key |
| `GET /projects/{id}/analysis` | — | Сохранённый core analysis с проверкой текущих source/adapter revisions; explicit unavailable/stale |
| `POST /projects/{id}/runtime/file-preflight` | `taskId`, обязательный integer `expectedRevision` | Metadata-only `allowed`, limits/counts/items/reasons, digest/taskRevision и source pins; без content/diff |
| `GET /projects/{id}/freshness` | — | Дешёвый profile stamp без обхода filesystem |

`POST /projects` сначала сохраняет регистрацию. `scan:true` запрашивает фоновый scan; ответ может содержать `scan` либо `scanError`, регистрация при ошибке scan сохраняется. Повтор `requestId` требует того же registration payload. `GET task-manager` возвращает entities и freshness из одного SQLite read transaction.

Registry владеет root и policy; browser не передаёт произвольный root. `fileRevision` — metadata/policy pin, `hash` и reference `revisionKind=sha256` — raw-byte content pin. Их нельзя подменять друг другом. Freshness `policyVersion` — integer CAS version, source `policyVersion` — строковая identity. Preflight читает сохранённую task scope, отвергает stale task revision; optional execution client guard `{digest,taskRevision}` не даёт разрешения на выполнение. Gateway проверяет preflight при admission и повторно проверяет доступ при capture перед native command; approvals и broker restrictions сохраняются.

Текущие bounded integration receipts основного агента: F29 API 6/6, file-preflight API 1/1, gateway policy 28/28, F18 5/5. Это переданное локальное evidence; новый browser/native final и human acceptance здесь не заявлены. Следующий артефакт — результат конкретного API/scan с provenance, затем соответствующая проверка пользователя.

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

## FUNC-G04 / F09 — bounded history и artifact summaries

Session catalog выбирает только sessions и связанные task/run attribution в SQLite. Transcript фильтрует `kind`, `parent_id`, hidden/analysis/reasoning до materialization; search сохраняет Unicode case folding. Worker замораживает membership и значения в connection-private SQLite TEMP tables: правка, вставка, удаление или archive после первой страницы не меняют последующие страницы. `journalOrder` сохраняет исходный insertion ordinal. В JavaScript переводится только текущая страница, где действует прежний redaction mapper; source bodies всей истории не передаются в LocalStore caller.

Cursor действует до 15 минут и может быть вытеснен LRU при storage pressure. Scope включает project/root identity, authority epoch, inventory policy и query/filters; несовпадение, expiry, eviction и restart дают `CURSOR_STALE`. `limit` — 1–100; byte cap может уменьшить страницу до числа меньше `limit`, после чего `nextCursor` продолжает без пропусков. Response budget — 1 MiB с резервом metadata. Один oversized item даёт `HISTORY_ITEM_TOO_LARGE`; snapshot больше 200 000 rows или payload budget — `HISTORY_SNAPSHOT_BUSY`. Перед freeze выполняется SQL size preflight, eviction — до insert, rollback сохраняет прежние cursors. Payload aggregate ограничен 230 MiB, оставляя резерв для indexes/page metadata; `temp.max_page_count` также ограничивает основной TEMP database file 256 MiB. Это не лимит RSS или общего disk I/O: transient SQLite sort/journal overhead учитывается отдельно. Persistent schema/migration не меняются.

Artifact catalog получает `substr(body,1,280)` и выбранные kinds из SQL, сохраняя frozen summaries/cursors и root/policy checks. Для длинного persisted body reason `persisted_body_preview_only_search` означает поиск только по title/preview; отсутствие совпадения в остальной части body не считается проверенным. Projection выше 6 MiB даёт partial reason `artifact_projection_byte_limit`; существующие catalog snapshot budgets остаются активны. Raw persisted document read проверяет SQL byte lengths до загрузки: body до 512 KiB, metadata до 256 KiB, иначе `DOCUMENT_TOO_LARGE`. Workspace document read сохраняет существующие checked-source guards.

Текущие synthetic regression checks: `node --test tests/web/snapshot-history-scale.test.mts` — 9/9: 100 000 messages около 100 MiB, 1000 documents по 107 315 bytes, page-only mapper, immutable edit/archive values, LRU/expiry/scope drift, rollback, byte caps, Unicode и oversized-read rejection. Existing session/source-policy/code-index integration проверялась отдельно; native-junction skips остаются gaps. Эти проверки не заменяют F20 after/final p95/soak или human acceptance. Node `DatabaseSync.function` сверена через Context7 `/nodejs/node/v26.0.0` с [официальной документацией](https://github.com/nodejs/node/blob/v26.0.0/doc/api/sqlite.md); установленная версия — Node v26.5.0.

## FUNC-G04 — карта кода, схема и static queries

GET graph принимает mode=all|dependencies|symbols, direction=both|incoming|outgoing и nodeId/pathTo для bounded static path (до8 hops/1000 visited nodes). Поиск/filters/cursor привязаны к revision и cache generation; restart/eviction требует rebuild. Это imports/lexical occurrences, не runtime call graph.

GET /projects/:id/database возвращает только registration/status/candidates; POST database/source выбирает relativePath+expectedFileRevision+expectedVersion либо clear. Он не открывает SQLite. POST database/scan запускает F27 inventory+schema; отмена/повтор используют обычные scans/:scanId/cancel|retry, повтор сохраняет selected stages. GET database/schema выдаёт bounded page, escaped Mermaid и diagramEntities из того же snapshot; GET database/changes сравнивает два совместимых metadata snapshots. Current/stale/incompatible и отсутствие baseline различаются. Source admission не разрешает generic Files DB read. Windows native read lease и offline SQLite — текущий adapter scope; PostgreSQL/credentials/rows/project SQL не поддержаны.

GET /projects/:id/code-database и GET code-database/links выдают status и static source evidence; POST code-database/scan запускает inventory+code_database. Links требуют оба codeRevision/schemaRevision, поддерживают table/path/operation/confidence/limit/cursor и ограничены32KiB. Confirmed требует source binding; inferred/unresolved не становятся runtime facts. SQL values/rows не возвращаются.

POST /agent/v1/project-query — private App-agent action с channel capability и worker lease, runId, kind=status|links и теми же query fields. Project берётся из claimed run; projectId из payload запрещён. Lease/run/scope проверяются до и после async read; ответ≤32KiB. Browser cookie не даёт эту capability. Claimed job объявляет наличие query port; старый model/provider route не включается. Проверка использует synthetic worker без вызова модели.
