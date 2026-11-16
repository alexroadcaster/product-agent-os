import test from 'node:test';import assert from 'node:assert/strict';import {writeFile} from 'node:fs/promises';import {join} from 'node:path';import {createHash,randomUUID} from 'node:crypto';
import {g03Fixture} from './project-g03-fixture.mts';import {newM2Task} from '../../packages/contracts/issues/task-profile.ts';
import {resolveTaskReference} from '../../apps/local-service/src/task-manager/service.mts';
import {createArtifactCatalog} from '../../apps/local-service/src/artifacts/service.mts';import {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';
async function revokeOnCapture(f:Awaited<ReturnType<typeof g03Fixture>>,exclude:string[],action:()=>Promise<void>){const project=f.store.project;let crossed=false;f.store.project=async id=>{const value=await project(id);if(!crossed&&id==='p'){crossed=true;await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude}});}return value;};try{await action();assert.equal(crossed,true);}finally{f.store.project=project;}}
test('task reference cannot return plaintext after policy revocation during its read',async t=>{
 const f=await g03Fixture(t),content='export const visible=1;\n',task={...newM2Task('p',randomUUID(),'Reference race','local-user'),fileContexts:[{relativePath:'main.ts',revision:createHash('sha256').update(content).digest('hex'),context:'explicit source'}]};
 await f.store.write({projectId:'p',actorId:'fixture',idempotencyKey:randomUUID(),expectedAuthorityEpoch:1,changes:[{expectedRevision:0,entity:{id:task.id,kind:'task',data:task}}]});
 await revokeOnCapture(f,['main.ts'],async()=>{const result=await resolveTaskReference(f.store,'p',{taskId:task.id,relativePath:'main.ts'});assert.equal(result.availability,'unavailable');assert.equal(result.content,undefined);});
});
test('artifact body and cursor previews cannot publish captured revoked policy',async t=>{
 for(const mode of ['body','cursor']){const f=await g03Fixture(t);await writeFile(join(f.workspace,'a.md'),'# A');await writeFile(join(f.workspace,'b.md'),'# B');const catalog=createArtifactCatalog(f.store),page=await catalog.catalog('p',new URLSearchParams({kind:'documents',limit:'1'}));assert.ok(page.nextCursor);
  await revokeOnCapture(f,['*.md'],async()=>{if(mode==='body'){const result=await catalog.read('p',page.items[0].id,page.items[0].source.version);assert.equal(result.state,'unavailable');assert.equal(result.body,null);}else await assert.rejects(catalog.catalog('p',new URLSearchParams({kind:'documents',limit:'1',cursor:page.nextCursor!})),{code:'PROJECT_SCOPE_STALE'});});
 }
});
test('graph plaintext and direct rebuild publication recheck registry even without scan orchestration',async t=>{
 for(const mode of ['source','build']){const f=await g03Fixture(t),index=createCodeIndex(f.store),built=await index.rebuild('p');const graph=await index.graph('p',new URLSearchParams({revision:built.revision!})),file=graph.nodes.find(node=>node.kind==='file')!;
  if(mode==='source')await revokeOnCapture(f,['main.ts'],async()=>{await assert.rejects(index.source('p',new URLSearchParams({revision:built.revision!,fileId:file.id})),{code:'PROJECT_SCOPE_STALE'});});
  else {await writeFile(join(f.workspace,'main.ts'),'export const changed=2;\n');await assert.rejects(index.rebuild('p',{publicationGuard:async()=>{await f.store.writeProjectState('p','project_inventory_policy_v1',0,{schemaVersion:'paos_inventory_policy_v1',policy:{exclude:['main.ts']}});}}),{code:'PROJECT_SCOPE_STALE'});const status=await index.status('p');assert.equal(status.revision,built.revision);assert.equal(status.state,'stale');}
 }
});
