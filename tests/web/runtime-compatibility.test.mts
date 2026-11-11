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

test('requires the concrete RPC shapes used by sandbox qualification and lifecycle mapping', () => {
  const missing = inspectRuntimeSchema({ definitions: {} }, { definitions: {} });
  for (const check of ['ClientRequest:windowsSandbox/readiness', 'ClientRequest:command/exec',
    'CommandExecParams.permissionProfile', 'CommandExecResponse.exitCode', 'ThreadStartResponse.runtimeWorkspaceRoots',
    'WindowsSandboxReadinessResponse.status', 'TurnStatus:interrupted', 'ItemCompletedNotification.item']) {
    assert.ok(missing.includes(check), check);
  }
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

test('requires observed Windows write and denial even when readiness and the named profile match', () => {
  const matchingPage = (count: number) => ({ count, matchesExpected: true, cwdMatches: true, error: null });
  const binarySha256 = 'a'.repeat(64);
  const diagnostic = {
    binarySha256,
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

  const ready = { ...diagnostic, windows: { readiness: 'ready' } };
  assert.deepEqual(inspectStdioObservation(ready), ['scoped_execution_policy']);

  const boundary = {
    binarySha256, mode: 'mxc', readiness: 'ready', readinessError: null,
    outerBaselineBothWritable: true, isolatedHome: true, processExit: 0, turnNotifications: 0,
    authFileCreated: false, tempProfileCleaned: true,
    nativeBreadcrumbs: ['MXC availability: true', 'Windows sandbox selection: mxc'],
    policy: { type: 'workspaceWrite', network: false, approval: 'on-request', writableRoots: 0,
      excludeSlashTmp: true, excludeTmpdirEnvVar: true, profileMatches: true, rootMatches: true },
    profileError: null,
    writeTest: { rpcError: null, childExit: 0, childInside: 'written', childOutside: 'denied',
      insideMatchesChild: true, outsideUnchanged: true },
  };
  assert.deepEqual(inspectStdioObservation(ready, boundary), []);
  assert.deepEqual(inspectStdioObservation(diagnostic, boundary), []);
  assert.deepEqual(inspectStdioObservation(ready, { ...boundary, binarySha256: 'b'.repeat(64) }), ['scoped_execution_policy']);
  assert.deepEqual(inspectStdioObservation(ready, { ...boundary, outerBaselineBothWritable: false }), ['scoped_execution_policy']);
  assert.deepEqual(inspectStdioObservation(ready, {
    ...boundary, nativeBreadcrumbs: ['MXC availability: false', 'Windows sandbox selection: mxc'],
  }), ['scoped_execution_policy']);
  assert.deepEqual(inspectStdioObservation(ready, {
    ...boundary, writeTest: { ...boundary.writeTest, rpcError: -32603, childExit: null, childOutside: null },
  }), ['scoped_execution_policy']);
});
