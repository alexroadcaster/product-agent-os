import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile,mkdir,writeFile} from 'node:fs/promises';
import {performance} from 'node:perf_hooks';
import {analyzeCodeDatabase} from '../../apps/local-service/src/code-database/analyzer.mts';
const corpus=JSON.parse(await readFile(new URL('../fixtures/func_g04/code-database/corpus.json',import.meta.url),'utf8'));
const files=corpus.files.map((f:any)=>({relativePath:f.relativePath,text:f.content}));
const analyze=(input=files)=>analyzeCodeDatabase(input,{sourcePath:corpus.sourcePath,tables:corpus.tables,codeRevision:'code-fixture',schemaRevision:'schema-fixture'});
test('shadowed URL and TypeScript constructor parameter properties cannot confirm selected database identity',()=>{
 const query="db.prepare('SELECT * FROM users');",constructor="const db=new DatabaseSync(new URL('../app.sqlite',import.meta.url));";
 for(const text of [constructor+`class X{constructor(private db:any){${query}}}`,
  `class URL{};${constructor}${query}`,`function f(URL:any){${constructor}${query}}`,
  `import URL from './fake';${constructor}${query}`,`function URL(){};${constructor}${query}`]){
  const result=analyze([{relativePath:'src/shadow.ts',text:"import {DatabaseSync} from 'node:sqlite';"+text}]);
  assert.equal(result.links.filter(link=>link.confidence==='confirmed').length,0,text);
 }
});
test('DELETE writes only its target while nested SELECT sources remain reads',()=>{
 const result=analyze([{relativePath:'src/delete.ts',text:`import {DatabaseSync} from 'node:sqlite';const db=new DatabaseSync(new URL('../app.sqlite',import.meta.url));db.prepare('DELETE FROM users WHERE id IN (SELECT user_id FROM orders)');`}]);
 assert.deepEqual(result.links.map(link=>[link.table,link.operation,link.confidence]),[['users','write','confirmed'],['orders','read','confirmed']]);
});
test('pinned JS/TS, SQL and Prisma corpus exactly matches source/operation/confidence ground truth',()=>{const at=performance.now(),result=analyze(),key=(x:any)=>JSON.stringify([x.relativePath,x.line??x.span.start.line,x.table,x.operation,x.confidence]);assert.deepEqual(result.links.map(key).sort(),corpus.expected.map(key).sort());assert.ok(result.reasons.includes('unsupported_language:src/unsupported.py'));const serialized=JSON.stringify(result);assert.ok(!serialized.includes('secret_value'));assert.ok(!serialized.includes('comment_only'));assert.ok(!serialized.includes('string_only'));assert.ok(result.links.filter(x=>x.confidence==='confirmed').every(x=>x.sourcePath==='app.sqlite'));assert.ok(result.links.every(x=>x.codeRevision==='code-fixture'&&x.schemaRevision==='schema-fixture'));assert.ok(performance.now()-at<30000);});
test('Prisma env datasource and ambiguous schemas stay unresolved, never a naming match confirmation',()=>{const env=files.map((f:any)=>f.relativePath.endsWith('.prisma')?{...f,text:f.text.replace('"file:../app.sqlite"','env("DATABASE_URL")')}:f);assert.ok(analyze(env).links.filter(x=>x.method==='prisma_static').every(x=>x.confidence==='unresolved'));const other=[...files,{relativePath:'other/schema.prisma',text:'datasource db { provider = "sqlite" url = "file:../other.sqlite" } model User { id Int @id @@map("users") }'}];assert.ok(analyze(other).links.filter(x=>x.method==='prisma_static').every(x=>x.confidence!=='confirmed'));});
test('lexical declarations, quoted identifiers, SQL comments/strings and CTEs cannot fabricate confirmed references',()=>{const result=analyze([{relativePath:'src/adversarial.ts',text:`import {DatabaseSync} from 'node:sqlite';
const db=new DatabaseSync(new URL('../app.sqlite',import.meta.url));
db.exec('SELECT "orders" FROM "users" -- JOIN old_table');
db.exec("WITH users AS (SELECT 1) SELECT * FROM users");
function f(DatabaseSync:any){const shadow=new DatabaseSync(new URL('../app.sqlite',import.meta.url));shadow.exec('SELECT * FROM orders');}
`}]);assert.equal(result.links.filter(x=>x.confidence==='confirmed').length,1);assert.equal(result.links.filter(x=>x.reason==='sql_cte_unresolved').length,1);assert.ok(result.links.some(x=>x.table==='orders'&&x.confidence==='unresolved'));});

