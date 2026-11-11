import assert from 'node:assert/strict';
import { test } from 'node:test';
import { inspectRuntimeTuple, adapterRevision, type RuntimeManifest } from '../../packages/contracts/runtime/manifest.mts';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const manifest: RuntimeManifest = {
  schemaVersion: 'paos_runtime_manifest_v1', qualification: 'native_offline',
  platform: 'win32', arch: 'x64', windowsRelease: 'synthetic-build',
  codex: { version: 'fixture', sha256: 'a'.repeat(64) },
  node: { version: 'fixture-node', sha256: 'b'.repeat(64) }, sqliteVersion: 'fixture-sqlite',
  adapterRevision: 'c'.repeat(64), packageLockSha256: 'd'.repeat(64),
  schema: { sha256: 'e'.repeat(64), v2Sha256: 'f'.repeat(64) },
  capabilities: { projectHistory: true, scopedExecution: true, ephemeralAuth: true, fts5: true, backupRestore: true },
  evidence: { synthetic: '1'.repeat(64) },
};
const current = { platform: manifest.platform, arch: manifest.arch, windowsRelease: manifest.windowsRelease,
  codexSha256: manifest.codex.sha256, node: manifest.node, sqliteVersion: manifest.sqliteVersion,
  adapterRevision: manifest.adapterRevision, packageLockSha256: manifest.packageLockSha256 };

test('qualifies only the exact locally observed runtime tuple and all required capabilities', () => {
  assert.deepEqual(inspectRuntimeTuple(manifest, current), []);
  for (const [field, reason] of [['codexSha256', 'runtime_mismatch'], ['adapterRevision', 'adapter_mismatch'],
    ['packageLockSha256', 'package_lock_mismatch'], ['sqliteVersion', 'sqlite_mismatch'],
    ['windowsRelease', 'platform_mismatch']] as const) {
    assert.ok(inspectRuntimeTuple(manifest, { ...current, [field]: 'changed' }).includes(reason), field);
  }
  assert.ok(inspectRuntimeTuple({ ...manifest, capabilities: { ...manifest.capabilities, ephemeralAuth: false } }, current)
    .includes('capability_unverified'));
  assert.ok(inspectRuntimeTuple(manifest, { ...current, node: { ...current.node, sha256: 'changed' } }).includes('node_mismatch'));
});

test('pins executable host admission, HTTP guards and storage alongside the runtime adapter', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-manifest-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  for (const area of ['apps/local-service/src/runtime', 'apps/local-service/src/connections', 'apps/local-service/src/commands',
    'apps/local-service/src/http', 'apps/local-service/src/storage', 'apps/launcher', 'packages/contracts']) {
    await mkdir(join(root, area), { recursive: true });
    await writeFile(join(root, area, 'fixture.mts'), 'export const revision = 1;');
  }
  const initial = await adapterRevision(root);
  for (const area of ['apps/local-service/src/http', 'apps/local-service/src/storage', 'apps/launcher', 'packages/contracts']) {
    await writeFile(join(root, area, 'fixture.mts'), 'export const revision = 2;');
    assert.notEqual(await adapterRevision(root), initial, area);
    await writeFile(join(root, area, 'fixture.mts'), 'export const revision = 1;');
  }
});
