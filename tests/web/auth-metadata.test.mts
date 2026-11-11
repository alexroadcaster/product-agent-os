import assert from 'node:assert/strict';
import { test } from 'node:test';
import { assertOfflineAuthReadback, metadataMethodAllowed } from './single-window/auth-metadata.mts';
const config = { config: { model_provider: 'paos_offline_auth', cli_auth_credentials_store: 'ephemeral', forced_login_method: 'api',
  check_for_update_on_startup: false, web_search: 'disabled', mcp_servers: {}, analytics: { enabled: false },
  features: { api_key_model_discovery: false, apps: false, plugins: false, computer_use: false },
  model_providers: { paos_offline_auth: { base_url: 'http://127.0.0.1:1/v1', requires_openai_auth: true } } },
  layers: [{ name: { type: 'user', file: 'synthetic-home/config.toml' } }] };

test('auth canary refuses provider endpoints, background discovery and inherited project layers', () => {
  assert.doesNotThrow(() => assertOfflineAuthReadback(config));
  for (const unsafe of [
    { ...config, config: { ...config.config, features: { ...config.config.features, api_key_model_discovery: true } } },
    { ...config, config: { ...config.config, model_provider: 'openai' } },
    { ...config, config: { ...config.config, model_providers: { paos_offline_auth: { base_url: 'https://example.invalid', requires_openai_auth: true } } } },
    { ...config, layers: [...config.layers, { name: { type: 'project', file: 'synthetic-project/config.toml' } }] },
  ]) assert.throws(() => assertOfflineAuthReadback(unsafe), { code: 'OFFLINE_AUTH_CONFIG_REQUIRED' });
});

test('auth canary allows metadata only and rejects thread, turn, tool, model and rate-limit methods', () => {
  for (const method of ['initialize', 'config/read', 'account/login/start', 'account/read', 'account/logout']) assert.equal(metadataMethodAllowed(method), true);
  for (const method of ['thread/start', 'turn/start', 'command/exec', 'model/list', 'account/rateLimits/read']) assert.equal(metadataMethodAllowed(method), false);
});
