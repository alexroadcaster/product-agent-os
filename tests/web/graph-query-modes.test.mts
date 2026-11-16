import test from 'node:test';import assert from 'node:assert/strict';import {writeFile} from 'node:fs/promises';import {join} from 'node:path';import {m2Fixture} from './m2-fixture.mts';import {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';
test('dependency/symbol views, directional neighborhoods and bounded paths share one revision',async t=>{
 const f=await m2Fixture(t);for(const [path,text] of Object.entries({'a.ts':'import {b} from "./b";export const a=b;','b.ts':'import {c} from "./c";export const b=c;','c.ts':'export const c=1;'}))await writeFile(join(f.root,path),text);
 const index=createCodeIndex(f.store),built=await index.rebuild('p'),q=(extra:Record<string,string>)=>new URLSearchParams({revision:built.revision!,limit:'100',...extra});
 const deps=await index.graph('p',q({mode:'dependencies'}));assert.ok(deps.nodes.every(n=>n.kind==='file'||n.kind==='unresolved'));assert.ok(deps.edges.every(e=>e.type==='import'));
 const ids=Object.fromEntries(deps.nodes.filter(n=>n.kind==='file').map(n=>[n.relativePath,n.id]));
 const outgoing=await index.graph('p',q({mode:'dependencies',nodeId:ids['b.ts'],direction:'outgoing',depth:'1'}));assert.deepEqual(outgoing.nodes.map(n=>n.relativePath).sort(),['b.ts','c.ts']);
 const incoming=await index.graph('p',q({mode:'dependencies',nodeId:ids['b.ts'],direction:'incoming',depth:'1'}));assert.deepEqual(incoming.nodes.map(n=>n.relativePath).sort(),['a.ts','b.ts']);
 const path=await index.graph('p',q({mode:'dependencies',nodeId:ids['a.ts'],pathTo:ids['c.ts'],direction:'outgoing'}));assert.equal(path.path?.state,'found');assert.equal(path.edges.length,2);assert.deepEqual(path.path?.nodeIds,[ids['a.ts'],ids['b.ts'],ids['c.ts']]);
 const symbols=await index.graph('p',q({mode:'symbols'}));assert.ok(symbols.nodes.length);assert.ok(symbols.nodes.every(n=>n.kind==='symbol'||n.kind==='unresolved'));assert.equal(symbols.revision,deps.revision);
 await assert.rejects(index.graph('p',q({mode:'runtime'})),{code:'GRAPH_QUERY_INVALID'});
 const old=await index.graph('p',new URLSearchParams({revision:built.revision!,limit:'1'}));assert.ok(old.nextCursor);await index.rebuild('p');await assert.rejects(index.graph('p',new URLSearchParams({revision:built.revision!,limit:'1',cursor:old.nextCursor!})),{code:'GRAPH_CURSOR_INVALID'});
});
