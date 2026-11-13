import assert from 'node:assert/strict';
import { test } from 'node:test';
import { launch } from '../../apps/launcher/launcher.ts';
import { createServiceSupervisor } from '../../apps/local-service/src/supervisor/lifecycle.ts';

const expected = { serviceBuild: 'test-build', runtime: { version: '0.167.0', sha256: 'a'.repeat(64) } };

test('an old running service needs an explicit restart and is never stopped by the new launcher',async()=>{
 let opened=false;
 const result=await launch({inspectRuntime:async()=>null,claimInstance:async()=>({kind:'existing',service:{instanceId:'old',port:41821,
  health:async()=>({instanceId:'old',build:'test-build',alive:true,sourceReaderReady:true,runtimeCapable:false})}}),
  openUi:async()=>{opened=true;}},{...expected,browserLaunchVersion:1});
 assert.equal(result.status,'service_restart_required');assert.equal(opened,false);
});

test('opens the loopback UI in local mode when the runtime is missing', async () => {
  const opened: string[] = [];
  const modes: string[] = [];
  const result = await launch({
    async inspectRuntime() { return null; },
    async claimInstance() {
      return {
        kind: 'owner' as const,
        async start(mode: string) {
          modes.push(mode);
          return {
            instanceId: 'synthetic-instance', port: 41821,
            async health() {
              return { instanceId: 'synthetic-instance', build: 'test-build', alive: true,
                sourceReaderReady: true, runtimeCapable: false };
            },
            async quit() { return { status: 'stopped' as const }; },
          };
        },
        async release() {},
      };
    },
    async openUi(origin: string) { opened.push(origin); },
  }, expected);

  assert.deepEqual(result, { status: 'opened', origin: 'http://127.0.0.1:41821', instance: 'started',
    runtime: 'runtime_missing', sourceReaderReady: true });
  assert.deepEqual(modes, ['runtime_missing']);
  assert.deepEqual(opened, ['http://127.0.0.1:41821']);
});

test('Quit waits for a recovery receipt before shutdown and joins duplicate stop requests', async () => {
  const effects: string[] = [];
  const supervisor = createServiceSupervisor({
    async interruptAndDrain() { effects.push('drain'); return 'unknown' as const; },
    async recordRecovery() { effects.push('record recovery'); },
    async stopChildren() { effects.push('stop children'); },
  });

  const outcomes = await Promise.all([supervisor.quit(), supervisor.quit()]);
  assert.deepEqual(outcomes, [{ status: 'stopped_recovery_required' }, { status: 'stopped_recovery_required' }]);
  assert.deepEqual(effects, ['drain', 'record recovery', 'stop children']);
});

test('a repeat launch reuses the current service and exposes an incompatible runtime without switching it', async () => {
  const ui: unknown[] = [];
  const result = await launch({
    async inspectRuntime() { return { version: '0.167.0', sha256: 'b'.repeat(64) }; },
    async claimInstance() {
      return { kind: 'existing' as const, service: {
        port: 41821, instanceId: 'first-launch',
        async health() {
          return { instanceId: 'first-launch', build: 'test-build', alive: true,
            sourceReaderReady: true, runtimeCapable: true };
        },
        async quit(): Promise<never> { assert.fail('second launcher does not own the service'); },
      } };
    },
    async openUi(origin, state) { ui.push({ origin, runtime: state.runtime }); },
  }, expected);

  assert.deepEqual(result, { status: 'opened', origin: 'http://127.0.0.1:41821', instance: 'existing',
    runtime: 'runtime_incompatible', sourceReaderReady: true });
  assert.deepEqual(ui, [{ origin: 'http://127.0.0.1:41821', runtime: 'runtime_incompatible' }]);
});

test('invalid service health closes the owned process before releasing its instance reservation', async () => {
  const effects: string[] = [];
  const result = await launch({
    async inspectRuntime() { return null; },
    async claimInstance() {
      return { kind: 'owner' as const,
        async start() {
          return { port: 41821, instanceId: 'owned-instance',
            async health() {
              return { instanceId: 'different-instance', build: 'test-build', alive: true,
                sourceReaderReady: true, runtimeCapable: false };
            },
            async quit() { effects.push('quit'); return { status: 'stopped' as const }; },
          };
        },
        async release() { effects.push('release'); },
      };
    },
    async openUi() { effects.push('open'); },
  }, expected);

  assert.deepEqual(result, { status: 'service_unhealthy' });
  assert.deepEqual(effects, ['quit', 'release']);
});

test('a timed-out start preserves the instance reservation until the child outcome is known', async () => {
  const effects: string[] = [];
  const result = await launch({
    async inspectRuntime() { return null; },
    async claimInstance() {
      return { kind: 'owner' as const,
        async start(_runtime, signal): Promise<never> {
          return new Promise(() => signal.addEventListener('abort', () => effects.push('abort'), { once: true }));
        },
        async release() { effects.push('release'); },
      };
    },
    async openUi() { effects.push('open'); },
  }, expected, 5);

  assert.deepEqual(result, { status: 'service_start_failed', cleanupPending: true });
  assert.deepEqual(effects, ['abort']);
});

test('leaving the service running has no stop effects and a failed receipt keeps children available for retry', async () => {
  const effects: string[] = [];
  let allowReceipt = false;
  const supervisor = createServiceSupervisor({
    async interruptAndDrain() { effects.push('drain'); return 'unknown'; },
    async recordRecovery() {
      effects.push('receipt');
      if (!allowReceipt) throw new Error('test journal unavailable');
    },
    async stopChildren() { effects.push('stop children'); },
  });

  assert.deepEqual(await supervisor.quit('keep_running'), { status: 'kept_running' });
  assert.deepEqual(effects, []);
  assert.deepEqual(await supervisor.quit(), { status: 'stop_blocked', phase: 'record_recovery' });
  assert.deepEqual(effects, ['drain', 'receipt']);
  allowReceipt = true;
  assert.deepEqual(await supervisor.quit(), { status: 'stopped_recovery_required' });
  assert.deepEqual(effects, ['drain', 'receipt', 'receipt', 'stop children']);
});
