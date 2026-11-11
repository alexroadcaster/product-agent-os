import { createHash } from 'node:crypto';
import { lstat, readFile, readdir } from 'node:fs/promises';
import { isAbsolute, join, relative } from 'node:path';
import { arch, platform, release } from 'node:os';
import { fileURLToPath } from 'node:url';

const sourceRoot = fileURLToPath(new URL('../../../', import.meta.url));
export type RuntimeFingerprint = { version: string; sha256: string };
export type RuntimeManifest = {
  schemaVersion: 'paos_runtime_manifest_v1'; qualification: 'native_offline';
  platform: string; arch: string; windowsRelease: string;
  codex: RuntimeFingerprint; node: RuntimeFingerprint; sqliteVersion: string;
  adapterRevision: string; packageLockSha256: string;
  schema: { sha256: string; v2Sha256: string };
  capabilities: { projectHistory: boolean; scopedExecution: boolean; ephemeralAuth: boolean; fts5: boolean; backupRestore: boolean };
  evidence: Record<string, string>;
};
const sha256 = (bytes: Uint8Array | string) => createHash('sha256').update(bytes).digest('hex');
type CurrentTuple = Pick<RuntimeManifest, 'platform' | 'arch' | 'windowsRelease' | 'node' | 'sqliteVersion' | 'adapterRevision' | 'packageLockSha256'> & { codexSha256: string };

/** Qualification is an exact local tuple check; it never establishes model access or commercial admission. */
export function inspectRuntimeTuple(manifest: RuntimeManifest, current: CurrentTuple): string[] {
  const reasons: string[] = [];
  if (manifest.schemaVersion !== 'paos_runtime_manifest_v1' || manifest.qualification !== 'native_offline') reasons.push('manifest_invalid');
  if (manifest.platform !== current.platform || manifest.arch !== current.arch || manifest.windowsRelease !== current.windowsRelease) reasons.push('platform_mismatch');
  if (manifest.codex.sha256 !== current.codexSha256) reasons.push('runtime_mismatch');
  if (manifest.node.version !== current.node.version || manifest.node.sha256 !== current.node.sha256) reasons.push('node_mismatch');
  if (manifest.sqliteVersion !== current.sqliteVersion) reasons.push('sqlite_mismatch');
  if (manifest.adapterRevision !== current.adapterRevision) reasons.push('adapter_mismatch');
  if (manifest.packageLockSha256 !== current.packageLockSha256) reasons.push('package_lock_mismatch');
  const required = ['projectHistory', 'scopedExecution', 'ephemeralAuth', 'fts5', 'backupRestore'] as const;
  if (!manifest.capabilities || required.some((name) => manifest.capabilities[name] !== true)
    || Object.keys(manifest.capabilities).length !== required.length) reasons.push('capability_unverified');
  return reasons;
}

/** Pin the executable local host and contracts, including transitive admission/storage guards, independently of Git. */
export async function adapterRevision(root = sourceRoot): Promise<string> {
  const paths: string[] = [];
  async function visit(path: string) {
    for (const item of await readdir(path, { withFileTypes: true })) {
      const entry = join(path, item.name);
      if (item.isSymbolicLink()) throw new Error('Linked runtime source is unsupported');
      if (item.isDirectory()) await visit(entry);
      else if (/\.(?:mts|ts|ps1)$/.test(item.name)) paths.push(entry);
    }
  }
  for (const area of ['apps/local-service/src', 'apps/launcher', 'packages/contracts']) {
    await visit(join(root, area));
  }
  const hash = createHash('sha256');
  for (const path of paths.sort()) hash.update(relative(root, path).replaceAll('\\', '/')).update('\0').update(await readFile(path)).update('\0');
  return hash.digest('hex');
}

/** The optional selection names a binary, never credentials or fallback configuration. This performs no process launch. */
export async function inspectConfiguredRuntime(profileDirectory: string) {
  let manifest: RuntimeManifest;
  try {
    manifest = JSON.parse(await readFile(new URL('./qualified-manifest.json', import.meta.url), 'utf8'));
  } catch { return { fingerprint: null, expected: null, qualified: false, reasons: ['manifest_unavailable'] }; }
  const expected = manifest.codex;
  try {
    const selection = JSON.parse(await readFile(join(profileDirectory, 'runtime-selection.json'), 'utf8'));
    const binaryPath = selection.binaryPath;
    if (typeof binaryPath !== 'string' || !isAbsolute(binaryPath) || binaryPath.startsWith('\\')) throw new Error('Invalid runtime path');
    const file = await lstat(binaryPath);
    if (!file.isFile() || file.isSymbolicLink()) throw new Error('Invalid runtime file');
    const fingerprint = { version: expected.version, sha256: sha256(await readFile(binaryPath)) };
    const reasons = inspectRuntimeTuple(manifest, { platform: platform(), arch: arch(), windowsRelease: release(),
      codexSha256: fingerprint.sha256, node: { version: process.version, sha256: sha256(await readFile(process.execPath)) },
      sqliteVersion: process.versions.sqlite!, adapterRevision: await adapterRevision(),
      packageLockSha256: sha256(await readFile(join(sourceRoot, 'apps/web/package-lock.json'))) });
    return { fingerprint, expected, qualified: reasons.length === 0, reasons, binaryPath };
  } catch { return { fingerprint: null, expected, qualified: false, reasons: ['runtime_not_configured'] }; }
}
