import {test} from 'node:test';
import assert from 'node:assert/strict';
import {writeFile,readFile,mkdir,access} from 'node:fs/promises';
import {join} from 'node:path';
import {m2Fixture} from './m2-fixture.mts';
import {createArtifactCatalog} from '../../apps/local-service/src/artifacts/service.mts';
import {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';
import {inventoryForProject} from '../../apps/local-service/src/code-index/sources.mts';
import {bindProject,inspectProjectSources,readProjectSource} from '../../apps/local-service/src/adapters/project-sources.ts';

test('policy changes invalidate catalog cursors and revoke document reads across consumers',async t=>{
 const f=await m2Fixture(t);await writeFile(join(f.root,'a.md'),'# A\n');await writeFile(join(f.root,'b.md'),'# B\n');
 const catalog=createArtifactCatalog(f.store),page=await catalog.catalog('p',new URLSearchParams({kind:'documents',limit:'1'}));assert.ok(page.nextCursor);
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['*.md']}});
 await assert.rejects(catalog.catalog('p',new URLSearchParams({kind:'documents',limit:'1',cursor:page.nextCursor!})),{code:'CURSOR_STALE'});
 assert.equal((await catalog.read('p',page.items[0].id,page.items[0].source.version)).state,'unavailable');
 assert.equal((await catalog.catalog('p',new URLSearchParams({kind:'documents'}))).items.length,0);
});

test('code graph and fixed sources share explicit inventory policy and revision invalidation',async t=>{
 const f=await m2Fixture(t);await writeFile(join(f.root,'visible.ts'),'export const visible=1;');await writeFile(join(f.root,'ignored.ts'),'export const ignored=2;');await writeFile(join(f.root,'.gitignore'),'ignored.ts\n');await writeFile(join(f.root,'REQUIREMENTS.md'),'# Required source\n');
 const index=createCodeIndex(f.store),built=await index.rebuild('p');
 assert.ok(built.inventory?.policyVersion);assert.ok(built.coverage!.some(row=>row.relativePath==='ignored.ts'&&row.reason==='gitignore'));
 const graph=await index.graph('p',new URLSearchParams({revision:built.revision!}));assert.ok(graph.nodes.some(node=>node.name==='visible'));assert.ok(!graph.nodes.some(node=>node.name==='ignored'));
 await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['REQUIREMENTS.md','visible.ts']}});
 assert.equal((await index.status('p')).state,'stale');
 const project=(await f.store.project('p'))!,binding=await bindProject('p',project.canonicalRoot);
 assert.equal((await inspectProjectSources(binding,'p',undefined,project.inventoryPolicy)).sources.find(row=>row.id==='requirements')!.status,'excluded');
 await assert.rejects(readProjectSource(binding,'requirements',project.inventoryPolicy),{code:'SOURCE_UNAVAILABLE'});
});

test('isolated engine corpus projection is a stricter subset of F28 read authority',async t=>{
 const f=await m2Fixture(t),corpus=JSON.parse(await readFile(new URL('../fixtures/func_g02/corpus.json',import.meta.url),'utf8'));
 const files=Object.entries(corpus.files).map(([path,content])=>({path,content:content as string}));
 for(const file of files){const path=join(f.root,file.path);await mkdir(join(path,'..'),{recursive:true});await writeFile(path,file.content);}
 await writeFile(join(f.root,'.env'),'API_KEY=synthetic_inventory_canary');
 const project=(await f.store.project('p'))!,inventory=inventoryForProject(project),snapshot=await inventory.snapshot(project);
 for(const file of files){const entry=snapshot.entries.find(row=>row.relativePath===file.path)!;assert.ok(entry?.access.readable,file.path);assert.equal((await inventory.read(project,{path:file.path,revision:entry.revision})).text,file.content);}
 assert.equal(snapshot.entries.find(row=>row.relativePath==='.env')?.access.readable,false);
 await assert.rejects(inventory.read(project,{path:'.env'}),{code:'INVENTORY_SOURCE_FORBIDDEN'});
 await assert.rejects(access(join(f.root,'CONFIG_EXECUTED')));
});
