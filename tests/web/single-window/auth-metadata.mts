import { randomUUID, createHash } from 'node:crypto';
import { spawn } from 'node:child_process';
import { mkdir, mkdtemp, writeFile, readFile, readdir, lstat, rm } from 'node:fs/promises';
import { dirname, join, resolve, win32 } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createConnectionBroker } from '../../../apps/local-service/src/connections/broker.ts';
import { createStdioRpc, type RuntimeRpc } from '../../../apps/local-service/src/runtime/codex/stdio-rpc.ts';
import { nativeProfileConfiguration } from '../../../apps/local-service/src/runtime/native-rpc.mts';
import { inspectConfiguredRuntime } from '../../../packages/contracts/runtime/manifest.mts';

const object = (value: unknown): Record<string, any> => value && typeof value === 'object' && !Array.isArray(value) ? value as Record<string, any> : {};
const fail = (code: string): never => { throw Object.assign(new Error('Offline authentication qualification failed.'), { code }); };
const endpoint = 'http://127.0.0.1:1/v1';
const methods = new Set(['initialize', 'config/read', 'account/login/start', 'account/read', 'account/logout']);
export function metadataMethodAllowed(method: string): boolean { return methods.has(method); }

/** Reject inherited contexts and provider discovery before admitting even a synthetic credential. */
export function assertOfflineAuthReadback(value: unknown): void {
  const response = object(value), config = object(response.config), features = object(config.features);
  const provider = object(object(config.model_providers).paos_offline_auth);
  const layers = Array.isArray(response.layers) ? response.layers.map(object) : [];
  if (config.model_provider !== 'paos_offline_auth' || config.cli_auth_credentials_store !== 'ephemeral'
    || config.forced_login_method !== 'api' || config.web_search !== 'disabled'
    || config.check_for_update_on_startup !== false || object(config.analytics).enabled !== false
    || Object.keys(object(config.mcp_servers)).length || features.api_key_model_discovery !== false
    || features.apps !== false || features.plugins !== false || features.computer_use !== false
    || provider.base_url !== endpoint || provider.requires_openai_auth !== true || provider.model_catalog_url != null
    || layers.some(layer => object(layer.name).type === 'project')
    || layers.filter(layer => object(layer.name).type === 'user').length !== 1) fail('OFFLINE_AUTH_CONFIG_REQUIRED');
}

