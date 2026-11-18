import {test} from 'node:test';
import assert from 'node:assert/strict';
import {capabilityLabel,runtimeConnectionState,graphCapabilityState,databaseCapabilityState} from '../../apps/web/src/ui/capability.ts';

test('capability labels distinguish unavailable, unsupported, pending and evidence levels in both languages',()=>{
 const states=['not_configured','unsupported','unavailable','indexing','partial','stale','failed','available','staged','connected','qualified','accepted'];
 for(const locale of ['ru','en'] as const){const labels=states.map(state=>capabilityLabel(state,locale));assert.equal(new Set(labels).size,states.length);assert.equal(capabilityLabel('unknown',locale),capabilityLabel('unavailable',locale));assert.equal(capabilityLabel('__proto__',locale),capabilityLabel('unavailable',locale));assert.ok(labels.every(label=>label.length>4));}
});
test('global worker connection never attests per-binding qualification from endpoint, model or native flags',()=>{
 const connected={route:'codex_app_agent' as const,state:'connected',verified:true,nativeSandbox:true,modelAccess:'observed'};
 assert.equal(runtimeConnectionState(null),'not_configured');
 assert.equal(runtimeConnectionState(connected),'connected');
 assert.equal(runtimeConnectionState({...connected,capabilities:{executionConfigured:true,nativeSandbox:false}}),'connected');
 assert.equal(runtimeConnectionState({...connected,capabilities:{executionConfigured:true,nativeSandbox:true}}),'connected');
 assert.equal(runtimeConnectionState({...connected,verified:false,capabilities:{executionConfigured:true,nativeSandbox:true}}),'unavailable');
 assert.equal(runtimeConnectionState({...connected,state:'disconnected',capabilities:{executionConfigured:true,nativeSandbox:true}}),'unavailable');
});
test('empty or unsupported graph and missing schema never become fully analyzed or ready',()=>{
 assert.equal(graphCapabilityState(undefined),'not_configured');
 assert.equal(graphCapabilityState({state:'unavailable',limitations:['parser_unavailable']}),'unavailable');
 assert.equal(graphCapabilityState({state:'stale',limitations:[]}),'stale');
 assert.equal(graphCapabilityState({state:'fresh',counts:{files:0,nodes:0,edges:0},coverage:[{relativePath:'app.py',status:'unsupported'}],limitations:[]}),'unsupported');
 assert.equal(graphCapabilityState({state:'fresh',counts:{files:0,nodes:0,edges:0},coverage:[],limitations:[]}),'partial');
 for(const state of ['unselected','selected','ready','partial','stale','unavailable'] as const)assert.equal(databaseCapabilityState({state} as any),state==='ready'?'available':['unselected','selected'].includes(state)?'not_configured':state);
});
