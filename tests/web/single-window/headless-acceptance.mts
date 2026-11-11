import { randomUUID } from 'node:crypto';
import { mkdtemp, mkdir, readFile, rm, stat, writeFile, link, unlink } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join, resolve } from 'node:path';
import { runNativeLauncher } from '../../../apps/launcher/main.mts';
import { newTask } from '../../../apps/web/src/api/task.ts';
import { withFrozenSource } from '../../../apps/local-service/src/import-export/source-freeze.mts';

if (process.argv[2] !== '--synthetic') throw new Error('Explicit synthetic acceptance mode is required');
const scratch = fileURLToPath(new URL('../../../.tmp/paos-m1/', import.meta.url));
const root = await mkdtemp(join(scratch, 'headless-'));
if (resolve(root, '..') !== resolve(scratch)) throw new Error('Unexpected fixture root');
const profile = join(root, 'profile');
const workspace = join(root, 'workspace');
await mkdir(profile); await mkdir(workspace);
const checks: string[] = [];
const evidence: Record<string, unknown> = { syntheticOnly: true, browserUsed: false, providerUsed: false,
  realKeysUsed: false, systemPoliciesChanged: false, checks, startedAt: new Date().toISOString() };
const check = (name: string, passed: boolean) => { if (!passed) throw new Error(name); checks.push(name); };
try {
  const result = await runNativeLauncher({ profileDirectory: profile,
    async showWindow({ origin, pairingCode }) {
      const index = await fetch(origin, { signal: AbortSignal.timeout(5000) });
      check('built_web_html_served', index.status === 200 && (await index.text()).includes('<div id="root">'));
      let cookie = '', csrf = '';
      async function request(path: string, payload?: unknown, method = payload === undefined ? 'GET' : 'POST', extra: Record<string, string> = {}) {
        // Native cutover holds up to two source locks under the existing 30s lease deadline.
        // Ordinary HTTP checks retain 5s; import has no product 5s latency contract.
        const timeoutMs=method==='POST'&&path.endsWith('/imports/commit')?35000:path.endsWith('/imports/source-status')?65000:5000;
        evidence.lastRequest={path,method,timeoutMs};
        return fetch(`${origin}/api/v1${path}`, { method, signal: AbortSignal.timeout(timeoutMs),
          headers: { origin, cookie, 'x-paos-csrf': csrf, 'content-type': 'application/json', ...extra },
          ...(payload === undefined ? {} : { body: JSON.stringify(payload) }) });
      }
      check('unpaired_data_rejected', (await request('/projects')).status === 401);
      const pair = await request('/bootstrap/exchange', { code: pairingCode });
      check('private_pairing_exchange', pair.status === 200 && pair.headers.get('set-cookie')?.includes('HttpOnly') === true);
      cookie = pair.headers.get('set-cookie')!.split(';')[0];
      csrf = (await pair.json()).csrfToken;
      const denied = await request('/projects', { name: 'Foreign', workspaceRoot: workspace }, 'POST', { origin: 'https://untrusted.invalid' });
      check('cross_origin_write_rejected', denied.status === 403);
      const created = await request('/projects', { name: 'Synthetic', keyPrefix: 'PAOS', workspaceRoot: workspace });
      check('project_registered', created.status === 201);
      const project = await created.json();
      const task = newTask(project.id, 'Synthetic acceptance task', 'Only fixture data', ['Owner verifies the synthetic result']);
      const command = { expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'synthetic-create',
        changes: [{ expectedRevision: 0, entity: task }] };
      check('task_committed', (await request(`/projects/${project.id}/commands`, command)).status === 200);
      const page = await (await request(`/projects/${project.id}/entities?kind=task`)).json();
      check('task_public_key_allocated', page.items.length === 1 && page.items[0].publicKey === 'PAOS-1');
      check('same_command_retry', (await request(`/projects/${project.id}/commands`, command)).status === 200);
      const found = await (await request(`/projects/${project.id}/search?q=Synthetic`)).json();
      check('fts_finds_committed_task', found.items.some((item: { id: string }) => item.id === task.id));
      await request('/preferences', { locale: 'en', theme: 'dark' }, 'PUT');
      const preferences = await (await request('/preferences')).json();
      check('preferences_persisted', preferences.locale === 'en' && preferences.theme === 'dark');
      const sessionId = randomUUID();
      const draftId = randomUUID();
      check('session_draft_committed', (await request(`/projects/${project.id}/commands`, {
        expectedAuthorityEpoch: project.authorityEpoch, idempotencyKey: 'session-draft', changes: [
          { expectedRevision: 0, entity: { id: sessionId, kind: 'session', title: 'Fixture session' } },
          { expectedRevision: 0, entity: { id: draftId, kind: 'draft', parentId: sessionId, body: 'Unsaved provider work remains local' } },
        ] })).status === 200);
      const connection = await (await request('/connection')).json();
      check('no_provider_connection', connection.verified === false);
      const state = await (await request(`/runtime/state?projectId=${project.id}&sessionId=${sessionId}`)).json();
      const deniedSend=await request('/runtime/send', {
        projectId: project.id, sessionId, input: 'Never dispatch this fixture' });
      const denial=await deniedSend.json();
      // The default App route has no attached worker or binding; no inference runtime is launched.
      check('send_fails_closed', connection.route==='codex_app_agent' && state.canSend===false
        && state.reason==='app_agent_not_attached' && deniedSend.status===404 && denial.error?.code==='binding_not_found');
      const backup = await request(`/projects/${project.id}/backups`, {});
      check('real_database_backup', backup.status === 200);
      const backupReceipt = await backup.json();
      const restored = await request(`/projects/${project.id}/restores`, { backupId: backupReceipt.backupId });
      check('restore_separate_profile', restored.status === 200 && (await restored.json()).activeProfileChanged === false);
      const exported = await (await request(`/projects/${project.id}/imports/export`)).json();
      check('reverse_export_keeps_current_task', exported.tasks.length === 1 && exported.tasks[0].id === task.id);
      const normalized = await (await request(`/projects/${project.id}/imports/preview`, {
        sourceName: 'reverse.json', content: JSON.stringify(exported) })).json();
      check('reverse_export_reimport_stays_a_proposal', normalized.mode === 'normalized_proposal'
        && normalized.proposal?.baseRevisions?.[task.id] === 1);
      await writeFile(join(workspace, 'REQUIREMENTS.md'), '# Synthetic readable source\n');
      const sourceRead = await (await request(`/projects/${project.id}/sources/requirements`)).json();
      check('fixed_project_source_read_hash', sourceRead.content === '# Synthetic readable source\n' && /^[a-f0-9]{64}$/.test(sourceRead.sha256));
      const legacyRoot = join(root, 'legacy');
      await mkdir(legacyRoot);
      const source = JSON.stringify({ schema_version: 'paos_web_task_groups_v1', tasks: [
        { id: 'IMPT-0001', title: 'Legacy fixture', status: 'planned', depends_on: [] },
      ] });
      const sourcePath = join(legacyRoot, 'tasks.json');
      await writeFile(sourcePath, source);
      await withFrozenSource({ workspaceRoot: legacyRoot, sourceRelativePath: 'tasks.json' }, async (lease) => {
        lease.assertHeld();
        let denied = false;
        try { await writeFile(sourcePath, source + ' '); } catch (error) {
          denied = ['EACCES', 'EBUSY', 'EPERM'].includes((error as NodeJS.ErrnoException).code ?? '');
        }
        check('native_source_lock_denies_concurrent_write', denied);
      });
      await writeFile(sourcePath, source);
      check('source_write_allowed_after_release', await readFile(sourcePath, 'utf8') === source);
      const alias = join(legacyRoot, 'alias.json');
      await link(sourcePath, alias);
      let linkedRejected = false;
      try { await withFrozenSource({ workspaceRoot: legacyRoot, sourceRelativePath: 'alias.json' }, async () => {}); }
      catch { linkedRejected = true; }
      await unlink(alias);
      check('native_source_hardlink_rejected', linkedRejected);
      const legacyProject = await (await request('/projects', { name: 'Imported', keyPrefix: 'IMPT', workspaceRoot: legacyRoot, legacySource: true })).json();
      const single = await (await request(`/projects/${legacyProject.id}/imports/preview`, { sourceName: 'tasks.json', content: source })).json();
      check('legacy_preview_retains_original_alias', single.items?.[0]?.task?.legacyAlias === 'IMPT-0001');
      const projection = ['### Task `IMPT-0001`', '- Task: Legacy fixture', '- Status: planned',
        '- Schema version: task_matrix_plan_v1', '- Depends on: none'].join('\n');
      const projectionPath = join(legacyRoot, 'tasks.md');
      await writeFile(projectionPath, projection);
      const sources = [{ role: 'records', sourceName: 'tasks.json', sourceRelativePath: 'tasks.json', content: source },
        { role: 'projection', sourceName: 'tasks.md', sourceRelativePath: 'tasks.md', content: projection }];
      const conflict = await (await request(`/projects/${legacyProject.id}/imports/preview`, { sources:
        sources.map((item) => item.role === 'projection' ? { ...item, content: projection.replace('Legacy fixture', 'Conflicting fixture') } : item) })).json();
      check('json_markdown_conflict_is_blocked', conflict.blocked?.length > 0);
      const preview = await (await request(`/projects/${legacyProject.id}/imports/preview`, { sources })).json();
      check('json_markdown_bundle_deduplicated', preview.items?.length === 1 && preview.blocked?.length === 0 && preview.sources?.length === 2);
      const cutover = { stageId: preview.stageId, sourceDigest: preview.sourceDigest,
        expectedAuthorityEpoch: legacyProject.authorityEpoch, idempotencyKey: 'native-cutover' };
      await writeFile(sourcePath, source + ' ');
      check('server_rereads_source_and_rejects_drift', (await request(`/projects/${legacyProject.id}/imports/commit`, cutover)).status === 409);
      await writeFile(sourcePath, source);
      await writeFile(projectionPath, projection + '\n');
      check('projection_source_drift_rejected', (await request(`/projects/${legacyProject.id}/imports/commit`, cutover)).status === 409);
      await writeFile(projectionPath, projection);
      const promoted = await request(`/projects/${legacyProject.id}/imports/commit`, cutover);
      check('native_locked_cutover_with_restore_rehearsal', promoted.status === 200 && (await promoted.clone().json()).mappingCount === 1);
      const beforeChange = await (await request(`/projects/${legacyProject.id}/imports/source-status`)).json();
      check('cutover_retains_both_source_bindings', beforeChange.items?.length === 2 && beforeChange.items.every((item: { status: string }) => item.status === 'unchanged'));
      await writeFile(sourcePath, source + ' ');
      const afterChange = await (await request(`/projects/${legacyProject.id}/imports/source-status`)).json();
      check('legacy_edit_after_cutover_is_visible_without_auto_import', afterChange.items?.some((item: { status: string }) => item.status === 'changed'));
      const repeated = await request(`/projects/${legacyProject.id}/imports/commit`, cutover);
      check('cutover_retry_after_source_edit_returns_committed_receipt', repeated.status === 200);
      check('authenticated_quit_requested', (await request('/quit', {})).status === 202);
      return 'closed';
    },
  });
  check('normal_launcher_entrypoint', result.status === 'opened');
  const lock = join(profile, 'service-instance');
  for (let count = 0; count < 50; count++) {
    try { await stat(lock); } catch { break; }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  let removed = false;
  try { await stat(lock); } catch { removed = true; }
  check('quit_acknowledged_and_reservation_released', removed);
  evidence.status = 'passed_headless_local';
} catch (error) {
  evidence.status = 'failed'; evidence.failedCheck = error instanceof Error ? error.message : 'unknown';
  evidence.failureCode=typeof (error as {code?:unknown})?.code==='string'?(error as {code:string}).code:null;process.exitCode = 1;
} finally {
  const lock = join(profile, 'service-instance');
  let live = false;
  try { await stat(lock); live = true; } catch { /* No live reservation remains. */ }
  if (!live) { await rm(root, { recursive: true, force: true }); evidence.fixtureCleaned = true; }
  else evidence.fixtureCleaned = false;
  evidence.finishedAt = new Date().toISOString();
  await writeFile(join(scratch, 'headless-result.json'), JSON.stringify(evidence, null, 2));
  console.log(JSON.stringify(evidence, null, 2));
}