test('Prisma custom outputs/config and malformed schema preserve explicit unresolved coverage',()=>{for(const replacement of ['provider = "prisma-client-js"\n output = "../custom-client"','provider = "prisma-client"']){const custom=files.map((f:any)=>f.relativePath.endsWith('.prisma')?{...f,text:f.text.replace('provider = "prisma-client-js"',replacement)}:f),result=analyze(custom);assert.ok(result.links.some(x=>x.method==='prisma_static'));assert.ok(result.links.filter(x=>x.method==='prisma_static').every(x=>x.confidence==='unresolved'));}const configured=analyze([...files,{relativePath:'prisma.config.ts',text:'export default {};'}]);assert.ok(configured.links.filter(x=>x.method==='prisma_static').every(x=>x.confidence==='unresolved'));assert.ok(configured.reasons.includes('prisma_config_unresolved'));const malformed=analyze([...files,{relativePath:'broken/schema.prisma',text:'model "unterminated'}]);assert.ok(malformed.reasons.includes('prisma_schema_parse_unavailable'));assert.ok(malformed.links.some(x=>x.method==='literal_sql'&&x.confidence==='confirmed'));});

test('literal semicolons cannot escape CTE unresolved handling and var/function shadowing cannot confirm a foreign receiver',()=>{const result=analyze([{relativePath:'src/edge.ts',text:`import {DatabaseSync} from 'node:sqlite';const db=new DatabaseSync(new URL('../app.sqlite',import.meta.url));
db.exec("WITH users AS (SELECT ';') SELECT * FROM users");
function local(){if(true){var db={prepare:()=>{}};}db.prepare('SELECT * FROM users');}
`}]);assert.equal(result.links.filter(x=>x.confidence==='confirmed').length,0);assert.ok(result.links.some(x=>x.reason==='sql_cte_unresolved'));});

test('per-method ground-truth precision and recall retain literal denominators in an evaluation receipt',async()=>{const at=performance.now(),result=analyze(),key=(x:any)=>JSON.stringify([x.relativePath,x.line??x.span.start.line,x.table,x.operation]),methods=['literal_sql','prisma_static'],metrics=methods.map(method=>{const expected=corpus.expected.filter((x:any)=>x.confidence==='confirmed'&&(x.relativePath==='src/orm.ts'?'prisma_static':'literal_sql')===method),actual=result.links.filter(x=>x.method===method&&x.confidence==='confirmed'),truth=new Set(expected.map(key)),found=new Set(actual.map(key)),truePositive=actual.filter(x=>truth.has(key(x))).length,precision=actual.length?truePositive/actual.length:null,recall=expected.length?expected.filter((x:any)=>found.has(key(x))).length/expected.length:null;assert.equal(precision,1);assert.ok(recall!==null&&recall>=.9);return {method,expectedConfirmed:expected.length,actualConfirmed:actual.length,truePositive,precision,recall};});const root=new URL('../../.tmp/func-g04/code-database/',import.meta.url);await mkdir(root,{recursive:true});await writeFile(new URL('ground-truth-'+Date.now()+'.json',root),JSON.stringify({schemaVersion:'paos_code_database_accuracy_v1',observedAt:new Date().toISOString(),parserVersion:result.parserVersion,milliseconds:performance.now()-at,expectedEdges:corpus.expected.length,actualEdges:result.links.length,metrics},null,2));});
