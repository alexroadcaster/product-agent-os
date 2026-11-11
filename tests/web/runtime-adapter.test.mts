import assert from 'node:assert/strict';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { createStdioRpc } from '../../apps/local-service/src/runtime/codex/stdio-rpc.ts';
import {EventEmitter} from 'node:events';
import {PassThrough} from 'node:stream';

test('a child without a confirmed exit keeps close unverified and repeated waits release listeners',async()=>{
 const child=Object.assign(new EventEmitter(),{stdin:new PassThrough(),stdout:new PassThrough(),stderr:new PassThrough(),exitCode:null as number|null,signalCode:null,kill:()=>false});
 const rpc=createStdioRpc(child as any);
 const baseExitListeners=child.listenerCount('exit');
 for(let attempt=0;attempt<2;attempt++) {
  await assert.rejects(()=>rpc.close(),{code:'runtime_stop_unverified'});
  assert.equal(child.listenerCount('exit'),baseExitListeners);
 }
 child.exitCode=0;child.emit('exit',0,null);await rpc.close();
});

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
