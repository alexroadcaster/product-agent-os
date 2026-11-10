import assert from 'node:assert/strict';
import { mkdtemp, mkdir, rename, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { bindProject, inspectProjectSources } from '../../apps/local-service/src/adapters/project-sources.ts';

test('reports source coverage for the registered project without exposing other roots', async (t) => {
  const temp = await mkdtemp(join(tmpdir(), 'paos-project-sources-'));
  t.after(() => rm(temp, { recursive: true, force: true }));
  const workspace = join(temp, 'workspace');
  const otherProject = join(temp, 'other-project');
  await mkdir(workspace);
  await mkdir(otherProject);
  await writeFile(join(workspace, 'AGENTS.md'), '# Project instructions');
  await writeFile(join(otherProject, 'PLAN.md'), '# Different project');
  await symlink(otherProject, join(workspace, 'RUNLOG.md'), 'junction');

  const binding = await bindProject('workspace-id', workspace);
  const result = await inspectProjectSources(binding, 'workspace-id');
  assert.equal(result.projectId, 'workspace-id');
  const byId = new Map(result.sources.map((source) => [source.id, source]));
  assert.deepEqual(byId.get('instructions'), {
    id: 'instructions', relativePath: 'AGENTS.md', status: 'available',
  });
  assert.deepEqual(byId.get('plan'), {
    id: 'plan', relativePath: 'PLAN.md', status: 'unavailable', reason: 'missing',
  });
  assert.deepEqual(byId.get('runlog'), {
    id: 'runlog', relativePath: 'RUNLOG.md', status: 'excluded', reason: 'linked_file',
  });
  assert.deepEqual(byId.get('runtimeHistory'), {
    id: 'runtimeHistory', status: 'unavailable', reason: 'runtime_not_connected',
  });
  assert.equal(JSON.stringify(result).includes(temp), false);
  await assert.rejects(inspectProjectSources(binding, 'other-project-id'), { code: 'PROJECT_NOT_FOUND' });
});

test('rejects a registered root replaced by a different directory at the same path', async (t) => {
  const temp = await mkdtemp(join(tmpdir(), 'paos-project-rebind-'));
  t.after(() => rm(temp, { recursive: true, force: true }));
  const workspace = join(temp, 'workspace');
  await mkdir(workspace);
  const binding = await bindProject('workspace-id', workspace);
  await rename(workspace, join(temp, 'old-workspace'));
  await mkdir(workspace);
  await writeFile(join(workspace, 'AGENTS.md'), '# Replacement directory');

  await assert.rejects(inspectProjectSources(binding, 'workspace-id'), { code: 'PROJECT_ROOT_UNAVAILABLE' });
});

test('scopes runtime history requests and excludes unexpected rows from other roots', async (t) => {
  const temp = await mkdtemp(join(tmpdir(), 'paos-runtime-history-'));
  t.after(() => rm(temp, { recursive: true, force: true }));
  const binding = await bindProject('workspace-id', temp);

  const result = await inspectProjectSources(binding, 'workspace-id', async (request) => {
    assert.equal(request.cwd, binding.workspaceRoot);
    assert.equal(request.limit, 50);
    assert.deepEqual(request.sourceKinds, ['cli', 'vscode', 'appServer']);
    assert.deepEqual(request.modelProviders, []);
    return { data: [
      { id: 'own-session', cwd: binding.workspaceRoot },
      { id: 'other-session', cwd: join(binding.workspaceRoot, 'other-project') },
    ], nextCursor: null };
  });

  assert.deepEqual(result.sources.find((source) => source.id === 'runtimeHistory'), {
    id: 'runtimeHistory', status: 'partial', reason: 'runtime_scope_mismatch',
    visibleThreadCount: 1, hasMore: false,
  });
  assert.equal(JSON.stringify(result).includes(temp), false);
});
