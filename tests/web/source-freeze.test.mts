import assert from 'node:assert/strict';
import { test } from 'node:test';
import { EventEmitter } from 'node:events';
import { PassThrough } from 'node:stream';
import { nativeSourceFreezeBridge, withFrozenSource } from '../../apps/local-service/src/import-export/source-freeze.mts';

const input = { workspaceRoot: 'C:\\synthetic-workspace', sourceRelativePath: 'plan/tasks.json' };
const sha256 = 'a'.repeat(64);

function injectedLease() {
  const actions: string[] = [];
  let finish!: (exit: { code: number }) => void;
  let exitCode: number | undefined;
  const closed = new Promise<{ code: number }>(resolve => { finish = resolve; });
  const close = (code: number) => { if (exitCode === undefined) { exitCode = code; finish({ code }); } };
  return { actions, close, bridge: async () => ({ sha256, byteSize: 42, closed,
    release: async () => { actions.push('release'); close(0); if ((await closed).code !== 0) throw new Error('closed'); },
    terminate: async () => { actions.push('terminate'); close(1); } }) };
}

test('holds the injected source lease across the operation and returns only after release and clean exit', async () => {
  const actions: string[] = [];
  let finish!: (exit: { code: number }) => void;
  const closed = new Promise<{ code: number }>(resolve => { finish = resolve; });
  const bridge = async () => ({ sha256, byteSize: 42, closed,
    release: async () => { actions.push('release'); finish({ code: 0 }); },
    terminate: async () => { actions.push('terminate'); finish({ code: 1 }); } });
  const result = await withFrozenSource(input, async source => {
    source.assertHeld();
    assert.equal(source.sha256, sha256);
    assert.equal(source.byteSize, 42);
    assert.equal(source.signal.aborted, false);
    actions.push('promotion');
    return 'receipt';
  }, { bridge });
  assert.equal(result, 'receipt');
  assert.deepEqual(actions, ['promotion', 'release']);
});

test('invalid relative paths never reach the native bridge', async () => {
  let calls = 0;
  const fixture = injectedLease();
  const bridge = async () => { calls++; return fixture.bridge(); };
  for (const sourceRelativePath of ['../tasks.json', '/tasks.json', 'C:\\tasks.json', 'plan//tasks.json', 'tasks.json:stream', 'plan/./tasks.json', 'NUL.json', 'tasks.json ']) {
    await assert.rejects(withFrozenSource({ ...input, sourceRelativePath }, async () => true, { bridge }), { code: 'SOURCE_PATH_INVALID' });
  }
  assert.equal(calls, 0);
});

test('callback failure releases the handle and preserves the failure', async () => {
  const fixture = injectedLease();
  await assert.rejects(withFrozenSource(input, async () => { throw Object.assign(new Error('Synthetic callback failed'), { code: 'PROMOTION_FAILED' }); }, fixture), { code: 'PROMOTION_FAILED' });
  assert.deepEqual(fixture.actions, ['release']);
});

test('early helper exit invalidates a delayed callback before promotion and cleans the child', async () => {
  const fixture = injectedLease();
  let resume!: () => void;
  let entered!: () => void;
  const entry = new Promise<void>(resolve => { entered = resolve; });
  const gate = new Promise<void>(resolve => { resume = resolve; });
  let promoted = false;
  const result = withFrozenSource(input, async source => { entered(); await gate; source.assertHeld(); promoted = true; }, fixture);
  await entry;
  fixture.close(1);
  await assert.rejects(result, { code: 'SOURCE_FREEZE_LOST' });
  resume();
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(promoted, false);
  assert.deepEqual(fixture.actions, ['release', 'terminate']);
});

test('timeout aborts the callback lease and rejects oversized observations without invoking the operation', async () => {
  const fixture = injectedLease();
  let sourceSignal: AbortSignal | undefined;
  await assert.rejects(withFrozenSource(input, async source => { sourceSignal = source.signal; await new Promise(() => {}); },
    { bridge: fixture.bridge, timeoutMs: 20 }), { code: 'SOURCE_FREEZE_TIMEOUT' });
  assert.equal(sourceSignal?.aborted, true);
  assert.deepEqual(fixture.actions, ['release']);
  let called = false;
  const oversized = injectedLease();
  await assert.rejects(withFrozenSource(input, async () => { called = true; }, { bridge: async () => ({ ...await oversized.bridge(), byteSize: 1048577 }) }), { code: 'SOURCE_FREEZE_PROTOCOL_INVALID' });
  assert.equal(called, false);
  assert.deepEqual(oversized.actions, ['release']);
});

test('the native protocol is lazy, sends only bound paths and waits for clean close after release', async () => {
  const stdin = new PassThrough();
  const stdout = new PassThrough();
  const child = new EventEmitter() as any;
  child.stdin = stdin; child.stdout = stdout;
  let closed = false;
  child.kill = () => { if (!closed) { closed = true; queueMicrotask(() => child.emit('close', 1)); } return true; };
  const lines: string[] = [];
  stdin.on('data', chunk => {
    lines.push(String(chunk).trim());
    if (String(chunk).trim() === 'release') { closed = true; queueMicrotask(() => child.emit('close', 0)); }
  });
  const lease = await nativeSourceFreezeBridge({ workspaceRoot: input.workspaceRoot, sourcePath: 'C:\\synthetic-workspace\\plan\\tasks.json' }, new AbortController().signal,
    { launch: (_executable, arguments_, options) => {
      assert.equal(arguments_.includes('-ExecutionPolicy'), false);
      assert.equal(options?.shell, false);
      queueMicrotask(() => stdout.write(JSON.stringify({ sha256, byteSize: 42 }) + '\n'));
      return child;
    } });
  assert.equal(lease.sha256, sha256);
  assert.deepEqual(Object.keys(JSON.parse(lines[0]!)).sort(), ['sourcePath', 'workspaceRoot']);
  await lease.release();
  assert.equal(closed, true);
  assert.equal(lines[1], 'release');
});
