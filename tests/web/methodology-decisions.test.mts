import assert from 'node:assert/strict';
import {test} from 'node:test';
import {mkdir,writeFile} from 'node:fs/promises';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {createMethodologyDecisions} from '../../apps/local-service/src/project-analysis/methodology-decisions.mts';
import {openLocalStore,restoreLocalBackup} from '../../apps/local-service/src/storage/local-store.mts';
import {m2Fixture} from './m2-fixture.mts';

test('methodology decisions preserve history, compare revisions and survive verified backup restore',async t=>{
  const f=await m2Fixture(t),service=createMethodologyDecisions(f.store);
  const task=await f.ready('Evidence scope',{acceptanceCriteria:['Observed behavior','Second behavior']});
  await writeFile(join(f.root,'fixture.txt'),'original bytes');
  const before=await service.get('p',task.id);
  assert.equal(before.status,'unknown');
  assert.equal(before.revision,0);
  const input={expectedRevision:0,taskRevision:task.revision,scopeDigest:before.scopeDigest,
    idempotencyKey:'accept-gap',disposition:'accepted_gap',criterionId:'AC-1',reason:'Observed through a manual check'};
  const results=await Promise.allSettled([
    service.save('p',task.id,'local-user',input),
    service.save('p',task.id,'other-user',{...input,idempotencyKey:'other',disposition:'review_required',criterionId:null}),
  ]);
  assert.equal(results.filter(result=>result.status==='fulfilled').length,1);
  const current=await service.get('p',task.id);
  assert.equal(current.status,'current');
  assert.equal(current.history.length,1);
  if(results[0].status==='fulfilled'){
    assert.deepEqual(await service.save('p',task.id,'local-user',input),current);
    await assert.rejects(service.save('p',task.id,'local-user',{...input,reason:'Different intent'}),{code:'IDEMPOTENCY_CONFLICT'});
  }
  await assert.rejects(service.save('p',task.id,'local-user',{...input,expectedRevision:1,idempotencyKey:'secret',
    reason:'Bearer abcdefghijklmnop'}),{code:'METHODOLOGY_DECISION_INVALID'});
  const second=await service.save('p',task.id,'local-user',{...input,expectedRevision:1,idempotencyKey:'next',criterionId:'AC-2'});
  assert.equal(second.history.length,2);
  assert.deepEqual(second.history[0],current.history[0]);
  assert.equal(second.history[1].actorId,'local-user');
  assert.equal((await f.store.get('p',task.id))?.revision,task.revision);
  assert.equal((await f.store.get('p',task.id))?.status,task.status);
  await assert.rejects(service.get('other',task.id),{code:'TASK_NOT_FOUND'});

  const backupRoot=join(f.root,'backups');await mkdir(backupRoot);
  const backup=await f.store.backup(backupRoot);
  const restoredPath=join(f.root,'restored.sqlite');
  await restoreLocalBackup(backup.directory,restoredPath);
  const restored=await openLocalStore({databasePath:restoredPath});
  try{
    const observed=await createMethodologyDecisions(restored).get('p',task.id);
    assert.equal(observed.status,'stale');
    assert.deepEqual(observed.history,second.history);
    assert.notEqual(observed.scopeDigest,second.scopeDigest);
  }finally{await restored.close();}
  await writeFile(join(f.root,'fixture.txt'),'concurrent source edit');
  const drift=await service.get('p',task.id);
  assert.equal(drift.status,'stale');
  assert.deepEqual(drift.history,second.history);
  await assert.rejects(service.save('p',task.id,'local-user',{...input,expectedRevision:2,idempotencyKey:'stale'}),{code:'METHODOLOGY_DECISION_STALE'});
});

test('an older methodology reader preserves an unsupported record while ordinary task edits still work',async t=>{
  const f=await m2Fixture(t),service=createMethodologyDecisions(f.store);
  const task=await f.create('Existing task',{acceptanceCriteria:['Observed criterion']});
  const id='methodology-decision-'+createHash('sha256').update(JSON.stringify(['p',task.id])).digest('hex');
  const future={category:'methodology_decision',schemaVersion:'paos_methodology_decision_record_v2',
    taskId:task.id,history:[{newOwnerRecord:'preserve exactly'}]};
  await f.store.write({projectId:'p',actorId:'fixture',expectedAuthorityEpoch:1,idempotencyKey:'future-schema',changes:[{
    expectedRevision:0,entity:{id,kind:'settings',data:future},
  }]});
  const blocked=await service.get('p',task.id);
  assert.equal(blocked.status,'unsupported');
  await assert.rejects(service.save('p',task.id,'local-user',{expectedRevision:1,taskRevision:task.revision,
    scopeDigest:blocked.scopeDigest,idempotencyKey:'old-client',disposition:'review_required',criterionId:null,reason:'Review'}),
    {code:'METHODOLOGY_DECISION_UNSUPPORTED'});
  await f.command({action:'save',task:{...task.data,title:'Edited by ordinary client'},expectedRevision:task.revision});
  assert.deepEqual((await f.store.get('p',id))?.data,future);
});
