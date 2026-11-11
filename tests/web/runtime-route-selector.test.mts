import assert from 'node:assert/strict';
import {test} from 'node:test';
import {createRuntimeRouteSelector} from '../../apps/local-service/src/runtime/route-selector.ts';

function fixture(){
 const calls:string[]=[];let apiConnect=async()=>{};let foreign=async(_route:string)=>{};
 const port=(name:string)=>({connection:{status:()=>({verified:false,state:'disconnected'}),connect:async(_input:Record<string,unknown>)=>{calls.push(`${name}:connect`);if(name==='api')await apiConnect();return {name};},disconnect:async()=>{calls.push(`${name}:disconnect`);return {name};}},
  runtime:{snapshot:async(_input:Record<string,unknown>)=>({name}),dispatch:async(action:string,_input:Record<string,unknown>)=>{calls.push(`${name}:${action}`);return {name};}}});
 const selector=createRuntimeRouteSelector({app:port('app'),api:port('api'),assertProfile:async()=>{},beforeApiConnect:async()=>{calls.push('api:admission');},assertNoForeignUnresolved:route=>foreign(route)});
 return {selector,calls,setApi:(next:()=>Promise<void>)=>{apiConnect=next;},setForeign:(next:(route:string)=>Promise<void>)=>{foreign=next;}};
}
test('a delayed API connect reserves the selector before a simultaneous App connection can enter',async()=>{
 const f=fixture(),gate=Promise.withResolvers<void>(),entered=Promise.withResolvers<void>();
 f.setApi(async()=>{entered.resolve();await gate.promise;});
 const first=f.selector.connection.connect({route:'local_api_byok',connectionId:'fixture',apiKey:'synthetic'});await entered.promise;
 const second=f.selector.connection.connect({route:'codex_app_agent'});const rejected=assert.rejects(second,{code:'ROUTE_DISCONNECT_REQUIRED'});
 gate.resolve();await first;await rejected;assert.deepEqual(f.calls,['api:admission','api:connect']);assert.equal(f.selector.connection.status().route,'local_api_byok');
});

test('disconnect and following runtime operations wait for the pending connection before switching routes',async()=>{
 const f=fixture(),gate=Promise.withResolvers<void>(),entered=Promise.withResolvers<void>();
 f.setApi(async()=>{entered.resolve();await gate.promise;});
 const connecting=f.selector.connection.connect({route:'local_api_byok',apiKey:'synthetic'});await entered.promise;
 const disconnecting=f.selector.connection.disconnect();const next=f.selector.connection.connect({route:'codex_app_agent'});
 const dispatch=f.selector.runtime.dispatch('bindings',{projectId:'p',sessionId:'s'});gate.resolve();
 await Promise.all([connecting,disconnecting,next,dispatch]);await f.selector.drain();
 assert.deepEqual(f.calls,['api:admission','api:connect','api:disconnect','app:connect','app:bindings']);
 assert.equal(f.selector.connection.status().route,'codex_app_agent');
});

test('foreign unresolved guards fence both routes on connection and are refreshed before new bindings or sends',async()=>{
 for(const route of ['codex_app_agent','local_api_byok'] as const){
  const f=fixture();f.setForeign(async selected=>{assert.equal(selected,route);throw Object.assign(new Error('fixture unresolved'),{code:'FOREIGN_UNRESOLVED'});});
  await assert.rejects(f.selector.connection.connect({route}),{code:'FOREIGN_UNRESOLVED'});assert.equal(f.calls.length,0);
 }
 const f=fixture();await f.selector.connection.connect({route:'codex_app_agent'});
 f.setForeign(async()=>{throw Object.assign(new Error('new unresolved'),{code:'FOREIGN_UNRESOLVED'});});
 for(const action of ['bindings','send'])await assert.rejects(f.selector.runtime.dispatch(action,{projectId:'p'}),{code:'FOREIGN_UNRESOLVED'});
 assert.deepEqual(await f.selector.runtime.dispatch('interrupt',{projectId:'p'}),{name:'app'});
 assert.deepEqual(f.calls,['app:connect','app:interrupt']);
});

test('API failure and mixed payloads never silently activate App or transfer API credentials to it',async()=>{
 const f=fixture();f.setApi(async()=>{throw Object.assign(new Error('fixture API unavailable'),{code:'API_UNAVAILABLE'});});
 await assert.rejects(f.selector.connection.connect({apiKey:'synthetic'}),{code:'API_UNAVAILABLE'});
 assert.equal(f.selector.connection.status().route,'codex_app_agent');assert.deepEqual(f.calls,['api:admission','api:connect']);
 for(const request of [{route:'codex_app_agent',apiKey:'synthetic'},{route:'codex_app_agent',remember:false},{route:'unknown'},{route:'codex_app_agent',unknown:true}])
  await assert.rejects(f.selector.connection.connect(request));
 assert.deepEqual(f.calls,['api:admission','api:connect']);
 await f.selector.connection.connect({route:'codex_app_agent'});assert.equal(f.calls.at(-1),'app:connect');
});
