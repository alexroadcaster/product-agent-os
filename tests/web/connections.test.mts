import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createConnectionBroker } from '../../apps/local-service/src/connections/broker.ts';

test('keeps credentials ephemeral, never infers model access, and clears on disconnect', async () => {
  const calls: Array<{ method: string; params: unknown }> = [];
  const broker = createConnectionBroker({ profileId: 'synthetic-profile', request: async (method, params) => {
    calls.push({ method, params });
    if (method === 'account/read') return { account: { type: 'apiKey' }, requiresOpenaiAuth: true };
    return { type: 'apiKey' };
  } });
  assert.equal(broker.snapshot().state, 'unverified');
  await broker.connect({ connectionId: 'synthetic-connection', apiKey: 'synthetic-secret', remember: false });
  assert.equal(broker.snapshot().state, 'connected');
  assert.equal(broker.snapshot().modelAccess, 'unverified');
  assert.equal(JSON.stringify(broker.snapshot()).includes('synthetic-secret'), false);
  assert.equal(calls.filter((call) => call.method === 'account/login/start').length, 1);
  assert.equal(broker.authorize(broker.accountScopeId()!), true);
  assert.equal(JSON.stringify(broker.snapshot()).includes(broker.accountScopeId()!), false);
  await broker.disconnect();
  assert.equal(broker.authorize('synthetic-connection'), false);
  assert.equal(broker.snapshot().state, 'disconnected');
});

test('secure-store bridge accepts only namespaced targets and uses no implicit OS calls', async () => {
  const { createWindowsCredentialStore } = await import('../../apps/local-service/src/connections/windows-credential-store.ts');
  const received: unknown[] = [];
  const store = createWindowsCredentialStore(async (input) => { received.push(input); return input.operation==='read'?{secret:'synthetic-secret'}:{}; });
  await store.write('PAOS/profile/connection','synthetic-secret');
  assert.equal(await store.read('PAOS/profile/connection'),'synthetic-secret');
  await store.delete('PAOS/profile/connection');
  await assert.rejects(store.write('other/profile/connection','synthetic-secret'),{code:'credential_target_invalid'});
  assert.equal(received.length,3);
});

