import assert from 'node:assert/strict';
import { test } from 'node:test';
import { inspectRuntimeSchema, inspectStdioObservation } from '../../packages/contracts/runtime/compatibility.ts';

test('requires dynamic tools as an actual server request and thread parameter', () => {
  const protocol = {
    definitions: {
      ServerNotification: {
        oneOf: [{ properties: { method: { enum: ['item/tool/call'] } } }],
      },
    },
  };
  const protocolV2 = { definitions: { ThreadStartParams: { description: 'Supports dynamicTools' } } };

  const missing = inspectRuntimeSchema(protocol, protocolV2);
  assert.ok(missing.includes('ServerRequest:item/tool/call'));
  assert.ok(missing.includes('ThreadStartParams.dynamicTools'));
});

test('blocks qualification when a successful stdio process lacks positive history or downgrades execution', () => {
  const observation = {
    processStarted: true, processExit: 0, turnNotifications: 0,
    handshake: { isolatedHome: true, error: null },
    effectiveConfig: { offlineFixtureProvider: true, userLayerTemporary: true, projectLayers: 0,
      userLayerCredentialMode: ['ephemeral'], error: null },
    account: { empty: true, error: null },
    authFileCreated: false,
    alpha: { started: true, cwdMatches: true, error: null, injectError: null,
      policy: { type: 'readOnly', approval: 'never', network: false } },
    beta: { started: true, cwdMatches: true, error: null, injectError: null,
      policy: { type: 'readOnly', approval: 'on-request', network: false } },
    list: {
      alpha: { count: 0, matchesExpected: false, cwdMatches: true, error: null },
      beta: { count: 0, matchesExpected: false, cwdMatches: true, error: null },
      empty: { count: 0, matchesExpected: true, cwdMatches: true, error: null },
      all: { count: 0, matchesExpected: false, cwdMatches: true, error: null },
    },
    threadReadById: true,
  };

  assert.deepEqual(inspectStdioObservation(observation), ['project_history', 'scoped_execution_policy']);
});

test('accepts positive persisted history controls without treating a named profile as Windows readiness', () => {
  const matchingPage = (count: number) => ({ count, matchesExpected: true, cwdMatches: true, error: null });
  const diagnostic = {
    processStarted: true, processExit: 0, turnNotifications: 0,
    handshake: { isolatedHome: true, error: null },
    effectiveConfig: { offlineFixtureProvider: true, userLayerTemporary: true, projectLayers: 0,
      userLayerCredentialMode: ['ephemeral'], error: null },
    account: { empty: true, error: null }, authFileCreated: false,
    persistedList: { alpha: matchingPage(1), beta: matchingPage(1), empty: matchingPage(0), all: matchingPage(2) },
    persistedRead: { idMatches: true, cwdMatches: true, persistedFilePresent: true, pathInTemporaryProfile: true,
      previewPresent: true, error: null },
    fresh: { alpha: { policy: { type: 'readOnly', approval: 'never', network: false } } },
    namedPolicy: { started: true, error: null, policy: {
      type: 'workspaceWrite', activeProfile: 'paos_fixture_write', approval: 'on-request', network: false,
      runtimeWorkspaceRootMatches: true, writableRoots: 0, excludeSlashTmp: true, excludeTmpdirEnvVar: true,
    } },
    windows: { readiness: 'notConfigured' },
  };
  assert.deepEqual(inspectStdioObservation(diagnostic), ['scoped_execution_policy']);
});
