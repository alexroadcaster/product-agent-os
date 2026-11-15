import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,rm,stat,realpath} from 'node:fs/promises';
import {resolve,join,dirname} from 'node:path';
import {DatabaseSync} from 'node:sqlite';
import {createHash} from 'node:crypto';
import {inspectSqlite,normalizeSchema,canonicalMermaid,stableSchemaRead,runTbls} from './tbls-poc.mts';

async function fixture(t:any){const root=resolve('.tmp/func-g02/f32');await mkdir(root,{recursive:true});const dir=await mkdtemp(join(root,'unit-'));t.after(async()=>{const actual=await realpath(dir);assert.equal(dirname(actual),await realpath(root),'CLEANUP_BOUNDARY');await rm(actual,{recursive:true,force:true});});return dir;}
test('metadata baseline preserves generated/composite/self-reference/no-FK ground truth without source writes',async t=>{
 const root=await fixture(t),path=join(root,'schema.db'),sql=await readFile(new URL('./tbls-fixture.sql',import.meta.url),'utf8'),db=new DatabaseSync(path);db.exec(sql);db.close();
 const before=createHash('sha256').update(await readFile(path)).digest('hex'),value=inspectSqlite(path),snapshot=normalizeSchema(value,sql);
 assert.equal(value.tables.length,6);assert.equal(snapshot.edges.length,3);
 assert.equal(value.tables.find(v=>v.name==='parent')!.columns.find(v=>v.name==='doubled').generated,true);
 assert.equal(snapshot.edges.filter(e=>e.columns.length===2).length,1);
 assert.equal(snapshot.edges.some(e=>e.from===e.to),true);
 assert.equal(snapshot.edges.some(e=>e.from===snapshot.nodes.find(n=>n.name==='orphan')!.id),false);
 assert.equal(snapshot.nodes.find(n=>n.name==='parent')!.line,2);
 assert.equal(snapshot.nodes.find(n=>n.name==='child')!.line,13);
 assert.equal(createHash('sha256').update(await readFile(path)).digest('hex'),before);
});
test('read-only baseline never creates a missing database and refuses corrupt files',async t=>{
 const root=await fixture(t),missing=join(root,'missing.db');assert.throws(()=>inspectSqlite(missing));assert.equal(await stat(missing).then(()=>true,()=>false),false);
 const corrupt=join(root,'corrupt.db');await writeFile(corrupt,'synthetic-corrupt');assert.throws(()=>inspectSqlite(corrupt));
});
test('effective nullable distinguishes rowid aliases from ordinary nullable primary keys',async t=>{
 const root=await fixture(t),path=join(root,'schema.db'),db=new DatabaseSync(path);
 db.exec('CREATE TABLE alias(id INTEGER PRIMARY KEY); CREATE TABLE nullable_text(id TEXT PRIMARY KEY); CREATE TABLE nullable_int(id INT PRIMARY KEY); CREATE TABLE nullable_desc(id INTEGER PRIMARY KEY DESC); CREATE TABLE table_desc_alias(id INTEGER, PRIMARY KEY(id DESC)); CREATE TABLE composite(a INTEGER,b TEXT,PRIMARY KEY(a,b)); CREATE TABLE without_rowid(id TEXT PRIMARY KEY) WITHOUT ROWID; CREATE TABLE strict_pk(id TEXT PRIMARY KEY) STRICT;');
 const schema=inspectSqlite(path),column=(name:string)=>schema.tables.find(t=>t.name===name)!.columns[0];
 assert.equal(column('alias').notNullDeclared,false);assert.equal(column('alias').nullable,false);
 assert.equal(column('table_desc_alias').nullable,false);
 for(const name of ['nullable_text','nullable_int','nullable_desc','composite'])assert.equal(column(name).nullable,true,name);
 for(const name of ['without_rowid','strict_pk'])assert.equal(column(name).nullable,false,name);
 // Observe stored values separately from INSERT acceptance: a NULL alias input allocates a non-NULL rowid.
 db.exec('INSERT INTO alias VALUES(NULL); INSERT INTO nullable_text VALUES(NULL); INSERT INTO nullable_int VALUES(NULL); INSERT INTO nullable_desc VALUES(NULL)');
 assert.equal((db.prepare('SELECT id IS NULL AS is_null FROM alias').get() as any).is_null,0);
 for(const name of ['nullable_text','nullable_int','nullable_desc'])assert.equal((db.prepare('SELECT id IS NULL AS is_null FROM '+name).get() as any).is_null,1,name);
 db.close();
});
test('stable metadata envelope marks concurrent schema change stale rather than claiming a current revision',async t=>{
 const root=await fixture(t),path=join(root,'schema.db'),db=new DatabaseSync(path);db.exec('PRAGMA journal_mode=WAL; CREATE TABLE initial(id INT)');
 const stable=await stableSchemaRead(path,async()=>1);assert.equal(stable.state,'current');
 const stale=await stableSchemaRead(path,async()=>{await Promise.resolve();db.exec('CREATE TABLE concurrent(id INT)');return 2;});assert.equal(stale.state,'stale');assert.notEqual(stale.beforeRevision,stale.afterRevision);db.close();
});
test('canonical Mermaid encodes malicious identifiers and preserves declared relationship counts',async t=>{
 const root=await fixture(t),path=join(root,'schema.db'),db=new DatabaseSync(path);db.exec('CREATE TABLE "<script>bad" ("x\"\"y" TEXT)');db.close();const value=normalizeSchema(inspectSqlite(path));
 assert.equal(value.nodes[0].line,null);const mermaid=canonicalMermaid(value);assert.equal(mermaid.startsWith('erDiagram\n'),true);assert.equal(mermaid.includes('<script>'),false);assert.equal(mermaid.includes('"'),false);
});
test('guarded tbls boundary rejects outside and missing paths before launching any native process',async t=>{
 const root=await fixture(t);await assert.rejects(runTbls('DO_NOT_EXECUTE',resolve('package.json'),root,'DO_NOT_EXECUTE'),/OUTSIDE_POC_ROOT/);
 await assert.rejects(runTbls('DO_NOT_EXECUTE',join(root,'missing.db'),root,'DO_NOT_EXECUTE'),/ENOENT/);
});
