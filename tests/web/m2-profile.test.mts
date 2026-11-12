import assert from 'node:assert/strict';
import { test } from 'node:test';
import { randomUUID } from 'node:crypto';
import { newM2Task, decodeTaskProfile, validateIssueGraph } from '../../packages/contracts/issues/task-profile.ts';

test('M2 profile round-trips hierarchy and preserves strict legacy rejection', () => {
  const task = newM2Task('project', randomUUID(), 'Bug', 'local-user');
  task.key = 'PAOS-1'; task.type = 'bug'; task.components = ['DB']; task.affectsVersions = ['v12']; task.fixVersions = ['v13'];
  assert.deepEqual(decodeTaskProfile(JSON.parse(JSON.stringify(task))), task);
  assert.throws(() => decodeTaskProfile({...task,schemaVersion:'m1_task_profile_v1'}), {code:'INVALID_M1_TASK_PROFILE'});
});

test('hierarchy rejects invalid nesting and terminal parent with unfinished children', () => {
  const epic = newM2Task('p', randomUUID(), 'Epic','u'); epic.key='PAOS-1'; epic.type='epic';
  const child = newM2Task('p',randomUUID(),'Child','u'); child.key='PAOS-2'; child.parentId=epic.id;
  validateIssueGraph([epic,child],[]);
  assert.throws(()=>validateIssueGraph([epic,{...child,type:'sub_task'}],[]),{code:'INVALID_PARENT_TYPE'});
  assert.throws(()=>validateIssueGraph([{...epic,status:'done'},child],[]),{code:'CHILDREN_INCOMPLETE'});
});

test('structured M2 references reject credentials and traversal while preserving unknown original dates',()=>{
  const task=newM2Task('p',randomUUID(),'Fixture','u');task.key='PAOS-1';
  const artifact={type:'research',reference:'https://user:password@example.com/private',revision:null,provenance:'user',availability:'unverified'};
  for(const reference of [artifact.reference,'javascript:alert(1)','../outside.md','C:\\private.txt','CON.txt'])
    assert.throws(()=>decodeTaskProfile({...task,artifacts:[{...artifact,reference}]}),{code:'INVALID_ARTIFACT'});
  assert.throws(()=>decodeTaskProfile({...task,createdAt:'2026-02-30T12:00:00Z'}),{code:'INVALID_CREATED_AT'});
  assert.throws(()=>decodeTaskProfile({...task,fileContexts:[{relativePath:'../outside.txt',revision:null,context:'line 1'}]}),{code:'INVALID_FILE_CONTEXT'});
  assert.equal((decodeTaskProfile({...task,createdAt:null}) as any).createdAt,null);
});
