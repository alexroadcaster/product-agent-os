import { createHmac, randomUUID, timingSafeEqual } from 'node:crypto';
import { lstat, mkdir, readFile, realpath } from 'node:fs/promises';
import { basename, join, relative, resolve } from 'node:path';
import { restoreLocalBackup, pruneManagedBackups, type LocalStore } from '../storage/local-store.mts';
import type { EntityInput, EntityKind, StoreWrite } from '../../../../packages/contracts/storage/local-store.ts';
import { bindProject, inspectProjectSources, readProjectSource } from '../adapters/project-sources.ts';
import { createSessionGate } from './session-gate.mts';
import { applyUserCommand, recordManualCheck, acceptTask } from '../tasks/user-commands.mts';
import { taskManagerSnapshot, taskManagerCommand, uploadTaskAttachment, downloadTaskAttachment, resolveTaskReference, requestPendingLinkStop } from '../task-manager/service.mts';
import { previewTaskImport, type ImportSourceInput } from '../import-export/preview.mts';
import { createMigrationManager, type WriterInventory } from '../import-export/migration.mts';
import { scanReadOnlyCatalogs } from './catalogs.mts';
import {createSessionHistory} from '../sessions/service.mts';
import {createTeamService} from '../team/service.mts';
import type {AssetRoot} from '../team/sources.mts';
import {startTeamGeneration,teamGenerationResult} from '../team/generation.mts';
import { loadUiPreferences, saveUiPreferences } from '../../../web/src/design/preferences.ts';

export type ApplicationOptions = {
  store: LocalStore; origin: string; instanceId: string; profileDirectory: string; staticDirectory?: string;
  writerInventory?: (projectId: string) => Promise<WriterInventory>;
  runtimeCapable?: () => boolean;
  onQuit?: () => void;
  connection?: { status(): unknown; connect(input: unknown): Promise<unknown>; disconnect(): Promise<unknown> };
  runtime?: { snapshot(input: Record<string, unknown>): Promise<unknown>; dispatch(action: string, input: Record<string, unknown>): Promise<unknown> };
  /** Separate profile capability, never a browser cookie or a provider credential. */
  agentChannel?: {handle(request: Request): Promise<Response>};
  assetRoots?:AssetRoot[];
};

function fail(code: string): never { throw Object.assign(new Error(code), { code }); }
function record(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) fail('INVALID_REQUEST');
  return value as Record<string, unknown>;
}
function string(value: unknown): string { if (typeof value !== 'string' || !value.trim()) fail('INVALID_REQUEST'); return value; }
function integer(value: unknown): number { if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < 0) fail('INVALID_REQUEST'); return value; }
const kinds: EntityKind[] = ['task', 'session', 'message', 'draft', 'comment', 'settings', 'document', 'run', 'approval', 'evidence'];
const headers = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' };
const json = (value: unknown, status = 200) => new Response(JSON.stringify(value), { status, headers });

async function body(request: Request, limit = 1024 * 1024) {
  if (request.headers.get('content-type')?.split(';')[0].trim() !== 'application/json') fail('JSON_REQUIRED');
  const reader = request.body?.getReader();
  const chunks: Uint8Array[] = [];
  let bytes = 0;
  if (reader) {
    try {
      while (true) {
        const next = await reader.read();
        if (next.done) break;
        bytes += next.value.byteLength;
        if (bytes > limit) { await reader.cancel(); fail('REQUEST_TOO_LARGE'); }
        chunks.push(next.value);
      }
    } finally { reader.releaseLock(); }
  }
  try { return record(JSON.parse(Buffer.concat(chunks).toString('utf8'))); } catch { fail('INVALID_REQUEST'); }
}