export const offlineAuthConfiguration = nativeProfileConfiguration
  .replace('model_provider = "openai"', 'model_provider = "paos_offline_auth"')
  .replace('[features]', '[features]\napi_key_model_discovery = false')
  + `\n[model_providers.paos_offline_auth]\nname = "PAOS offline auth qualification"\nbase_url = "${endpoint}"\nwire_api = "responses"\nrequires_openai_auth = true\n`;

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (process.argv.length !== 5 || process.argv[2] !== '--synthetic-auth' || process.argv[3] !== '--binary') fail('EXPLICIT_SYNTHETIC_MODE_REQUIRED');
  const scratch = fileURLToPath(new URL('../../../.tmp/paos-m1/', import.meta.url));
  await mkdir(scratch, { recursive: true });
  const profile = await mkdtemp(join(scratch, 'auth-metadata-'));
  const canary = `PAOS_SYNTHETIC_AUTH_${randomUUID()}`;
  const result: Record<string, any> = { status: 'running', syntheticOnly: true, startedAt: new Date().toISOString(),
    browserUsed: false, realKeysUsed: false, osStoreUsed: false, inferenceRequested: false,
    networkObservation: 'not_instrumented; explicit loopback provider and discovery-off gates required', methods: [],
    turnNotifications: 0, profileCleaned: false };
  let rpc: RuntimeRpc | undefined, child: ReturnType<typeof spawn> | undefined;
  let exit: Promise<void> | undefined;
  try {
    const binaryPath = resolve(process.argv[4]);
    await writeFile(join(profile, 'runtime-selection.json'), JSON.stringify({ binaryPath, providerAuthority: false }));
    if (!(await inspectConfiguredRuntime(profile)).qualified) fail('RUNTIME_UNQUALIFIED');
    const home = join(profile, 'codex');
    for (const directory of [home, join(home, 'user'), join(home, 'user', 'AppData'), join(home, 'user', 'AppData', 'Roaming'),
      join(home, 'user', 'AppData', 'Local'), join(home, 'temp')]) await mkdir(directory);
    await writeFile(join(home, 'config.toml'), offlineAuthConfiguration);
    const systemRoot = process.env.SystemRoot;
    if (!systemRoot || !win32.isAbsolute(systemRoot)) fail('WINDOWS_REQUIRED');
    const system32 = join(systemRoot, 'System32'), user = join(home, 'user');
    child = spawn(binaryPath, ['app-server', '--listen', 'stdio://'], { cwd: home, windowsHide: true, shell: false,
      env: { SystemRoot: systemRoot, WINDIR: systemRoot, ComSpec: join(system32, 'cmd.exe'), PATH: system32,
        CODEX_HOME: home, USERPROFILE: user, HOME: user, APPDATA: join(user, 'AppData', 'Roaming'),
        LOCALAPPDATA: join(user, 'AppData', 'Local'), TEMP: join(home, 'temp'), TMP: join(home, 'temp') },
      stdio: ['pipe', 'pipe', 'pipe'] });
    exit = new Promise<void>(accept => { child!.once('exit', () => accept()); child!.once('error', () => accept()); });
    rpc = createStdioRpc(child as Parameters<typeof createStdioRpc>[0]);
    rpc.subscribe(message => { if (String(message.method).startsWith('turn/')) result.turnNotifications++; });
    const call = async (method: string, params: unknown) => {
      if (!metadataMethodAllowed(method)) fail('OFFLINE_METADATA_METHOD_DENIED');
      result.methods.push(method);
      return rpc!.request(method, params);
    };
    const initialized = await call('initialize', { clientInfo: { name: 'paos-offline-auth-qualification', version: '1' }, capabilities: { experimentalApi: true } });
    if (resolve(String(initialized.codexHome)) !== resolve(home)) fail('ISOLATED_HOME_REQUIRED');
    rpc.notify('initialized');
    const readback = await call('config/read', { cwd: home, includeLayers: true });
    assertOfflineAuthReadback(readback); result.configGatesVerified = true;
    const userLayer = (readback.layers as any[]).find(layer => object(layer.name).type === 'user');
    if (resolve(String(userLayer?.name?.file)) !== resolve(home, 'config.toml')) fail('ISOLATED_HOME_REQUIRED');
    const before = await call('account/read', { refreshToken: false });
    result.initialAccountEmpty = before.account === null;
    if (!result.initialAccountEmpty) fail('INHERITED_ACCOUNT_FORBIDDEN');
    const broker = createConnectionBroker({ profileId: 'synthetic-offline-auth', request: call });
    const connected = await broker.connect({ connectionId: 'synthetic', apiKey: canary, remember: false });
    const account = await call('account/read', { refreshToken: false });
    result.typedApiKeyAccount = object(account.account).type === 'apiKey';
    result.providerRequiresAuth = account.requiresOpenaiAuth === true;
    result.brokerConnected = connected.state === 'connected'; result.modelAccessUnverified = connected.modelAccess === 'unverified';
    result.authorizedBeforeDisconnect = broker.authorize(broker.accountScopeId()!);
    result.publicSnapshotContainsCanary = JSON.stringify(broker.snapshot()).includes(canary);
    const previousScope = broker.accountScopeId()!;
    await broker.disconnect();
    result.authorizationRevoked = !broker.authorize(previousScope);
    result.disconnected = broker.snapshot().state === 'disconnected';
    result.accountEmptyAfterLogout = (await call('account/read', { refreshToken: false })).account === null;
  } catch (error) {
    const allowed = new Set(['RUNTIME_UNQUALIFIED', 'OFFLINE_AUTH_CONFIG_REQUIRED', 'WINDOWS_REQUIRED', 'ISOLATED_HOME_REQUIRED',
      'INHERITED_ACCOUNT_FORBIDDEN', 'OFFLINE_METADATA_METHOD_DENIED', 'rpc_rejected', 'runtime_timeout', 'connection_failed']);
    const code = (error as { code?: string }).code;
    result.errorCode = code && allowed.has(code) ? code : 'NATIVE_AUTH_QUALIFICATION_FAILED';
  } finally {
    if (child) {
      child.stdin?.end();
      let timer: ReturnType<typeof setTimeout> | undefined;
      try { await Promise.race([exit, new Promise<void>(accept => { timer = setTimeout(accept, 5000); })]); }
      finally { if (timer) clearTimeout(timer); }
      if (child.exitCode === null && child.signalCode === null) await rpc?.close();
      result.processClosed = child.exitCode !== null || child.signalCode !== null;
      result.processExit = child.exitCode;
    }
    let files = 0, bytes = 0, matches = 0, complete = true;
    async function scan(directory: string) {
      for (const item of await readdir(directory, { withFileTypes: true })) {
        const path = join(directory, item.name);
        if (++files > 1000 || item.isSymbolicLink()) { complete = false; continue; }
        if (item.isDirectory()) await scan(path);
        else {
          try {
            const info = await lstat(path);
            if (info.size > 8 * 1024 * 1024 || bytes + info.size > 32 * 1024 * 1024) { complete = false; continue; }
            bytes += info.size; if ((await readFile(path)).includes(Buffer.from(canary))) matches++;
          } catch { complete = false; }
        }
      }
    }
    if (!child || result.processClosed) {
      await scan(profile);
      result.canaryFileMatches = matches; result.profileScanComplete = complete;
      try { await lstat(join(profile, 'codex', 'auth.json')); result.authFileCreated = true; }
      catch { result.authFileCreated = false; }
      if (dirname(resolve(profile)) !== resolve(scratch)) fail('PROFILE_SCOPE_REQUIRED');
      await rm(profile, { recursive: true, force: true }); result.profileCleaned = true;
    }
    const required = ['configGatesVerified', 'initialAccountEmpty', 'typedApiKeyAccount', 'providerRequiresAuth',
      'brokerConnected', 'modelAccessUnverified', 'authorizedBeforeDisconnect', 'authorizationRevoked', 'disconnected',
      'accountEmptyAfterLogout', 'profileScanComplete', 'profileCleaned', 'processClosed'];
    result.status = !result.errorCode && required.every(key => result[key] === true) && result.processExit === 0
      && result.turnNotifications === 0 && result.publicSnapshotContainsCanary === false && result.canaryFileMatches === 0
      && result.authFileCreated === false ? 'passed_native_local_auth' : 'failed';
    result.sourceDigests = {};
    for (const path of ['apps/local-service/src/connections/broker.ts', 'apps/local-service/src/runtime/codex/stdio-rpc.ts',
      'tests/web/single-window/auth-metadata.mts']) result.sourceDigests[path] = createHash('sha256').update(await readFile(new URL(`../../../${path}`, import.meta.url))).digest('hex');
    result.finishedAt = new Date().toISOString();
    await writeFile(join(scratch, 'native-auth-metadata-result-2026-11-11.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result));
    if (result.status !== 'passed_native_local_auth') process.exitCode = 1;
  }
}
