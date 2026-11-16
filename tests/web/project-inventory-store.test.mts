import {test} from 'node:test';
import assert from 'node:assert/strict';
import {m2Fixture} from './m2-fixture.mts';
import {openLocalStore} from '../../apps/local-service/src/storage/local-store.mts';
import {join} from 'node:path';

test('inventory policy persists through restart with CAS and does not become a task or document',async t=>{
 const f=await m2Fixture(t),namespace='project_inventory_policy_v1' as const;
 const before=await f.store.projectEntities('p');assert.equal(await f.store.readProjectState('p',namespace),null);
 const value={schemaVersion:'paos_inventory_policy_v1',policy:{include:['src/**'],exclude:['generated/**'],respectGitignore:true}};
 const saved=await f.store.writeProjectState('p',namespace,0,value);assert.equal(saved.version,1);
 await assert.rejects(f.store.writeProjectState('p',namespace,0,value),{code:'PROJECT_STATE_CONFLICT'});
 assert.deepEqual((await f.store.project('p'))!.inventoryPolicy,value.policy);
 assert.deepEqual(await f.store.projectEntities('p'),before);
 await f.store.close();const reopened=await openLocalStore({databasePath:join(f.root,'state.sqlite')});
 try{assert.deepEqual(await reopened.readProjectState('p',namespace),saved);}finally{await reopened.close();}
});

test('profile state rejects malformed inventory authority and foreign project namespaces',async t=>{
 const f=await m2Fixture(t),namespace='project_inventory_policy_v1' as const;
 await assert.rejects(f.store.writeProjectState('p',namespace,0,{schemaVersion:'wrong',policy:{include:['../outside']}}),{code:'PROJECT_STATE_INVALID'});
 assert.equal(await f.store.readProjectState('p',namespace),null);
 await assert.rejects(f.store.readProjectState('unknown',namespace),{code:'PROJECT_NOT_FOUND'});
 await assert.rejects(f.store.writeProjectState('p','arbitrary_meta' as any,0,{schemaVersion:'any'}),{code:'PROJECT_STATE_INVALID'});
});
