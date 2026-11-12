import {test} from 'node:test';
import assert from 'node:assert/strict';
import {join} from 'node:path';
import {writeFile,readFile,link,unlink,mkdir,symlink,rename} from 'node:fs/promises';
import {bindProject} from '../../apps/local-service/src/adapters/project-sources.ts';
import {createHash} from 'node:crypto';
import {m2Fixture} from './m2-fixture.mts';
import {createLocalApplication} from '../../apps/local-service/src/http/application.mts';

async function paired(f:Awaited<ReturnType<typeof m2Fixture>>){
 const origin='http://127.0.0.1:49831',app=await createLocalApplication({store:f.store,origin,instanceId:'code-index',profileDirectory:join(f.root,'profile')});
 const r=await app.handleRequest(new Request(origin+'/bootstrap/exchange',{method:'POST',headers:{host:'127.0.0.1:49831',origin,'content-type':'application/json'},body:JSON.stringify({code:app.issuePairingCode()})}));
 const cookie=r.headers.get('set-cookie')!.split(';')[0],csrf=(await r.json() as any).csrfToken;
 return async(path:string,input?:unknown,project='p')=>{const response=await app.handleRequest(new Request(origin+'/api/v1/projects/'+project+path,{method:input===undefined?'GET':'POST',headers:{host:'127.0.0.1:49831',origin,cookie,'x-paos-csrf':csrf,'content-type':'application/json'},...(input===undefined?{}:{body:JSON.stringify(input)})}));return {status:response.status,body:await response.json() as any};};
}
test('authenticated graph status and immutable read-only rebuild',async t=>{
 const f=await m2Fixture(t),request=await paired(f);
 assert.equal((await request('/graph/status')).status,200);
 assert.equal((await request('/graph/status')).body.state,'unavailable');
 await writeFile(join(f.root,'main.ts'),'const value = 1; function use(){ return value; } use();');
 const built=await request('/graph/rebuild',{});assert.equal(built.status,200);assert.equal(built.body.state,'fresh');
 const graph=await request('/graph?revision='+built.body.revision);assert.equal(graph.status,200);assert.ok(graph.body.nodes.some((n:any)=>n.name==='value'));
});
test('foreign revision/cursor, restart and changed root identity cannot bypass source authority',async t=>{
 const f=await m2Fixture(t),other=await m2Fixture(t),request=await paired(f);
 await writeFile(join(f.root,'root.ts'),'const rootOnly=1;');await writeFile(join(other.root,'foreign.ts'),'const foreignOnly=1;');
 const binding=await bindProject('q',other.root);await f.store.registerProject({id:'q',keyPrefix:'QQQQ',canonicalRoot:binding.workspaceRoot,rootIdentity:binding.directoryIdentity,authorityMode:'sql'});
 const p=(await request('/graph/rebuild',{})).body;
 const graph=(await request('/graph?revision='+p.revision+'&limit=1')).body;assert.ok(!JSON.stringify(graph).includes('foreignOnly'));
 const q=(await request('/graph/rebuild',{},'q')).body;assert.equal((await request('/graph?revision='+p.revision,undefined,'q')).status,409);
 assert.equal((await request('/graph?revision='+q.revision+'&limit=1&cursor='+encodeURIComponent(graph.nextCursor),undefined,'q')).status,400);
 const restarted=await paired(f);assert.equal((await restarted('/graph/status')).body.state,'unavailable');
 const previous=join(other.root,'nested');await mkdir(previous);const pin=await bindProject('r',previous);await f.store.registerProject({id:'r',keyPrefix:'RRRR',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
 await rename(previous,join(other.root,'old-nested'));await mkdir(previous);assert.equal((await request('/graph/rebuild',{},'r')).status,409);
});
test('relative static imports link files; aliases, catch/loop scopes and property keys stay honest',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await writeFile(join(f.root,'dep.ts'),'export function run(){ return 1; }');await writeFile(join(f.root,'entry.ts'),'import {run as alias} from "./dep"; alias(); let index=0; for(let index=1; index<2; index++){ index; } try { throw 1; } catch(index){ index; } const data:{field:TypeOnly} = {field: alias}; data.field;');
 const built=(await request('/graph/rebuild',{})).body,g=(await request('/graph?revision='+built.revision+'&limit=100')).body;
 const entry=g.nodes.find((n:any)=>n.name==='entry.ts'),dep=g.nodes.find((n:any)=>n.name==='dep.ts');assert.ok(g.edges.some((e:any)=>e.type==='import'&&e.from===entry.id&&e.to===dep.id&&e.resolution==='lexical'));
 assert.equal(g.nodes.filter((n:any)=>n.name==='index'&&n.kind==='symbol').length,3);assert.ok(!g.nodes.some((n:any)=>n.name==='TypeOnly'||n.name==='field'));const alias=g.nodes.find((n:any)=>n.name==='alias'&&n.kind==='symbol');assert.equal(alias.reason,'module_alias_unresolved');assert.ok(g.edges.some((e:any)=>e.to===alias.id&&e.type==='call'&&e.resolution==='unresolved'));
});
test('junction sources are excluded without following external content',async t=>{
 const f=await m2Fixture(t),other=await m2Fixture(t),request=await paired(f);await writeFile(join(other.root,'outside.ts'),'const outside=1;');
 try{await symlink(other.root,join(f.root,'linked'),'junction');}catch(error){if((error as any).code==='EPERM'){t.skip('sandbox cannot create junction fixture (EPERM)');return;}throw error;}
 const built=(await request('/graph/rebuild',{})).body;assert.ok(built.coverage.some((c:any)=>c.relativePath==='linked'&&c.status==='excluded'));const graph=(await request('/graph?revision='+built.revision)).body;assert.ok(!graph.nodes.some((n:any)=>n.name==='outside'));
});
test('impact keeps matching and stale source pins distinct from the graph revision',async t=>{
 const f=await m2Fixture(t),request=await paired(f),source='const pinned=1;',hash=createHash('sha256').update(source).digest('hex');await writeFile(join(f.root,'pin.ts'),source);
 const matching=await f.create('Matching',{fileContexts:[{relativePath:'pin.ts',revision:hash,context:'Pinned source'}]}),stale=await f.create('Stale',{fileContexts:[{relativePath:'pin.ts',revision:'0'.repeat(64),context:'Earlier source'}]}),artifact=await f.create('Artifact',{artifactReferences:['pin.ts']});
 const built=(await request('/graph/rebuild',{})).body,g=(await request('/graph?revision='+built.revision)).body,node=g.nodes.find((n:any)=>n.kind==='symbol'),impact=(await request('/graph/nodes/'+node.id+'/impact?revision='+built.revision)).body;
 assert.equal(impact.tasks.find((r:any)=>r.id===matching.id).sourceState,'matching');assert.equal(impact.tasks.find((r:any)=>r.id===stale.id).sourceState,'stale');assert.equal(impact.tasks.find((r:any)=>r.id===artifact.id).sourceState,'unknown');assert.equal(impact.tasks.find((r:any)=>r.id===stale.id).actualSourceRevision,hash);
});
test('source byte budget rejects oversized build without replacing a valid snapshot',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await writeFile(join(f.root,'small.ts'),'let small=1');const old=(await request('/graph/rebuild',{})).body;
 await writeFile(join(f.root,'large.ts'),' '.repeat(512*1024+1));const failed=await request('/graph/rebuild',{});assert.equal(failed.status,400);assert.equal(failed.body.error.code,'GRAPH_SOURCE_LIMIT');assert.equal((await request('/graph/status')).body.revision,old.revision);assert.equal((await request('/graph/status')).body.state,'stale');
});
test('two-pass scopes, destructuring, hoisting and Unicode CRLF anchors distinguish read/write/reference',async t=>{
 const f=await m2Fixture(t),request=await paired(f);
 const source='const имя=1;\r\nfunction first({value: alias}) { before(); var before=()=>alias; let имя=2; { let имя=3; имя++; } return имя; }\r\nfunction second(){ return имя; }\r\nconst obj={property:имя}; obj.property += 1; import("./dynamic"); eval("private literal");';
 await writeFile(join(f.root,'scope.ts'),source);const built=(await request('/graph/rebuild',{})).body,params='?revision='+built.revision+'&limit=100';
 const {body:g}=await request('/graph'+params);const same=g.nodes.filter((n:any)=>n.name==='имя'&&n.kind==='symbol');assert.equal(same.length,3);assert.equal(new Set(same.map((n:any)=>n.scope)).size,3);
 const inner=same.find((n:any)=>source.slice(n.anchor.start-4,n.anchor.start)==='let '&&n.anchor.start>source.indexOf('{ let'));
 assert.ok(inner);const uses=g.edges.filter((e:any)=>e.to===inner.id);assert.ok(uses.some((e:any)=>e.type==='read'));assert.ok(uses.some((e:any)=>e.type==='write'));
 for(const n of same)assert.equal(source.slice(n.anchor.start,n.anchor.end),'имя');
 assert.ok(g.nodes.some((n:any)=>n.name==='alias'&&n.kind==='symbol'));assert.ok(!g.nodes.some((n:any)=>n.name==='property'&&n.kind==='unresolved'));
 const before=g.nodes.find((n:any)=>n.name==='before'&&n.kind==='symbol');assert.ok(g.edges.some((e:any)=>e.type==='call'&&e.to===before.id));
 assert.ok(g.nodes.some((n:any)=>n.reason==='dynamic_import'));assert.ok(g.nodes.some((n:any)=>n.reason==='eval'));
 assert.ok(!JSON.stringify(g).includes('private literal'));assert.ok(!JSON.stringify(g).includes('./dynamic'));
 assert.deepEqual(await readFile(join(f.root,'scope.ts'),'utf8'),source);
});
test('manifest notices added, modified, deleted sources and pins revision/source independently of client paths',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await writeFile(join(f.root,'a.ts'),'let x=1; x++;');
 const a=(await request('/graph/rebuild',{})).body,graph=(await request('/graph?revision='+a.revision)).body,file=graph.nodes.find((n:any)=>n.kind==='file');
 assert.equal((await request('/graph/source?revision='+a.revision+'&fileId='+file.id+'&start=0&end=3')).body.content,'let');
 assert.equal((await request('/graph/source?revision='+a.revision+'&fileId=../../outside')).status,404);
 await writeFile(join(f.root,'b.ts'),'const b=2');assert.equal((await request('/graph/status')).body.state,'stale');assert.equal((await request('/graph/source?revision='+a.revision+'&fileId='+file.id)).status,409);
 const b=(await request('/graph/rebuild',{})).body;assert.notEqual(a.revision,b.revision);assert.equal((await request('/graph?revision='+a.revision)).status,409);
 await writeFile(join(f.root,'a.ts'),'let x=3;');assert.equal((await request('/graph/status')).body.state,'stale');await request('/graph/rebuild',{});await unlink(join(f.root,'b.ts'));assert.equal((await request('/graph/status')).body.state,'stale');
});
test('parse failures, unsupported source, type-only names, secrets and linked files stay explicit',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await writeFile(join(f.root,'ok.ts'),'type T = MissingType; const token="syntheticCredentialCanaryXYZ"; const object={key: 1}; object.key;');
 await writeFile(join(f.root,'broken.ts'),'const = ;');await writeFile(join(f.root,'other.py'),'answer=42');await writeFile(join(f.root,'.env.ts'),'const privateValue=1');await link(join(f.root,'ok.ts'),join(f.root,'hard.ts'));
 let built=(await request('/graph/rebuild',{})).body;assert.ok(built.coverage.some((c:any)=>c.status==='excluded'));await unlink(join(f.root,'hard.ts'));built=(await request('/graph/rebuild',{})).body;
 assert.ok(built.coverage.some((c:any)=>c.status==='parse_error'));assert.ok(built.coverage.some((c:any)=>c.status==='unsupported'));assert.ok(!built.coverage.some((c:any)=>c.relativePath==='.env.ts'));
 const g=(await request('/graph?revision='+built.revision)).body;assert.ok(!g.nodes.some((n:any)=>n.name==='MissingType'));const file=g.nodes.find((n:any)=>n.kind==='file');const excerpt=(await request('/graph/source?revision='+built.revision+'&fileId='+file.id)).body;assert.equal(excerpt.redacted,true);assert.ok(!JSON.stringify(excerpt).includes('syntheticCredentialCanaryXYZ'));
});
test('pagination binds revision and all filters and impact matches explicit task paths',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await writeFile(join(f.root,'many.ts'),Array.from({length:120},(_,i)=>`let item${i}=${i}; item${i}++;`).join('\n'));
 await f.create('Related',{files:[{relativePath:'many.ts',plannedOperation:'modify',actualOperation:null}]});const built=(await request('/graph/rebuild',{})).body,base='/graph?revision='+built.revision+'&limit=10',first=(await request(base)).body;
 assert.equal(first.nodes.length,10);assert.ok(first.nextCursor);assert.equal((await request(base+'&cursor='+encodeURIComponent(first.nextCursor))).status,200);
 assert.equal((await request(base+'&query=item&cursor='+encodeURIComponent(first.nextCursor))).status,400);assert.equal((await request(base+'&cursor=corrupt')).status,400);assert.equal((await request('/graph?revision='+built.revision+'&depth=4')).status,400);assert.equal((await request('/graph?revision='+built.revision+'&limit=101')).status,400);
 const symbol=first.nodes.find((n:any)=>n.kind==='symbol'),impact=(await request('/graph/nodes/'+symbol.id+'/impact?revision='+built.revision+'&limit=2')).body;assert.equal(impact.tasks[0].matchReason,'files:explicit_path');assert.ok(impact.edges.length<=2);
});
test('assignment destructuring reads computed keys and defaults while writing targets',async t=>{
 const f=await m2Fixture(t),request=await paired(f),source='let target=0; const key="a", fallback=1, source={}; ({[key]: target=fallback} = source);';await writeFile(join(f.root,'roles.ts'),source);
 const built=(await request('/graph/rebuild',{})).body,g=(await request('/graph?revision='+built.revision)).body;
 for(const name of ['key','fallback','source']){const node=g.nodes.find((n:any)=>n.kind==='symbol'&&n.name===name),uses=g.edges.filter((e:any)=>e.to===node.id&&e.type!=='define');assert.ok(uses.some((e:any)=>e.type==='read'),name+' must be read');assert.ok(!uses.some((e:any)=>e.type==='write'),name+' must not be written');}
 const target=g.nodes.find((n:any)=>n.kind==='symbol'&&n.name==='target');assert.ok(g.edges.some((e:any)=>e.to===target.id&&e.type==='write'));
});
test('switch discriminant uses outer binding while cases share switch lexical binding',async t=>{
 const f=await m2Fixture(t),request=await paired(f),source='const value=0; switch(value){case 0: let value=1; break; default: value++;}';await writeFile(join(f.root,'switch.ts'),source);
 const built=(await request('/graph/rebuild',{})).body,g=(await request('/graph?revision='+built.revision)).body,values=g.nodes.filter((n:any)=>n.kind==='symbol'&&n.name==='value'),outer=values.find((n:any)=>n.scope==='module:0'),inner=values.find((n:any)=>n.scope!=='module:0');
 const discriminant=g.edges.find((e:any)=>e.anchor.start===source.indexOf('value',source.indexOf('switch'))&&e.type==='read');assert.equal(discriminant.to,outer.id);assert.ok(g.edges.some((e:any)=>e.to===inner.id&&e.type==='write'));assert.ok(!g.edges.some((e:any)=>e.to===outer.id&&e.type==='write'));
});
test('later graph pages hydrate bounded off-page edge endpoints without changing primary cursor',async t=>{
 const f=await m2Fixture(t),request=await paired(f);await writeFile(join(f.root,'wide.ts'),Array.from({length:120},(_,i)=>`const child${i}=${i};`).join('\n'));
 const built=(await request('/graph/rebuild',{})).body,base='/graph?revision='+built.revision+'&limit=10',first=(await request(base)).body,second=(await request(base+'&cursor='+encodeURIComponent(first.nextCursor))).body;
 assert.equal(second.nodes.length,10);assert.ok(second.nodes.every((n:any)=>n.kind==='symbol'));assert.ok(second.edges.some((e:any)=>e.type==='define'&&second.nodes.some((n:any)=>n.id===e.to)));
 assert.ok(second.contextNodes.some((n:any)=>n.kind==='file'));const endpoints=new Set([...second.nodes,...second.contextNodes].map((n:any)=>n.id));assert.ok(second.edges.every((e:any)=>endpoints.has(e.from)&&endpoints.has(e.to)));assert.ok(second.edges.length<=100);assert.ok(second.contextNodes.length<=100);assert.ok(second.contextNodes.every((c:any)=>!second.nodes.some((n:any)=>n.id===c.id)));assert.ok(first.partial);
});
