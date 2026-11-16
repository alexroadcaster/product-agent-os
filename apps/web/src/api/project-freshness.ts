import type {ProjectFreshness} from '../../../../packages/contracts/project-freshness.ts';

/** A single cheap request in flight. Cleanup cancels transport, timer and late publication. */
export function startProjectFreshnessPolling(options:{projectId:string;read:(signal:AbortSignal)=>Promise<ProjectFreshness>;publish:(value:ProjectFreshness)=>void;error:(cause:unknown)=>void;schedule?:(callback:()=>void,delay:number)=>unknown;cancel?:(timer:unknown)=>void}){
 const controller=new AbortController(),schedule=options.schedule??((fn,delay)=>setTimeout(fn,delay)),cancel=options.cancel??(timer=>clearTimeout(timer as ReturnType<typeof setTimeout>));let timer:unknown;
 async function tick(){try{const value=await options.read(controller.signal);if(!controller.signal.aborted){if(value.schemaVersion!=='paos_project_freshness_v1'||value.projectId!==options.projectId)throw Error('FRESHNESS_SCOPE_MISMATCH');options.publish(value);}}catch(cause){if(!controller.signal.aborted)options.error(cause);}finally{if(!controller.signal.aborted)timer=schedule(()=>void tick(),2000);}}
 void tick();return()=>{controller.abort();if(timer!==undefined)cancel(timer);};
}
