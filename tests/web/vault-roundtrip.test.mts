import assert from 'node:assert/strict';
import { test } from 'node:test';
import { runSyntheticVaultRoundtrip } from './single-window/vault-roundtrip.mts';

test('native-vault runner uses exactly one random namespaced fixture and removes its synthetic value', async () => {
  const values = new Map<string, string>();
  const calls: { op: string; target: string }[] = [];
  const result = await runSyntheticVaultRoundtrip({
    read: async target => { calls.push({ op: 'read', target }); return values.get(target) ?? null; },
    write: async (target, value) => { calls.push({ op: 'write', target }); values.set(target, value); },
    delete: async target => { calls.push({ op: 'delete', target }); values.delete(target); },
  });
  assert.equal(result.status, 'passed');
  assert.equal(result.roundTrip, true);
  assert.equal(result.cleanupVerified, true);
  assert.equal(new Set(calls.map(call => call.target)).size, 1);
  assert.match(result.target, /^PAOS\/PAOS-M1-fixture-[0-9a-f-]{36}\/synthetic$/);
  assert.equal(calls.filter(call => call.op === 'write').length, 1);
  assert.equal(calls.filter(call => call.op === 'delete').length, 1);
  assert.equal(values.size, 0);
  assert.equal(JSON.stringify(result).includes('PAOS_SYNTHETIC_VALUE_'), false);
});

test('a fixture collision performs no write or deletion and never exports the existing value', async () => {
  let writes = 0, deletes = 0;
  const result = await runSyntheticVaultRoundtrip({ read: async () => 'synthetic-existing-fixture-value',
    write: async () => { writes++; }, delete: async () => { deletes++; } });
  assert.equal(result.status, 'blocked');
  assert.equal(result.errorCode, 'fixture_collision');
  assert.equal(writes, 0); assert.equal(deletes, 0);
  assert.equal(JSON.stringify(result).includes('existing-fixture-value'), false);
});

test('an uncertain write is reconciled and cleaned only when the value is still the newly generated fixture', async () => {
  let value: string | null = null, deletes = 0;
  const result = await runSyntheticVaultRoundtrip({ read: async () => value,
    write: async (_target, text) => { value = text; throw new Error('lost acknowledgement'); },
    delete: async () => { deletes++; value = null; } });
  assert.equal(result.status, 'failed');
  assert.equal(result.cleanupVerified, true); assert.equal(deletes, 1); assert.equal(value, null);
  assert.equal(JSON.stringify(result).includes('lost acknowledgement'), false);
});

test('changed ownership prevents cleanup from deleting another value', async () => {
  let reads = 0, deletes = 0;
  const result = await runSyntheticVaultRoundtrip({ read: async () => ++reads === 1 ? null : 'synthetic-intervening-value',
    write: async () => {}, delete: async () => { deletes++; } });
  assert.equal(result.status, 'failed');
  assert.equal(result.errorCode, 'cleanup_ownership_unverified');
  assert.equal(result.cleanupVerified, false); assert.equal(deletes, 0);
});

test('an initial read failure never attempts a write or deletion', async () => {
  let writes = 0, deletes = 0;
  const result = await runSyntheticVaultRoundtrip({ read: async () => { throw new Error('synthetic read failure'); },
    write: async () => { writes++; }, delete: async () => { deletes++; } });
  assert.equal(result.status, 'failed'); assert.equal(result.writeAttempted, false);
  assert.equal(writes, 0); assert.equal(deletes, 0);
});

test('a cleanup read failure never deletes a target with unverified ownership', async () => {
  let reads = 0, value: string | null = null, deletes = 0;
  const result = await runSyntheticVaultRoundtrip({ read: async () => {
    if (++reads === 3) throw new Error('synthetic cleanup read failure');
    return value;
  }, write: async (_target, text) => { value = text; }, delete: async () => { deletes++; value = null; } });
  assert.equal(result.status, 'failed'); assert.equal(result.errorCode, 'cleanup_failed');
  assert.equal(result.cleanupVerified, false); assert.equal(deletes, 0);
});

test('a failed deletion is reported without claiming that the fixture was removed', async () => {
  let value: string | null = null;
  const result = await runSyntheticVaultRoundtrip({ read: async () => value, write: async (_target, text) => { value = text; },
    delete: async () => { throw new Error('synthetic delete failure'); } });
  assert.equal(result.status, 'failed'); assert.equal(result.errorCode, 'cleanup_failed');
  assert.equal(result.cleanupVerified, false); assert.equal(result.cleanupOwnedValueMatched, true);
});
