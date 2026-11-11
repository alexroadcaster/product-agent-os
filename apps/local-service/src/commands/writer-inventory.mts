import { createHash } from 'node:crypto';
import { lstat, opendir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import type { WriterInventory, WriterRoute } from '../import-export/migration.mts';

/** Unknown installed script surfaces block cutover. Manual file edits remain source-drift conflicts. */
export async function inspectLegacyWriterInventory(workspaceRoot: string): Promise<WriterInventory> {
  const source = await readFile(new URL('./domain-tools.mts', import.meta.url));
  const entries: WriterRoute[] = [{ id: 'paos-domain-service', role: 'writer', route: 'domain_adapter',
    sourceDigest: createHash('sha256').update(source).digest('hex'), verified: true }];
  let complete = true;
  let scanned = 0;
  async function scan(relativePath: string) {
    const path = join(workspaceRoot, relativePath);
    let info;
    try { info = await lstat(path); } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== 'ENOENT') complete = false;
      return;
    }
    if (info.isSymbolicLink()) { complete = false; return; }
    if (!info.isDirectory()) { complete = false; return; }
    const directory = await opendir(path);
    for await (const item of directory) {
      if (++scanned > 256) { complete = false; return; }
      const relative = `${relativePath}/${item.name}`;
      if (item.isSymbolicLink()) { complete = false; continue; }
      if (item.isDirectory()) {
        if (!['node_modules', '.git', '__pycache__', 'dist'].includes(item.name)) await scan(relative);
      } else if (/\.(?:py|ps1|sh|cmd|bat|m?js|[cm]?ts|toml|ya?ml)$/.test(item.name)) {
        // Parsing a filename cannot establish behavioral ownership. Keep this potential writer unsupported.
        entries.push({ id: relative, role: 'writer', route: 'unsupported', sourceDigest: '', verified: false });
        complete = false;
      }
    }
  }
  for (const area of ['.codex', '.agents', 'scripts', 'tools', 'plugins']) await scan(area);
  return { entries, complete };
}
