import type { CredentialStore } from '../../../apps/local-service/src/connections/broker.ts';
import { createWindowsCredentialStore } from '../../../apps/local-service/src/connections/windows-credential-store.ts';
import { randomUUID, createHash } from 'node:crypto';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

type Result = { status: 'passed' | 'failed' | 'blocked'; syntheticOnly: true; target: string;
  initiallyAbsent: boolean; writeAttempted: boolean; writeAcknowledged: boolean;
  roundTrip: boolean; cleanupOwnedValueMatched: boolean; cleanupVerified: boolean; errorCode?: string };

/** Only a fresh, unshared synthetic target is permitted. Never enumerate or accept caller-supplied names/values. */
export async function runSyntheticVaultRoundtrip(store: CredentialStore): Promise<Result> {
  const target = `PAOS/PAOS-M1-fixture-${randomUUID()}/synthetic`;
  const value = `PAOS_SYNTHETIC_VALUE_${randomUUID()}`;
  const result: Result = { status: 'failed', syntheticOnly: true, target, initiallyAbsent: false,
    writeAttempted: false, writeAcknowledged: false, roundTrip: false, cleanupOwnedValueMatched: false, cleanupVerified: false };
  try {
    if (await store.read(target) !== null) { result.status = 'blocked'; result.errorCode = 'fixture_collision'; return result; }
    result.initiallyAbsent = true;
    // A failed acknowledgement does not prove that the OS write did not commit.
    result.writeAttempted = true;
    await store.write(target, value);
    result.writeAcknowledged = true;
    result.roundTrip = await store.read(target) === value;
    if (!result.roundTrip) result.errorCode = 'roundtrip_mismatch';
  } catch {
    result.errorCode = 'vault_roundtrip_failed';
  } finally {
    if (result.initiallyAbsent && result.writeAttempted) {
      try {
        const current = await store.read(target);
        if (current === null) result.cleanupVerified = true;
        else if (current === value) {
          result.cleanupOwnedValueMatched = true;
          await store.delete(target);
          result.cleanupVerified = await store.read(target) === null;
          if (!result.cleanupVerified) result.errorCode = 'cleanup_failed';
        } else result.errorCode = 'cleanup_ownership_unverified';
      } catch { result.errorCode = 'cleanup_failed'; }
    }
  }
  if (result.initiallyAbsent && result.writeAcknowledged && result.roundTrip && result.cleanupVerified && !result.errorCode) result.status = 'passed';
  return result;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 3 || process.argv[2] !== '--synthetic-vault') throw new Error('Explicit synthetic-vault mode is required');
  const startedAt = new Date().toISOString();
  const result = await runSyntheticVaultRoundtrip(createWindowsCredentialStore());
  const { target: _target, ...safe } = result;
  const sourceDigests: Record<string, string> = {};
  for (const path of ['apps/local-service/src/connections/windows-credential-store.ts',
    'apps/local-service/src/connections/windows-credential-bridge.ps1', 'tests/web/single-window/vault-roundtrip.mts']) {
    sourceDigests[path] = createHash('sha256').update(await readFile(new URL(`../../../${path}`, import.meta.url))).digest('hex');
  }
  const receipt = { ...safe, native: true, providerUsed: false, browserUsed: false, realKeysUsed: false,
    existingTargetsEnumerated: false, targetFamily: 'PAOS/PAOS-M1-fixture-<uuid>/synthetic',
    startedAt, finishedAt: new Date().toISOString(), sourceDigests };
  const directory = new URL('../../../.tmp/paos-m1/', import.meta.url);
  await mkdir(directory, { recursive: true });
  await writeFile(new URL('native-vault-result-2026-11-11.json', directory), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt));
  if (receipt.status !== 'passed') process.exitCode = 1;
}
