export type RuntimeRoute='codex_app_agent'|'local_api_byok';
type Input=Record<string,unknown>;
export type RuntimeRoutePort={
 connection:{status:()=>unknown;connect:(input:Input)=>Promise<unknown>;disconnect:()=>Promise<unknown>};
 runtime:{snapshot:(input:Input)=>Promise<unknown>;dispatch:(action:string,input:Input)=>Promise<unknown>};
};
function fail(code:string):never {throw Object.assign(new Error('The selected runtime route is unavailable.'),{code});}
function object(value:unknown):Input {if(!value||typeof value!=='object'||Array.isArray(value))fail('AUTH_ROUTE_INPUT_INVALID');return value as Input;}
/** One queue owns route admission and dispatch across both gateways. Neither route falls back to the other.
 * drain() observes queued work; the owning service must first stop admitting HTTP requests before final teardown. */
export function createRuntimeRouteSelector(options:{app:RuntimeRoutePort;api:RuntimeRoutePort;assertProfile:()=>Promise<void>;
 beforeApiConnect:(input:Input)=>Promise<void>;assertNoForeignUnresolved:(route:RuntimeRoute)=>Promise<void>}) {
 let route:RuntimeRoute='codex_app_agent',engaged=false;let queue:Promise<void>=Promise.resolve();
 const selected=()=>route==='codex_app_agent'?options.app:options.api;
 function serial<T>(operation:()=>Promise<T>):Promise<T>{const pending=queue.then(operation);queue=pending.then(()=>{},()=>{});return pending;}
 function status():Input {const state=selected().connection.status();return {...(state&&typeof state==='object'&&!Array.isArray(state)?state as Input:{}),route};}
 const connection={status,
  connect:(value:unknown)=>serial(async()=>{
   const data=object(value);
   if(Object.keys(data).some(key=>!['route','connectionId','apiKey','remember'].includes(key)))fail('AUTH_ROUTE_INPUT_INVALID');
   const requested=data.route??(Object.hasOwn(data,'apiKey')?'local_api_byok':'codex_app_agent');
   if(requested!=='codex_app_agent'&&requested!=='local_api_byok')fail('AUTH_ROUTE_UNSUPPORTED');
   if(requested==='codex_app_agent'&&(Object.hasOwn(data,'apiKey')||Object.hasOwn(data,'remember')))fail('AUTH_ROUTE_INPUT_INVALID');
   if(data.connectionId!==undefined&&(typeof data.connectionId!=='string'||!data.connectionId.trim()||data.connectionId.length>100))fail('AUTH_ROUTE_INPUT_INVALID');
   if(data.apiKey!==undefined&&(typeof data.apiKey!=='string'||!data.apiKey.trim()||data.apiKey.length>8192))fail('AUTH_ROUTE_INPUT_INVALID');
   if(data.remember!==undefined&&typeof data.remember!=='boolean')fail('AUTH_ROUTE_INPUT_INVALID');
   if(engaged&&route!==requested)fail('ROUTE_DISCONNECT_REQUIRED');
   await options.assertProfile();await options.assertNoForeignUnresolved(requested);
   const {route:ignored,...payload}=data;
   if(requested==='local_api_byok')await options.beforeApiConnect(payload);
   const port=requested==='codex_app_agent'?options.app:options.api;
   const result=await port.connection.connect(payload);route=requested;engaged=true;return result;
  }),
  disconnect:()=>serial(async()=>{await options.assertProfile();const result=await selected().connection.disconnect();engaged=false;return result;})};
 const runtime={snapshot:(input:Input)=>serial(async()=>selected().runtime.snapshot(input)),
  dispatch:(action:string,input:Input)=>serial(async()=>{
   await options.assertProfile();if(action==='bindings'||action==='send')await options.assertNoForeignUnresolved(route);
   return selected().runtime.dispatch(action,input);
  })};
 return {connection,runtime,drain:async()=>{await queue;}};
}
