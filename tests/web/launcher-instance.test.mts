import assert from 'node:assert/strict';
import { fork } from 'node:child_process';
import { once } from 'node:events';
import { mkdir, mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { test, type TestContext } from 'node:test';
import { fileURLToPath } from 'node:url';
import { launch } from '../../apps/launcher/launcher.ts';
import { createProfileInstanceClaimer } from '../../apps/launcher/profile-instance.ts';

async function createProfile(t: TestContext): Promise<string> {
  const scratch = await realpath(tmpdir());
  const path = await mkdtemp(join(scratch, 'paos-launcher-instance-'));
  t.after(async () => {
    assert.equal(dirname(await realpath(path)), scratch);
    await rm(path, { recursive: true, force: true });
  });
  return path;
}

test('an interrupted publication and a torn endpoint are blocked without overwriting the instance files', async (t) => {
  const profile = await createProfile(t);
  const lock = join(profile, 'service-instance');
  await mkdir(lock);
  const tornRecord = '{"instanceId":';
  await writeFile(join(lock, 'endpoint.next'), tornRecord);
  const ports = {
    claimInstance: createProfileInstanceClaimer(profile, {
      async startService(): Promise<never> { assert.fail('An existing reservation must stay in place.'); },
      async readHealth(): Promise<never> { assert.fail('A torn endpoint must not be used.'); },
    }),
    async inspectRuntime() { return null; },
    async openUi() { assert.fail('Unconfirmed service must not open a window.'); },
  };
  const expected = { serviceBuild: 'fixture-build', runtime: null };
  assert.deepEqual(await launch(ports, expected), { status: 'instance_unavailable', instanceReason: 'startup_unresolved' });
  await writeFile(join(lock, 'endpoint.json'), tornRecord);
  assert.deepEqual(await launch(ports, expected), { status: 'instance_unavailable', instanceReason: 'invalid_instance_record' });
  assert.equal(await readFile(join(lock, 'endpoint.next'), 'utf8'), tornRecord);
  assert.equal(await readFile(join(lock, 'endpoint.json'), 'utf8'), tornRecord);
});

test('a thrown start keeps the reservation while a definitive no-child result releases it', async (t) => {
  const expected = { serviceBuild: 'fixture-build', runtime: null };
  const confirmedProfile = await createProfile(t);
  const pendingProfile = await createProfile(t);
  const ports = {
    async inspectRuntime() { return null; },
    async openUi() { assert.fail('A failed start must not open a window.'); },
  };
  const host = {
    async readHealth(): Promise<never> { assert.fail('No service was confirmed.'); },
  };
  const confirmed = createProfileInstanceClaimer(confirmedProfile, {
    ...host, async startService() { return { status: 'not_started' }; },
  });
  const uncertain = createProfileInstanceClaimer(pendingProfile, {
    ...host, async startService() { throw new Error('Child outcome unknown.'); },
  });

  assert.deepEqual(await launch({ ...ports, claimInstance: confirmed }, expected), { status: 'service_start_failed' });
  const signal = new AbortController().signal;
  const retry = await confirmed(signal);
  assert.equal(retry.kind, 'owner');
  if (retry.kind === 'owner') await retry.release(signal);
  assert.deepEqual(await launch({ ...ports, claimInstance: uncertain }, expected), {
    status: 'service_start_failed', cleanupPending: true,
  });
  assert.deepEqual(await launch({ ...ports, claimInstance: uncertain }, expected), {
    status: 'instance_unavailable', instanceReason: 'startup_unresolved',
  });
});

test('a second launcher respects an unpublished claim, reuses the published service, then can reserve after Quit',
  { timeout: 8_000 }, async (t) => {
    const profile = await createProfile(t);
    const fixture = fileURLToPath(new URL('./launcher-instance.fixture.mts', import.meta.url));
    const child = fork(fixture, [profile], { execArgv: [], env: { SystemRoot: process.env.SystemRoot }, silent: true });
    t.after(() => { if (child.exitCode === null) child.kill(); });
    const [reservation] = await once(child, 'message');
    assert.equal(reservation, 'reserved');

    const ports = {
      claimInstance: createProfileInstanceClaimer(profile, {
        async startService(): Promise<never> { assert.fail('Another process holds the only reservation.'); },
        async readHealth({ instanceId }) {
          return { instanceId, build: 'fixture-build', alive: true, sourceReaderReady: true, runtimeCapable: false };
        },
      }),
      async inspectRuntime() { return null; },
      async openUi() {},
    };
    const expected = { serviceBuild: 'fixture-build', runtime: null };
    assert.deepEqual(await launch(ports, expected), { status: 'instance_unavailable', instanceReason: 'startup_unresolved' });

    const published = once(child, 'message');
    child.send('publish');
    assert.equal((await published)[0], 'published');
    assert.deepEqual(await launch(ports, expected), {
      status: 'opened', origin: 'http://127.0.0.1:41821', instance: 'existing',
      runtime: 'runtime_missing', sourceReaderReady: true,
    });

    const released = once(child, 'message');
    const exited = once(child, 'exit');
    child.send('quit');
    assert.equal((await released)[0], 'released');
    assert.equal((await exited)[0], 0);
    const signal = new AbortController().signal;
    const next = await ports.claimInstance(signal);
    assert.equal(next.kind, 'owner');
    if (next.kind === 'owner') await next.release(signal);
  });
