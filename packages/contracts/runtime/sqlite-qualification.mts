import { copyFile, mkdtemp, readdir, rmdir, stat, unlink } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { DatabaseSync } from 'node:sqlite';

const SQLITE_CONSTRAINT_FOREIGNKEY = 787;

/** Uses a private temporary directory under an existing writable fixture root. */
export async function verifySqliteQualification(fixtureOutputRoot: string) {
  if (!fixtureOutputRoot) throw new Error('SQLite qualification requires a writable fixture output root');

  const directory = await mkdtemp(join(resolve(fixtureOutputRoot), 'sqlite-'));
  const sourcePath = join(directory, 'source.sqlite');
  const backupPath = join(directory, 'backup.sqlite');
  const restoredPath = join(directory, 'restored.sqlite');
  try {
    let backedUpFromWal: boolean;
    let rejectedOrphan = false;
    const options = { enableForeignKeyConstraints: true };
    {
      using source = new DatabaseSync(sourcePath, options);
      const walEnabled = source.prepare('PRAGMA journal_mode = WAL').get()?.journal_mode === 'wal';
      source.exec(`
        PRAGMA wal_autocheckpoint = 0;
        PRAGMA synchronous = FULL;
        CREATE TABLE parent (id INTEGER PRIMARY KEY);
        CREATE TABLE child (parent_id INTEGER NOT NULL REFERENCES parent(id));
        BEGIN;
        INSERT INTO parent VALUES (1);
        INSERT INTO child VALUES (1);
        COMMIT;
        BEGIN;
        INSERT INTO parent VALUES (2);
        ROLLBACK;
      `);
      try {
        source.exec('INSERT INTO child VALUES (2)');
      } catch (error) {
        if (!(error instanceof Error) || !('errcode' in error) || error.errcode !== SQLITE_CONSTRAINT_FOREIGNKEY) {
          throw error;
        }
        rejectedOrphan = source.prepare('PRAGMA foreign_keys').get()?.foreign_keys === 1;
      }

      const populatedWal = walEnabled && (await stat(`${sourcePath}-wal`)).size > 0;
      // With synchronous=FULL, VACUUM INTO syncs the consistent snapshot before returning.
      source.prepare('VACUUM INTO ?').run(backupPath);
      backedUpFromWal = populatedWal && (await stat(backupPath)).size > 0;
      source.exec('INSERT INTO parent VALUES (3)');
    }
    using reopened = new DatabaseSync(sourcePath, { ...options, readOnly: true });
    const ids = reopened.prepare('SELECT id FROM parent ORDER BY id').all();
    const rollbackVerified = ids.length === 2 && ids[0]?.id === 1 && ids[1]?.id === 3;

    await copyFile(backupPath, restoredPath);
    using restored = new DatabaseSync(restoredPath, { ...options, readOnly: true });
    const restoredIds = restored.prepare('SELECT id FROM parent').all();
    const backupRestoreVerified = backedUpFromWal && restoredIds.length === 1 && restoredIds[0]?.id === 1
      && restored.prepare('PRAGMA integrity_check').get()?.integrity_check === 'ok';
    const restoredChildren = restored.prepare('SELECT parent_id FROM child').all();
    const foreignKeysEnforced = rejectedOrphan
      && restored.prepare('PRAGMA foreign_keys').get()?.foreign_keys === 1
      && restored.prepare('PRAGMA foreign_key_check').all().length === 0
      && restoredChildren.length === 1 && restoredChildren[0]?.parent_id === 1;
    return { rollbackVerified, backupRestoreVerified, foreignKeysEnforced };
  } finally {
    for (const name of await readdir(directory)) await unlink(join(directory, name));
    await rmdir(directory);
  }
}