/** Direct Request/Response entry point. Tests exercise the real service without opening a socket. */
export async function createLocalApplication(options: ApplicationOptions) {
  const { store, origin, instanceId, profileDirectory } = options;
  const sessionHistory=createSessionHistory(store);
  const team=createTeamService(store,options.assetRoots);
  const gate = createSessionGate({ origin, instanceId });
  const migration = createMigrationManager({ store, profileDirectory,
    inventory: options.writerInventory ?? (async () => ({ complete: false, entries: [] })) });
  const cursorSecret = randomUUID();
  const profileProject = '_paos_profile';
  await store.registerProject({ id: profileProject, keyPrefix: 'PREF', canonicalRoot: resolve(profileDirectory),
    rootIdentity: `profile:${resolve(profileDirectory)}`, authorityMode: 'sql', displayName: 'Preferences' });
  const preferencesStore = {
    read: async () => (await store.get(profileProject, 'ui-preferences'))?.data,
    write: async (preferences: unknown) => {
      const existing = await store.get(profileProject, 'ui-preferences');
      const project = await store.project(profileProject);
      await store.write({ projectId: profileProject, actorId: 'local-user', idempotencyKey: randomUUID(),
        expectedAuthorityEpoch: project!.authorityEpoch, changes: [{ expectedRevision: existing?.revision ?? 0,
          entity: { id: 'ui-preferences', kind: 'settings', data: record(preferences) } }] });
    },
  };

  async function metadata(projectId: string) {
    if (projectId === profileProject) fail('PROJECT_NOT_FOUND');
    const project = await store.project(projectId);
    if (!project) fail('PROJECT_NOT_FOUND');
    return project;
  }

  function encodeCursor(projectId: string, generation: string, seq: number) {
    const payload = Buffer.from(JSON.stringify({ projectId, generation, seq })).toString('base64url');
    return `${payload}.${createHmac('sha256', cursorSecret).update(payload).digest('base64url')}`;
  }

  function decodeCursor(token: string, projectId: string) {
    const [payload, signature, extra] = token.split('.');
    const expected = createHmac('sha256', cursorSecret).update(payload ?? '').digest('base64url');
    if (extra !== undefined || !signature || signature.length !== expected.length
      || !timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) fail('CURSOR_INVALID');
    const decoded = record(JSON.parse(Buffer.from(payload, 'base64url').toString('utf8')));
    if (decoded.projectId !== projectId) fail('CURSOR_INVALID');
    return { after: integer(decoded.seq), generation: string(decoded.generation) };
  }

  async function staticResponse(pathname: string) {
    if (!options.staticDirectory) return new Response('Web build unavailable', { status: 503 });
    const root = await realpath(options.staticDirectory);
    const candidate = resolve(root, pathname === '/' ? 'index.html' : `.${pathname}`);
    const within = relative(root, candidate);
    if (within.startsWith('..') || within.includes(':')) return new Response('Not found', { status: 404 });
    try {
      const final = await realpath(candidate);
      if (relative(root, final).startsWith('..') || !(await lstat(final)).isFile()) return new Response('Not found', { status: 404 });
      const type = final.endsWith('.js') ? 'text/javascript' : final.endsWith('.css') ? 'text/css'
        : final.endsWith('.html') ? 'text/html' : 'application/octet-stream';
      return new Response(await readFile(final), { headers: { 'content-type': `${type}; charset=utf-8`,
        'x-content-type-options': 'nosniff', 'cache-control': 'no-store',
        'content-security-policy': "default-src 'self'; script-src 'self'; connect-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'" } });
    } catch { return new Response('Not found', { status: 404 }); }
  }

  async function handleRequest(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      gate.validateOrigin(request, request.method !== 'GET' && request.method !== 'HEAD');
      if (url.pathname === '/health' && request.method === 'GET') return json({ instanceId, build: 'paos-m1-0.1.0',
        alive: true, sourceReaderReady: true, runtimeCapable: options.runtimeCapable?.() === true });
      if (['/bootstrap/exchange', '/api/v1/bootstrap/exchange'].includes(url.pathname) && request.method === 'POST') {
        const paired = gate.exchange(request, (await body(request)).code);
        return new Response(JSON.stringify({ csrfToken: paired.csrfToken, instanceId, actorId: 'local-user' }),
          { headers: { ...headers, 'set-cookie': paired.cookie } });
      }
      if (url.pathname.startsWith('/agent/')) {
        if (!options.agentChannel) fail('ROUTE_NOT_FOUND');
        return options.agentChannel.handle(request);
      }
      if (!url.pathname.startsWith('/api/')) {
        if (request.method !== 'GET') fail('ROUTE_NOT_FOUND');
        return staticResponse(decodeURIComponent(url.pathname));
      }
      const principal = gate.authorize(request);
      const path = url.pathname.replace(/^\/api\/v1/, '');
      if (path === '/session' && request.method === 'GET') return json(principal);
      if (path === '/quit' && request.method === 'POST') {
        if (!options.onQuit) fail('OWNER_UNAVAILABLE');
        options.onQuit();
        return json({ status: 'quit_requested' }, 202);
      }
      if (path === '/logout' && request.method === 'POST') { gate.revokeAll(); return json({ revoked: true }); }
      if (path === '/preferences') {
        if (request.method === 'GET') return json(await loadUiPreferences(preferencesStore));
        if (request.method === 'PUT') {
          const input = await body(request);
          return json(await saveUiPreferences(preferencesStore, { locale: input.locale, theme: input.theme }));
        }
      }
      if (path === '/connection') {
        if (request.method === 'GET') return json(options.connection?.status() ?? { verified: false, state: 'disconnected',
          reason: 'connection_unverified', payer: 'user_api_account' });
        if (request.method === 'POST') {
          if (!options.connection) fail('CONNECTION_UNAVAILABLE');
          return json(await options.connection.connect(await body(request)));
        }
        if (request.method === 'DELETE') return json(await options.connection?.disconnect() ?? { verified: false });
      }
      if (path === '/runtime/state' && request.method === 'GET') return json(await options.runtime?.snapshot(Object.fromEntries(url.searchParams))
        ?? { canSend: false, reason: 'connection_unverified', state: 'idle', pendingApprovals: [] });
      const runtimeAction = /^\/runtime\/(bindings|send|interrupt|approve|reconcile)$/.exec(path);
      if (runtimeAction && request.method === 'POST') {
        if (!options.runtime) fail('RUNTIME_UNAVAILABLE');
        return json(await options.runtime.dispatch(runtimeAction[1], await body(request)));
      }
      if (path === '/projects') {
        if (request.method === 'GET') {
          const projects = (await store.projects()).filter((project) => project.id !== profileProject);
          return json({ items: await Promise.all(projects.map(async (project) => ({ id: project.id, name: project.displayName,
            keyPrefix: project.keyPrefix, authorityMode: project.authorityMode, authorityEpoch: project.authorityEpoch,
            streamGeneration: (await store.events(project.id, { limit: 1 })).generation }))) });
        }
        if (request.method === 'POST') {
          const input = await body(request);
          const name = string(input.name);
          const binding = await bindProject(randomUUID(), string(input.workspaceRoot));
          const keyPrefix = typeof input.keyPrefix === 'string' ? input.keyPrefix : name.toUpperCase().replace(/[^A-Z]/g, '').slice(0, 4).padEnd(4, 'X');
          if (!/^[A-Z]{4}$/.test(keyPrefix)) fail('INVALID_PROJECT_KEY');
          const project = await store.registerProject({ id: binding.projectId, keyPrefix, displayName: name,
            canonicalRoot: binding.workspaceRoot, rootIdentity: binding.directoryIdentity,
            authorityMode: input.legacySource === true ? 'legacy_files' : 'sql' });
          return json({ id: project.id, name, keyPrefix, authorityMode: project.authorityMode, authorityEpoch: project.authorityEpoch }, 201);
        }
      }
      const route = /^\/projects\/([^/]+)(?:\/(.*))?$/.exec(path);
      if (!route) fail('ROUTE_NOT_FOUND');
      const projectId = decodeURIComponent(route[1]);
      const project = await metadata(projectId);
      const action = route[2] ?? '';
      if(action==='task-manager'&&request.method==='GET')return json(await taskManagerSnapshot(store,projectId));
      if(action==='task-manager/commands'&&request.method==='POST'){
        if(migration.frozen(projectId))fail('MIGRATION_BUSY');
        const input=await body(request,16*1024*1024),result=await taskManagerCommand(store,projectId,principal.actorId,input,{validateWorkflowReferences:definition=>team.validateWorkflowReferences(projectId,definition)});
        const linkId='linkId' in result&&typeof result.linkId==='string'?result.linkId:undefined;
        if(linkId&&(await taskManagerSnapshot(store,projectId)).links.some(link=>link.id===linkId&&link.state==='pending')){
          try{return json({...result,pendingStop:await requestPendingLinkStop(store,options.runtime,projectId,linkId)});}
          catch(error){return json({...result,pendingStop:{linkId,state:'pending',stopRequired:true,terminalReceipt:false,
            reason:typeof (error as any)?.code==='string'?(error as any).code:'RUNTIME_UNAVAILABLE'}});}
        }
        return json(result);
      }
      const pendingStop=/^task-manager\/links\/([^/]+)\/stop$/.exec(action);
      if(pendingStop&&request.method==='POST'){
        await body(request);
        return json(await requestPendingLinkStop(store,options.runtime,projectId,decodeURIComponent(pendingStop[1])));
      }
      if(action==='task-manager/reference'&&request.method==='POST')return json(await resolveTaskReference(store,projectId,await body(request)));
      const attachmentRoute=/^tasks\/([^/]+)\/attachments(?:\/([^/]+))?$/.exec(action);
      if(attachmentRoute){
        if(request.method==='POST'&&!attachmentRoute[2]){
          if(migration.frozen(projectId))fail('MIGRATION_BUSY');
          return json(await uploadTaskAttachment(store,projectId,decodeURIComponent(attachmentRoute[1]),principal.actorId,await body(request,70*1024*1024)));
        }
        if(request.method==='GET'&&attachmentRoute[2])return downloadTaskAttachment(store,projectId,decodeURIComponent(attachmentRoute[1]),decodeURIComponent(attachmentRoute[2]));
      }
      if (!action && request.method === 'GET') return json({ id: project.id, name: project.displayName, keyPrefix: project.keyPrefix,
        authorityMode: project.authorityMode, authorityEpoch: project.authorityEpoch, streamGeneration: (await store.events(projectId)).generation });
      if (action === 'sources' && request.method === 'GET') {
        const binding = await bindProject(projectId, project.canonicalRoot);
        if (binding.directoryIdentity !== project.rootIdentity) fail('PROJECT_ROOT_UNAVAILABLE');
        return json(await inspectProjectSources(binding, projectId));
      }
      if (action.startsWith('sources/') && request.method === 'GET') {
        const binding = await bindProject(projectId, project.canonicalRoot);
        if (binding.directoryIdentity !== project.rootIdentity) fail('PROJECT_ROOT_UNAVAILABLE');
        return json(await readProjectSource(binding, decodeURIComponent(action.slice(8))));
      }
      const runRoute=/^team\/runs\/([^/]+)$/.exec(action);
      if(runRoute&&request.method==='GET'){
        const row=await store.get(projectId,decodeURIComponent(runRoute[1])),run=(row?.data.appAgentRun??row?.data.runtimeRun) as any;
        if(!row||row.kind!=='run'||!run||run.projectId!==projectId)fail('TEAM_RUN_NOT_FOUND');
        // Deliberate allowlist: navigating a run never exposes its lease, input or full instructions.
        return json({id:row.id,sessionId:run.sessionId??null,taskId:run.taskContext?.taskId??run.taskId??null,status:run.state??row.status,mode:run.mode??null,route:run.route??(row.data.appAgentRun?'codex_app_agent':null),startedAt:run.observedStartedAt??run.startedAt??null,endedAt:run.endedAt??null,assetPins:(run.assetPins??[]).map((p:any)=>({assetId:p.assetId,kind:p.kind,version:p.version,hash:p.hash})),workflow:run.workflowSnapshot?{ref:run.workflowSnapshot.ref,definitionHash:run.workflowSnapshot.definitionHash}:null,coverage:'partial',source:'persisted_runtime'});
      }
      if(action==='team/catalog'&&request.method==='GET')return json(await team.catalog(projectId));
      if(action==='team/generation'&&request.method==='POST')return json(await startTeamGeneration(store,options.runtime,projectId,await body(request)));
      if(action.startsWith('team/generation/')&&request.method==='GET')return json(await teamGenerationResult(store,team,projectId,decodeURIComponent(action.slice('team/generation/'.length))));
      if(action==='team/skills/discovery'&&request.method==='GET')return json(await team.discovery(projectId,url.searchParams.get('q')??''));
      if(action==='team/skills/source-preview'&&request.method==='POST')return json(await team.sourcePreview(projectId,await body(request)));
      if(action==='team/proposals/preview'&&request.method==='POST')return json(await team.preview(projectId,await body(request,8*1024*1024)));
      if(action==='team/proposals/apply'&&request.method==='POST'){if(migration.frozen(projectId))fail('MIGRATION_BUSY');return json(await team.apply(projectId,principal.actorId,await body(request,8*1024*1024)));}
      if(action==='team/metrics'&&request.method==='GET')return json(await team.metrics(projectId,url.searchParams.get('from')??'',url.searchParams.get('to')??''));
      const copyRoute=/^team\/assets\/([^/]+)\/copy-preview$/.exec(action);if(copyRoute&&request.method==='POST'){await body(request);return json(await team.copyPreview(projectId,decodeURIComponent(copyRoute[1])));}
      const assetRoute=/^team\/assets\/([^/]+)(?:\/(history|export|resources)(?:\/(.+))?)?$/.exec(action);
      if(assetRoute&&request.method==='GET'){
        const id=decodeURIComponent(assetRoute[1]);if(assetRoute[2]==='export')return json(await team.exportAsset(projectId,id));
        if(assetRoute[2]==='resources'){const value=await team.resource(projectId,id,decodeURIComponent(assetRoute[3]??''),url.searchParams.has('version')?Number(url.searchParams.get('version')):undefined);return new Response(new Uint8Array(value.bytes),{headers:{'content-type':'application/octet-stream','content-disposition':'attachment','cache-control':'no-store','x-content-type-options':'nosniff'}});}
        const profile=await team.profile(projectId,id);return json(assetRoute[2]==='history'?{assetId:id,versions:profile.versions}:profile);
      }
      if(request.method==='GET'&&action==='sessions/catalog')return json(await sessionHistory.catalog(projectId,url.searchParams));
      if(request.method==='GET'&&action==='sessions/search')return json(await sessionHistory.search(projectId,url.searchParams));
      const transcriptRoute=/^sessions\/([^/]+)\/transcript$/.exec(action);
      if(request.method==='GET'&&transcriptRoute)return json(await sessionHistory.transcript(projectId,decodeURIComponent(transcriptRoute[1]),url.searchParams));
      if (action === 'catalogs' && request.method === 'GET') {
        const binding = await bindProject(projectId, project.canonicalRoot);
        if (binding.directoryIdentity !== project.rootIdentity) fail('PROJECT_ROOT_UNAVAILABLE');
        return json(await scanReadOnlyCatalogs(binding.workspaceRoot));
      }
      if (action === 'entities' && request.method === 'GET') {
        const kind = url.searchParams.get('kind');
        if (kind !== null && !kinds.includes(kind as EntityKind)) fail('INVALID_REQUEST');
        if (kind !== null && ['settings', 'run', 'approval'].includes(kind)) fail('PRIVATE_RUNTIME_STATE');
        const limit = Math.min(100, Math.max(1, Number(url.searchParams.get('limit') ?? 50)));
        const offset = Number(url.searchParams.get('offset') ?? 0);
        if (!Number.isSafeInteger(limit) || !Number.isSafeInteger(offset) || offset < 0) fail('INVALID_REQUEST');
        const items = await store.list(projectId, { kind: kind as EntityKind || undefined,
          parentId: url.searchParams.get('parentId') ?? undefined, limit, offset,
          order: url.searchParams.has('order') ? url.searchParams.get('order') as 'newest' : undefined });
        return json({ items: items.filter((item) => !['settings', 'run', 'approval'].includes(item.kind)), hasMore: items.length === limit });
      }
      if (action.startsWith('entities/') && request.method === 'GET') {
        const item = await store.get(projectId, decodeURIComponent(action.slice(9)));
        if (!item) fail('ENTITY_NOT_FOUND');
        if (['settings', 'run', 'approval'].includes(item.kind)) fail('PRIVATE_RUNTIME_STATE');
        return json(item);
      }
      if (action === 'commands' && request.method === 'POST') {
        if (migration.frozen(projectId)) fail('MIGRATION_BUSY');
        const input = await body(request);
        if (!Array.isArray(input.changes)) fail('INVALID_COMMAND');
        return json(await applyUserCommand(store, { projectId, actorId: principal.actorId,
          idempotencyKey: string(input.idempotencyKey), expectedAuthorityEpoch: integer(input.expectedAuthorityEpoch),
          changes: input.changes as StoreWrite['changes'] }));
      }
      const manual = /^tasks\/([^/]+)\/(check|accept)$/.exec(action);
      if (manual && request.method === 'POST') {
        const input = await body(request);
        const common = { projectId, taskId: decodeURIComponent(manual[1]), actorId: principal.actorId,
          expectedRevision: integer(input.expectedRevision), expectedAuthorityEpoch: integer(input.expectedAuthorityEpoch),
          idempotencyKey: string(input.idempotencyKey), note: typeof input.note === 'string' ? input.note : '' };
        return json(manual[2] === 'check' ? await recordManualCheck(store, { ...common, outcome: input.outcome as 'passed' | 'failed' })
          : await acceptTask(store, { ...common, checkId: string(input.checkId), accepted: input.accepted as boolean }));
      }
      if (action === 'search' && request.method === 'GET') {
        const result = await store.search(projectId, { query: url.searchParams.get('q') ?? '', limit: 50,
          offset: Number(url.searchParams.get('offset') ?? 0) });
        const visible = result.items.filter((item) => !['settings', 'run', 'approval'].includes(item.kind));
        return json({ ...result, items: visible, hasMore: result.items.length === 50 });
      }
      if (action === 'search/rebuild' && request.method === 'POST') {
        await body(request);
        await store.rebuildSearch(projectId, { signal: request.signal });
        return json({ status: 'rebuilt', coverage: (await store.search(projectId, { query: 'paos_index_coverage_probe', limit: 1 })).coverage });
      }
      if ((action === 'events' || action === 'history') && request.method === 'GET') {
        const cursor = url.searchParams.get('cursor');
        const decoded: { after?: number; generation?: string } = cursor ? decodeCursor(cursor, projectId) : {};
        // Replay retention does not limit the immutable task audit history.
        const page = action === 'history' ? await store.audit(projectId, decoded) : await store.events(projectId, decoded);
        const seq = page.items.at(-1)?.seq ?? decoded.after ?? 0;
        return json({ ...page, nextCursor: encodeCursor(projectId, page.generation, seq) });
      }
      if (action === 'imports/preview' && request.method === 'POST') {
        const input = await body(request, 3 * 1024 * 1024);
        if (input.sources !== undefined && !Array.isArray(input.sources)) fail('IMPORT_BUNDLE_INVALID');
        const preview = previewTaskImport(input.sources === undefined
          ? { projectId, sourceName: string(input.sourceName), content: string(input.content) }
          : { projectId, sources: input.sources as ImportSourceInput[] });
        const stageId = randomUUID();
        await store.write({ projectId, actorId: principal.actorId, idempotencyKey: `stage:${stageId}`,
          expectedAuthorityEpoch: project.authorityEpoch, changes: [{ expectedRevision: 0, entity: { id: stageId, kind: 'document',
            title: preview.sourceName, data: { category: 'import_staging', ...preview,
              sourceRelativePath: typeof input.sourceRelativePath === 'string' ? input.sourceRelativePath : preview.sourceName } } }] });
        return json({ stageId, parserVersion: preview.parserVersion, sourceDigest: preview.sourceDigest,
          sourceName: preview.sourceName, mode: preview.mode, proposal: preview.proposal,
          sources: preview.sources?.map(({ sourceSnapshot: _content, ...pin }) => pin), items: preview.items, blocked: preview.blocked });
      }
      if (action === 'imports/source-status' && request.method === 'GET') return json(await migration.sourceStatus(projectId));
      if ((action === 'backups'||action==='task-manager/export') && request.method === 'POST') {
        const outputRoot = join(profileDirectory, 'backups');
        await mkdir(outputRoot, { recursive: true });
        const backup = await store.backup(outputRoot);
        const rotationCandidateIds = backup.rotationCandidates.map((path) => basename(path));
        return json({ format:'paos_full_local_profile_v1',scope:'all_local_projects_tasks_catalogs_links_comments_attachments',
          restoreEndpoint:'task-manager/import-backup',backupId: basename(backup.directory), manifest: backup.manifest, rotationCandidateIds,
          retention: rotationCandidateIds.length ? 'pending' : 'complete' });
      }
      if (action === 'backups/rotation' && request.method === 'POST') {
        const input = await body(request);
        if (!Array.isArray(input.candidateIds) || input.candidateIds.length > 100
          || new Set(input.candidateIds).size !== input.candidateIds.length
          || input.candidateIds.some((id) => typeof id !== 'string' || !/^paos-backup-[a-zA-Z0-9_-]{1,150}$/.test(id))) fail('INVALID_BACKUP_PRUNE');
        const outputRoot = join(profileDirectory, 'backups');
        await pruneManagedBackups(outputRoot, input.candidateIds.map((id) => join(outputRoot, id as string)));
        return json({ rotatedBackupIds: input.candidateIds, retention: 'complete' });
      }
      if (action === 'imports/commit' && request.method === 'POST') {
        const input = await body(request);
        const result = await migration.cutover({ projectId, actorId: principal.actorId, stageId: string(input.stageId),
          currentSource: typeof input.currentSource === 'string' ? input.currentSource : '', sourceDigest: string(input.sourceDigest),
          expectedAuthorityEpoch: integer(input.expectedAuthorityEpoch), idempotencyKey: string(input.idempotencyKey) });
        return json({ receipt: result.receipt, sourceDigest: result.sourceDigest, backupId: result.backupId, mappingCount: result.mappingCount });
      }
      if (action === 'imports/export' && request.method === 'GET') return json(await migration.reverseTransfer(projectId));
      if ((action === 'restores'||action==='task-manager/import-backup') && request.method === 'POST') {
        const input = await body(request);
        const backupId = string(input.backupId);
        if (!/^[a-zA-Z0-9_-]{1,100}$/.test(backupId)) fail('BACKUP_INVALID');
        const backupRoot = await realpath(join(profileDirectory, 'backups'));
        const backupDirectory = await realpath(join(backupRoot, backupId));
        if (relative(backupRoot, backupDirectory) !== backupId) fail('BACKUP_INVALID');
        const restoreId = randomUUID();
        const destination = join(profileDirectory, 'restores', restoreId);
        await mkdir(destination, { recursive: true });
        await restoreLocalBackup(backupDirectory, join(destination, 'state.sqlite'));
        return json({ restoreId, requiresRestart: true, activeProfileChanged: false });
      }
      fail('ROUTE_NOT_FOUND');
    } catch (error) {
      const code = typeof (error as { code?: unknown }).code === 'string' ? (error as { code: string }).code : 'INVALID_REQUEST';
      const category = code.toUpperCase();
      const status = ['SESSION_REQUIRED', 'PAIRING_INVALID'].includes(category) ? 401
        : ['ORIGIN_REJECTED', 'CSRF_INVALID'].includes(category) ? 403 : category === 'JSON_REQUIRED' ? 415
        : /NOT_FOUND/.test(category) ? 404 : category === 'REQUEST_TOO_LARGE' ? 413
        : /CONFLICT|REQUIRED|UNAVAILABLE|AUTHORITY|FORBIDDEN|BLOCKED|UNVERIFIED|UNQUALIFIED|DRIFT|BUSY|STALE|PRIVATE/.test(category) ? 409 : 400;
      const cyclePath=(error as any)?.cyclePath;
      return json({ error: { code,...(Array.isArray(cyclePath)&&cyclePath.length<=100&&cyclePath.every(id=>typeof id==='string'&&/^[0-9a-f-]{36}$/.test(id))
        ?{details:{cyclePath,cyclePathTruncated:(error as any).cyclePathTruncated===true}}:{}) } }, status);
    }
  }
  return { handleRequest, issuePairingCode: gate.issuePairingCode, revokeSessions: gate.revokeAll };
}
