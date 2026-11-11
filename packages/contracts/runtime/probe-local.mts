import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { release } from 'node:os';
import { join } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { parseArgs } from 'node:util';
import { inspectRuntimeSchema, inspectStdioObservation } from './compatibility.ts';
import { verifySqliteQualification } from './sqlite-qualification.mts';

const { positionals, values } = parseArgs({
  allowPositionals: true,
  options: { 'sqlite-fixture-root': { type: 'string' } },
});
const [schemaDirectory, stdioObservationPath, windowsBoundaryPath] = positionals;
if (!schemaDirectory || positionals.length > 3) {
  throw new Error('Usage: node packages/contracts/runtime/probe-local.mts <generated-schema-directory> [stdio-observation-json [windows-boundary-json]] [--sqlite-fixture-root <directory>]');
}

const [protocol, protocolV2] = await Promise.all([
  readFile(join(schemaDirectory, 'codex_app_server_protocol.schemas.json')),
  readFile(join(schemaDirectory, 'codex_app_server_protocol.v2.schemas.json')),
]);
const sha256 = (bytes: Buffer) => createHash('sha256').update(bytes).digest('hex');
const missing = inspectRuntimeSchema(JSON.parse(protocol.toString('utf8')), JSON.parse(protocolV2.toString('utf8')));
const windowsBoundary = windowsBoundaryPath ? JSON.parse(await readFile(windowsBoundaryPath, 'utf8')) : undefined;
const stdioMissing = stdioObservationPath
  ? inspectStdioObservation(JSON.parse(await readFile(stdioObservationPath, 'utf8')), windowsBoundary)
  : null;

const db = new DatabaseSync(':memory:');
let compileOptions: unknown[];
let fts5Match: boolean;
try {
  compileOptions = db.prepare('PRAGMA compile_options').all().map((row) => row.compile_options).sort();
  db.exec("CREATE VIRTUAL TABLE sample USING fts5(body); INSERT INTO sample VALUES ('проект поиск');");
  fts5Match = db.prepare('SELECT count(*) AS matches FROM sample WHERE sample MATCH ?').get('проект')?.matches === 1;
} finally {
  db.close();
}

const fixtureRoot = values['sqlite-fixture-root'];
const fixture = fixtureRoot === undefined ? null : await verifySqliteQualification(fixtureRoot);
const staticChecksPassed = missing.length === 0 && fts5Match
  && (fixture === null || Object.values(fixture).every((verified) => verified === true));
const status = !staticChecksPassed ? 'static_checks_failed'
  : stdioMissing === null ? 'static_checks_passed'
  : stdioMissing.length === 0 ? 'stdio_checks_passed' : 'stdio_checks_blocked';
const evidence = {
  platform: process.platform,
  arch: process.arch,
  osRelease: release(),
  nodeVersion: process.version,
  sqlite: { version: process.versions.sqlite, compileOptions, fts5Match, fixture },
  schema: { sha256: sha256(protocol), v2Sha256: sha256(protocolV2), missing },
  stdio: stdioMissing === null ? null : { missing: stdioMissing },
  status,
};
console.log(JSON.stringify(evidence, null, 2));
process.exitCode = staticChecksPassed && (stdioMissing === null || stdioMissing.length === 0) ? 0 : 1;
