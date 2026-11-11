import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createSessionGate } from '../../apps/local-service/src/http/session-gate.mts';

const origin = 'http://127.0.0.1:43127';
const request = (method: string, headers: Record<string, string> = {}) => new Request(`${origin}/api/v1/projects`, {
  method, headers: { host: '127.0.0.1:43127', origin, ...headers },
});

test('pairs once and requires an instance-bound cookie and CSRF for mutation', () => {
  const gate = createSessionGate({ origin, instanceId: 'fixture-instance' });
  const code = gate.issuePairingCode();
  const paired = gate.exchange(request('POST', { 'content-type': 'application/json' }), code);
  const cookie = paired.cookie.split(';')[0];
  assert.match(paired.cookie, /HttpOnly; SameSite=Strict; Path=\//);
  assert.throws(() => gate.exchange(request('POST', { 'content-type': 'application/json' }), code), { code: 'PAIRING_INVALID' });
  assert.throws(() => gate.authorize(request('POST', { cookie })), { code: 'CSRF_INVALID' });
  assert.equal(gate.authorize(request('POST', { cookie, 'x-paos-csrf': paired.csrfToken })).actorId, 'local-user');
  assert.throws(() => gate.authorize(request('GET', { cookie, host: 'evil.example' })), { code: 'ORIGIN_REJECTED' });
  assert.throws(() => gate.authorize(request('POST', { cookie, origin: 'https://evil.example', 'x-paos-csrf': paired.csrfToken })),
    { code: 'ORIGIN_REJECTED' });
  gate.revokeAll();
  assert.throws(() => gate.authorize(request('GET', { cookie })), { code: 'SESSION_REQUIRED' });
});

test('expires pairing and sessions and locks the code after five failed attempts', () => {
  let now = 0;
  const gate = createSessionGate({ origin, instanceId: 'fixture-instance', now: () => now });
  const first = gate.issuePairingCode();
  now = 60_001;
  assert.throws(() => gate.exchange(request('POST', { 'content-type': 'application/json' }), first), { code: 'PAIRING_INVALID' });
  const next = gate.issuePairingCode();
  for (let i = 0; i < 5; i++) {
    assert.throws(() => gate.exchange(request('POST', { 'content-type': 'application/json' }), 'wrong'), { code: 'PAIRING_INVALID' });
  }
  assert.throws(() => gate.exchange(request('POST', { 'content-type': 'application/json' }), next), { code: 'PAIRING_INVALID' });
  const paired = gate.exchange(request('POST', { 'content-type': 'application/json' }), gate.issuePairingCode());
  now += 30 * 60_000 + 1;
  assert.throws(() => gate.authorize(request('GET', { cookie: paired.cookie.split(';')[0] })), { code: 'SESSION_REQUIRED' });
});
