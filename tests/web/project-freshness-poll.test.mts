import test from 'node:test';import assert from 'node:assert/strict';
import {startProjectFreshnessPolling} from '../../apps/web/src/api/project-freshness.ts';
import {sameSourceRevision,sameProjectFreshness,type ProjectFreshness} from '../../packages/contracts/project-freshness.ts';
const base:ProjectFreshness={schemaVersion:'paos_project_freshness_v1',projectId:'p',rootIdentity:'root',generation:'g',throughSeq:1,scanVersion:1,policyVersion:0};
test('freshness polling has one lane and disposal aborts and rejects late responses',async()=>{
 let resolve!:(value:ProjectFreshness)=>void,signal!:AbortSignal,reads=0,scheduled=0;const published:ProjectFreshness[]=[];
 const stop=startProjectFreshnessPolling({projectId:'p',read:s=>{signal=s;reads++;return new Promise(done=>resolve=done);},publish:v=>published.push(v),error:()=>assert.fail('unexpected error'),schedule:()=>{scheduled++;return 1;}});
 assert.equal(reads,1);assert.equal(scheduled,0);stop();assert.ok(signal.aborted);resolve(base);await new Promise(done=>setImmediate(done));assert.deepEqual(published,[]);assert.equal(scheduled,0);
});
test('polling rejects foreign scopes and clears scheduled work on unmount',async()=>{
 let next:(()=>void)|undefined,cancelled=0;const errors:unknown[]=[],published:ProjectFreshness[]=[];
 const stop=startProjectFreshnessPolling({projectId:'p',read:async()=>({...base,projectId:'other'}),publish:v=>published.push(v),error:v=>errors.push(v),schedule:fn=>{next=fn;return 7;},cancel:id=>{assert.equal(id,7);cancelled++;}});
 await new Promise(done=>setImmediate(done));assert.equal(errors.length,1);assert.deepEqual(published,[]);assert.ok(next);stop();assert.equal(cancelled,1);
});
test('common provenance invalidates project/root/policy/inventory and profile generations independently',()=>{
 const provenance={projectId:'p',rootIdentity:'r',policyVersion:'v',inventoryRevision:'i'};assert.ok(sameSourceRevision(provenance,{...provenance}));
 for(const key of Object.keys(provenance))assert.equal(sameSourceRevision(provenance,{...provenance,[key]:'changed'}),false);
 assert.ok(sameProjectFreshness(base,{...base}));for(const key of ['projectId','rootIdentity','generation','throughSeq','scanVersion','policyVersion'])assert.equal(sameProjectFreshness(base,{...base,[key]:typeof(base as any)[key]==='number'?2:'changed'}),false);
});
