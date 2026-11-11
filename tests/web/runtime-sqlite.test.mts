import assert from 'node:assert/strict';
import { mkdtemp, readdir, rmdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { verifySqliteQualification } from '../../packages/contracts/runtime/sqlite-qualification.mts';

test('the file-backed SQLite fixture preserves the committed rows and discards rolled-back rows', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-sqlite-test-'));
  t.after(() => rmdir(root));

  const evidence = await verifySqliteQualification(root);

  assert.equal(evidence.rollbackVerified, true);
  assert.deepEqual(await readdir(root), []);
});

test('a WAL-backed SQLite snapshot restores independently of later source writes', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-sqlite-test-'));
  t.after(() => rmdir(root));

  assert.equal((await verifySqliteQualification(root)).backupRestoreVerified, true);
});

test('the fixture rejects orphan rows and the restored database passes foreign key checks', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'paos-sqlite-test-'));
  t.after(() => rmdir(root));

  assert.equal((await verifySqliteQualification(root)).foreignKeysEnforced, true);
});
