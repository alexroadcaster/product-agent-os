import test from 'node:test';import assert from 'node:assert/strict';import {writeFile} from 'node:fs/promises';import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';import {runGraphParser} from '../../apps/local-service/src/code-index/parser-runner.mts';import {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';
test('native parser failure is contained in an owned child and the graph owner remains usable',async t=>{
 const f=await m2Fixture(t),index=createCodeIndex(f.store);await writeFile(join(f.root,'safe.ts'),'export const safe=1;');const old=await index.rebuild('p');
 await writeFile(join(f.root,'deep.ts'),'('.repeat(12000)+'1'+')'.repeat(12000));
 try{const result=await index.rebuild('p');assert.ok(result.coverage?.some(c=>c.relativePath==='deep.ts'&&c.status!=='indexed'));}catch(e){assert.ok(['GRAPH_PARSER_UNAVAILABLE','GRAPH_BUILD_LIMIT'].includes((e as any).code));assert.equal((await index.status('p')).revision,old.revision);}
 await writeFile(join(f.root,'deep.ts'),'export const recovered=2;');const recovered=await index.rebuild('p');assert.equal(recovered.state,'fresh');assert.equal(recovered.coverage?.find(c=>c.relativePath==='deep.ts')?.status,'indexed');assert.equal(recovered.coverage?.find(c=>c.relativePath==='safe.ts')?.status,'indexed');
});
test('parser deadline and cancellation terminate only the owned child before resolving',async()=>{
 const input={files:[{relativePath:'file.ts',text:'export const value=1;',language:'ts'}]};let pid=0;
 await assert.rejects(runGraphParser(input,{milliseconds:1,onChildStarted:child=>pid=child}),{code:'GRAPH_BUILD_LIMIT'});assert.ok(pid>0);assert.throws(()=>process.kill(pid,0));
 const signal=new AbortController();await assert.rejects(runGraphParser(input,{signal:signal.signal,onChildStarted:child=>{pid=child;signal.abort();}}),{code:'GRAPH_BUILD_CANCELLED'});assert.throws(()=>process.kill(pid,0));
 assert.ok((await runGraphParser(input)).results.length);
});
