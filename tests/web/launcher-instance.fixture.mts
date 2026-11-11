import { launch, type OwnedLauncherControls } from '../../apps/launcher/launcher.ts';
import { createProfileInstanceClaimer } from '../../apps/launcher/profile-instance.ts';

const profileDirectory = process.argv[2];
let publish: (() => void) | undefined;
const publishing = new Promise<void>((resolve) => { publish = resolve; });
const claimInstance = createProfileInstanceClaimer(profileDirectory, {
  async startService() {
    process.send?.('reserved');
    await publishing;
    return { status: 'started', port: 41821, async quit() { return { status: 'stopped' }; } };
  },
  async readHealth({ instanceId }) {
    return { instanceId, build: 'fixture-build', alive: true, sourceReaderReady: true, runtimeCapable: false };
  },
});

let controls: OwnedLauncherControls | undefined;
process.on('message', async (message) => {
  try {
    if (message === 'publish') publish?.();
    if (message === 'quit') {
      if (!controls || (await controls.quit()).status !== 'stopped') throw new Error('Fixture service did not stop.');
      process.send?.('released', () => process.disconnect());
    }
  } catch {
    process.send?.('fixture_failed', () => process.disconnect());
  }
});

try {
  const result = await launch({ claimInstance, async inspectRuntime() { return null; },
    async openUi(_origin, _state, _signal, owner) { controls = owner; } }, { serviceBuild: 'fixture-build', runtime: null });
  if (result.status !== 'opened' || !controls) throw new Error('Launcher did not retain native Quit.');
  process.send?.('published');
} catch {
  process.send?.('fixture_failed', () => process.disconnect());
}
