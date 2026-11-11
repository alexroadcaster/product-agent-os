import assert from 'node:assert/strict';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { createStdioRpc } from '../../apps/local-service/src/runtime/codex/stdio-rpc.ts';

test('correlates an isolated child response and denies raw shell methods', async (t) => {
  const child = fork(fileURLToPath(new URL('./runtime-adapter.fixture.mts', import.meta.url)), [], {
    execArgv: [], env: { SystemRoot: process.env.SystemRoot }, silent: true,
  });
  const rpc = createStdioRpc(child, { timeoutMs: 1000 });
  t.after(async () => { await rpc.close(); if (child.exitCode === null) child.kill(); });
  assert.deepEqual(await rpc.request('initialize', { clientInfo: { name: 'synthetic', version: '1' } }), {
    userAgent: 'synthetic', codexHome: 'synthetic-profile',
  });
  await assert.rejects(rpc.request('thread/shellCommand', {}), { code: 'method_denied' });
});
