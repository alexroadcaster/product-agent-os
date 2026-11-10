const requiredMethods = {
  ClientRequest: [
    'initialize', 'thread/start', 'thread/list', 'thread/read', 'thread/resume',
    'turn/start', 'turn/interrupt', 'account/read', 'account/login/start', 'account/logout',
  ],
  ClientNotification: ['initialized'],
  ServerRequest: [
    'item/commandExecution/requestApproval', 'item/fileChange/requestApproval',
    'item/permissions/requestApproval', 'item/tool/requestUserInput', 'item/tool/call',
  ],
  ServerNotification: [
    'error', 'turn/started', 'turn/completed', 'item/started', 'item/completed',
    'item/agentMessage/delta', 'serverRequest/resolved', 'account/updated',
  ],
} as const;

const requiredFields = {
  InitializeCapabilities: ['experimentalApi'],
  ThreadStartParams: ['cwd', 'dynamicTools'],
  ThreadListParams: ['cwd', 'cursor', 'archived'],
  ThreadListResponse: ['data', 'nextCursor'],
  TurnStartParams: ['cwd', 'threadId', 'sandboxPolicy', 'approvalPolicy'],
  TurnInterruptParams: ['threadId', 'turnId'],
  ServerRequestResolvedNotification: ['threadId', 'requestId'],
  TurnCompletedNotification: ['threadId', 'turn'],
} as const;

function object(value: unknown): Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? value as Record<string, unknown>
    : {};
}

function variants(schema: unknown): unknown[] {
  const { oneOf } = object(schema);
  return Array.isArray(oneOf) ? oneOf : [];
}

function hasEnum(schema: unknown, expected: string): boolean {
  const values = object(schema).enum;
  return Array.isArray(values) && values.includes(expected);
}

function properties(schema: unknown): Record<string, unknown> {
  return object(object(schema).properties);
}

/** Check the generated schema at the protocol boundary. Live behavior must be qualified separately. */
export function inspectRuntimeSchema(protocol: unknown, protocolV2: unknown): string[] {
  const envelope = object(object(protocol).definitions);
  const v2 = object(object(protocolV2).definitions);
  const missing: string[] = [];

  for (const [direction, methods] of Object.entries(requiredMethods)) {
    const entries = variants(envelope[direction]);
    for (const method of methods) {
      if (!entries.some((entry) => hasEnum(properties(entry).method, method))) {
        missing.push(`${direction}:${method}`);
      }
    }
  }
  for (const [name, fields] of Object.entries(requiredFields)) {
    const fieldsInSchema = properties(v2[name]);
    for (const field of fields) {
      if (!Object.hasOwn(fieldsInSchema, field)) {
        missing.push(`${name}.${field}`);
      }
    }
  }

  const sandbox = variants(v2.SandboxPolicy).map(properties);
  for (const mode of ['readOnly', 'workspaceWrite']) {
    const policy = sandbox.find((entry) => hasEnum(entry.type, mode));
    if (object(policy?.networkAccess).type !== 'boolean') {
      missing.push(`SandboxPolicy:${mode}.networkAccess`);
    }
    if (mode === 'workspaceWrite' && (
      object(policy?.writableRoots).type !== 'array'
      || object(policy?.excludeSlashTmp).type !== 'boolean'
      || object(policy?.excludeTmpdirEnvVar).type !== 'boolean'
    )) {
      missing.push('SandboxPolicy:workspaceWrite.rootIsolation');
    }
  }
  if (!variants(v2.AskForApproval).some((entry) => hasEnum(entry, 'on-request'))) {
    missing.push('AskForApproval:on-request');
  }
  if (!variants(v2.LoginAccountParams).map(properties).some(
    (entry) => hasEnum(entry.type, 'apiKey') && object(entry.apiKey).type === 'string',
  )) {
    missing.push('LoginAccountParams:apiKey');
  }
  if (object(properties(envelope.JSONRPCError).error).$ref === undefined) {
    missing.push('JSONRPCError.error');
  }

  return missing;
}

/** Evaluate recorded offline scenarios. The receipt cannot prove provider or tool enforcement. */
export function inspectStdioObservation(observation: unknown): string[] {
  const run = object(observation);
  const handshake = object(run.handshake);
  const config = object(run.effectiveConfig);
  const account = object(run.account);
  const alpha = object(run.alpha);
  const beta = object(run.beta);
  const diagnostic = Object.hasOwn(run, 'persistedList');
  const lists = object(diagnostic ? run.persistedList : run.list);
  const persistedRead = object(run.persistedRead);
  const named = object(run.namedPolicy);
  const readPolicy = object(diagnostic ? object(object(run.fresh).alpha).policy : alpha.policy);
  const writePolicy = object(diagnostic ? named.policy : beta.policy);
  const missing: string[] = [];

  if (run.processStarted !== true || run.processExit !== 0 || run.turnNotifications !== 0
    || Object.hasOwn(run, 'probeFailure') || run.forcedShutdown === true
    || handshake.isolatedHome !== true || handshake.error !== null) {
    missing.push('stdio_handshake');
  }
  const credentialModes = config.userLayerCredentialMode;
  if (config.offlineFixtureProvider !== true || config.userLayerTemporary !== true || config.projectLayers !== 0
    || config.error !== null || !Array.isArray(credentialModes) || credentialModes.length !== 1 || credentialModes[0] !== 'ephemeral'
    || account.empty !== true || account.error !== null || run.authFileCreated !== false) {
    missing.push('isolated_profile');
  }

  // An empty foreign-project query proves isolation only after the positive controls see both fixtures.
  const expectedCounts = { alpha: 1, beta: 1, empty: 0, all: 2 };
  const scopedListsMatch = Object.entries(expectedCounts).every(([name, count]) => {
    const page = object(lists[name]);
    return page.error === null && page.count === count && page.matchesExpected === true && page.cwdMatches === true;
  });
  const fixturesAvailable = [alpha, beta].every((fixture) => (
    fixture.started === true && fixture.cwdMatches === true && fixture.injectError === null
  ));
  const historyReadVerified = diagnostic
    ? persistedRead.error === null && persistedRead.idMatches === true && persistedRead.cwdMatches === true
      && persistedRead.pathInTemporaryProfile === true && persistedRead.persistedFilePresent === true
      && persistedRead.previewPresent === true
    : fixturesAvailable && run.threadReadById === true;
  if (!scopedListsMatch || !historyReadVerified) {
    missing.push('project_history');
  }

  // The named policy may use the runtime workspace root without repeating it in legacy writableRoots.
  const writeScopeVerified = diagnostic
    ? object(run.windows).readiness === 'ready' && named.started === true && named.error === null
      && writePolicy.activeProfile === 'paos_fixture_write' && writePolicy.runtimeWorkspaceRootMatches === true
      && (writePolicy.writableRoots === 0 || writePolicy.writableRootMatches === true)
    : writePolicy.writableRootMatches === true;
  if (readPolicy.type !== 'readOnly' || readPolicy.approval !== 'never' || readPolicy.network !== false
    || writePolicy.type !== 'workspaceWrite' || writePolicy.approval !== 'on-request' || writePolicy.network !== false
    || !writeScopeVerified || writePolicy.excludeSlashTmp !== true
    || writePolicy.excludeTmpdirEnvVar !== true) {
    missing.push('scoped_execution_policy');
  }

  return missing;
}
