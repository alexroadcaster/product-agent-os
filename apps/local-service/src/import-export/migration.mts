import { randomUUID } from 'node:crypto';
import { mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import type { LocalStore } from '../storage/local-store.mts';
import { restoreLocalBackup } from '../storage/local-store.mts';
import { previewTaskImport, type ImportSourceInput } from './preview.mts';
import { withFrozenSource, type FrozenSource } from './source-freeze.mts';
import { bindProject } from '../adapters/project-sources.ts';
import type { ImportSourceBinding } from '../../../../packages/contracts/storage/local-store.ts';

export type WriterRoute = { id: string; role: 'reader' | 'writer'; route: 'read_adapter' | 'domain_adapter' | 'unsupported';
  sourceDigest: string; verified: boolean };
export type WriterInventory = { entries: readonly WriterRoute[]; complete: boolean };
function fail(code: string): never { throw Object.assign(new Error(code), { code }); }

/** Cutover requires a server-owned inventory. Unknown external writers keep legacy authority intact. */
export function inventoryAllowsCutover(inventory: WriterInventory): boolean {
  return inventory.complete && inventory.entries.length > 0
    && new Set(inventory.entries.map((entry) => entry.id)).size === inventory.entries.length
    && inventory.entries.every((entry) => entry.verified && /^[a-f0-9]{64}$/.test(entry.sourceDigest)
      && (entry.role === 'reader' ? entry.route === 'read_adapter' : entry.route === 'domain_adapter'));
}

export function createMigrationManager({ store, profileDirectory, inventory, freeze = withFrozenSource }: {
  store: LocalStore; profileDirectory: string; inventory: (projectId: string) => Promise<WriterInventory>;
  freeze?: typeof withFrozenSource;
}) {
  const freezes = new Set<string>();
  async function holdSources<T>(workspaceRoot: string, sources: readonly ImportSourceBinding[], operation: (leases: FrozenSource[]) => Promise<T>,
    leases: FrozenSource[] = []): Promise<T> {
    const source = sources[leases.length];
    if (!source) return operation(leases);
    return freeze({ workspaceRoot, sourceRelativePath: source.sourceRelativePath }, lease => holdSources(workspaceRoot, sources, operation, [...leases, lease]));
  }
  function assertHeld(leases: readonly FrozenSource[]) { for (const lease of leases) lease.assertHeld(); }
  return {
    frozen: (projectId: string) => freezes.has(projectId),
    inventory,
    async cutover(input: { projectId: string; stageId: string; actorId: string; currentSource?: string; currentSources?: readonly ImportSourceInput[];
      sourceDigest: string; expectedAuthorityEpoch: number; idempotencyKey: string }) {
      if (freezes.has(input.projectId)) fail('MIGRATION_BUSY');
      freezes.add(input.projectId);
      try {
        const stage = await store.get(input.projectId, input.stageId);
        if (!stage || stage.kind !== 'document' || stage.data.category !== 'import_staging') fail('STAGING_NOT_FOUND');
        const bundled = Array.isArray(stage.data.sources);
        const sources = bundled ? input.currentSources ?? (stage.data.sources as Record<string, unknown>[]).map(source => ({
          role: source.role as 'records' | 'projection', sourceName: String(source.sourceName),
          sourceRelativePath: String(source.sourceRelativePath), content: String(source.sourceSnapshot),
        })) : undefined;
        const preview = sources ? previewTaskImport({ projectId: input.projectId, sources })
          : previewTaskImport({ projectId: input.projectId, sourceName: String(stage.data.sourceName),
            content: input.currentSource ?? String(stage.data.sourceSnapshot) });
        const digest = preview.sourceDigest;
        if (stage.data.sourceDigest !== input.sourceDigest || digest !== input.sourceDigest) fail('SOURCE_DRIFT');
        if (preview.mode === 'normalized_proposal') fail('IMPORT_PROPOSAL_ONLY');
        if (preview.blocked.length || preview.items.length === 0) fail('IMPORT_UNSUPPORTED');
        const bindings: ImportSourceBinding[] = preview.sources
          ? preview.sources.map(({ sourceSnapshot: _snapshot, ...source }) => source)
          : [{ role: 'records', sourceName: preview.sourceName, sourceRelativePath: String(stage.data.sourceRelativePath ?? preview.sourceName),
            sourceDigest: digest, byteSize: Buffer.byteLength(preview.sourceSnapshot) }];
        bindings.sort((a, b) => a.sourceRelativePath.toLowerCase() < b.sourceRelativePath.toLowerCase() ? -1 : 1);
        const previous = await store.receipt(input.projectId, input.idempotencyKey);
        const boundSources = previous ? await store.get(input.projectId, 'runtime-import-sources') : null;
        const promotion = { projectId: input.projectId, actorId: input.actorId,
          expectedAuthorityEpoch: input.expectedAuthorityEpoch, sourceDigest: input.sourceDigest, verifiedSourceDigest: digest,
          writerInventoryVerified: true, restoreRehearsalVerified: true, items: preview.items.map((item) => item.task),
          idempotencyKey: input.idempotencyKey, ...(!previous || boundSources ? { sourceBindings: bindings } : {}) };
        if (previous) {
          const receipt = await store.promoteLegacy({...promotion,
            ...(previous.cutoverBackupId ? {cutoverBackupId:previous.cutoverBackupId} : {})});
          return { receipt, sourceDigest: digest, backupId: receipt.cutoverBackupId ?? null, mappingCount: preview.items.length, replayed: true };
        }
        const project = await store.project(input.projectId);
        if (!project) fail('PROJECT_NOT_FOUND');
        const binding = await bindProject(input.projectId, project.canonicalRoot);
        if (binding.directoryIdentity !== project.rootIdentity) fail('PROJECT_ROOT_UNAVAILABLE');
        return await holdSources(binding.workspaceRoot, bindings, async leases => {
        if (leases.some((lease, index) => lease.sha256 !== bindings[index].sourceDigest || lease.byteSize !== bindings[index].byteSize)) fail('SOURCE_DRIFT');
        assertHeld(leases);
        if (!inventoryAllowsCutover(await inventory(input.projectId))) fail('WRITER_INVENTORY_INCOMPLETE');
        const backupRoot = join(profileDirectory, 'backups');
        await mkdir(backupRoot, { recursive: true });
        const backup = await store.backup(backupRoot);
        const rehearsalRoot = join(profileDirectory, 'restore-rehearsals', randomUUID());
        await mkdir(rehearsalRoot, { recursive: true });
        const restored = await restoreLocalBackup(backup.directory, join(rehearsalRoot, 'state.sqlite'));
        if (!restored.generationChanged) fail('RESTORE_REHEARSAL_FAILED');
        assertHeld(leases);
        const backupId = backup.directory.split(/[\\/]/).at(-1)!;
        const receipt = await store.promoteLegacy({...promotion,cutoverBackupId:backupId});
        assertHeld(leases);
        return { receipt, sourceDigest: digest, backupId,
          mappingCount: preview.items.length, project: await store.project(input.projectId) };
        });
      } finally { freezes.delete(input.projectId); }
    },
    async sourceStatus(projectId: string) {
      const project = await store.project(projectId);
      if (!project) fail('PROJECT_NOT_FOUND');
      const metadata = await store.get(projectId, 'runtime-import-sources');
      const pins = metadata?.data.bindings;
      if (!Array.isArray(pins) || pins.length < 1 || pins.length > 2) return { authorityMode: project.authorityMode, items: [] };
      const bindings = pins as ImportSourceBinding[];
      const unavailable = () => bindings.map(source => ({ sourceName: source.sourceName, sourceRelativePath: source.sourceRelativePath,
        sourceDigest: source.sourceDigest, status: 'unavailable' as const }));
      try {
        const binding = await bindProject(projectId, project.canonicalRoot);
        if (binding.directoryIdentity !== project.rootIdentity || metadata!.data.authorityEpoch !== project.authorityEpoch) fail('PROJECT_ROOT_UNAVAILABLE');
        const items = await holdSources(binding.workspaceRoot, bindings, async leases => {
          assertHeld(leases);
          return bindings.map((source, index) => ({ sourceName: source.sourceName, sourceRelativePath: source.sourceRelativePath,
            sourceDigest: source.sourceDigest, observedDigest: leases[index].sha256,
            status: leases[index].sha256 === source.sourceDigest && leases[index].byteSize === source.byteSize ? 'unchanged' as const : 'changed' as const }));
        });
        return { authorityMode: project.authorityMode, items };
      } catch { return { authorityMode: project.authorityMode, items: unavailable() }; }
    },
    /** Stage every current SQL task. A pre-cutover backup never replaces later work. */
    async reverseTransfer(projectId: string) {
      const snapshot = await store.exportTasks(projectId);
      const baseRevisions: Record<string, number> = {};
      for (let offset = 0; offset <= 10000; offset += 100) {
        const rows = await store.list(projectId, { kind: 'task', limit: 100, offset });
        for (const row of rows) baseRevisions[row.id] = row.revision;
        if (rows.length < 100) break;
      }
      const verified = await store.exportTasks(projectId);
      if (verified.project.authorityEpoch !== snapshot.project.authorityEpoch || verified.generation !== snapshot.generation
        || verified.throughSeq !== snapshot.throughSeq || Object.keys(baseRevisions).length !== snapshot.tasks.length) fail('EXPORT_CONFLICT');
      return { schema_version: 'm1_task_profile_v1', projectId, authorityEpoch: snapshot.project.authorityEpoch,
        streamGeneration: snapshot.generation, throughSeq: snapshot.throughSeq, baseRevisions, tasks: snapshot.tasks,
        authority: 'sql', operation: 'staged_reverse_transfer' };
    },
  };
}
