import assert from 'node:assert/strict';
import { mkdtemp,rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join,resolve,dirname,basename } from 'node:path';
import { randomUUID } from 'node:crypto';
import { openLocalStore } from '../../apps/local-service/src/storage/local-store.mts';
import { bindProject } from '../../apps/local-service/src/adapters/project-sources.ts';
import { taskManagerCommand } from '../../apps/local-service/src/task-manager/service.mts';
import { newM2Task } from '../../packages/contracts/issues/task-profile.ts';

export async function m2Fixture(t:{after(fn:()=>Promise<void>):void}){
  const cleanup:Array<()=>Promise<void>>=[];
  const scratch=resolve(tmpdir()),root=await mkdtemp(join(scratch,'paos-m2-'));
  const pin=await bindProject('p',root),store=await openLocalStore({databasePath:join(root,'state.sqlite')});
  await store.registerProject({id:'p',keyPrefix:'PAOS',canonicalRoot:pin.workspaceRoot,rootIdentity:pin.directoryIdentity,authorityMode:'sql'});
  t.after(async()=>{for(const fn of cleanup)await fn();await store.close();const target=resolve(root);assert.equal(dirname(target),scratch);assert.ok(basename(target).startsWith('paos-m2-'));await rm(target,{recursive:true,force:true});});
  const command=(payload:Record<string,any>)=>taskManagerCommand(store,'p','local-user',{expectedAuthorityEpoch:1,idempotencyKey:randomUUID(),...payload});
  const create=async(title='Task',extra={})=>{const task={...newM2Task('p',randomUUID(),title,'local-user'),...extra};await command({action:'save',task,expectedRevision:0});return (await store.get('p',task.id))!;};
  const ready=async(title='Task',extra={})=>{const task=await create(title,{summary:'Scope',technicalValue:'Technical value',productValue:'Product value',
    files:[{relativePath:'fixture.txt',plannedOperation:'create',actualOperation:null}],acceptanceCriteria:['Observed fixture'],estimateSeconds:60,risks:['none'],...extra});
    await command({action:'transition',taskId:task.id,expectedRevision:task.revision,status:'ready',reason:'Prepared'});return (await store.get('p',task.id))!;};
  return {root,store,command,create,ready,beforeClose:(fn:()=>Promise<void>)=>cleanup.push(fn)};
}
