import {randomUUID,createHash} from 'node:crypto';
import type {LocalStore,Project} from '../storage/local-store.mts';
import {inventoryForProject} from '../code-index/sources.mts';
import {safeVisibleValue} from '../redaction/persisted.mts';
import type {InventorySnapshot} from '../../../../packages/contracts/project-inventory.ts';
import type {ProjectScan,ProjectScanStage,ProjectScanStageKind,ProjectScanView,ProjectScanCapabilities} from '../../../../packages/contracts/project-scan.ts';

export type ScanAnalyzerResult={state?:'completed'|'partial'|'unavailable';counts?:Record<string,number|null>;reasons?:string[];data?:Record<string,unknown>};
export type ScanAnalyzerContext={project:Project;inventory:InventorySnapshot;signal:AbortSignal;publicationGuard:()=>Promise<void>;canPublish:()=>boolean;onProgress:(completed:number,total:number)=>Promise<void>};
export type ScanAnalyzer=(context:ScanAnalyzerContext)=>Promise<ScanAnalyzerResult>;
export type ScanLimits={concurrency:number;milliseconds:number;stageMilliseconds:number;resultBytes:number;queued:number};
type AnalysisObservation={scanId:string;stage:ProjectScanStage};
type RecordState={schemaVersion:'paos_project_scan_record_v1';latest:ProjectScan|null;lastSuccessful:ProjectScan|null;lastAnalysis?:AnalysisObservation;requests:{id:string;digest:string;scanId:string}[]};
type Saved={version:number;value:RecordState};
function fail(code:string):never{throw Object.assign(new Error(code),{code});}
const code=(error:unknown)=>typeof(error as any)?.code==='string'?(error as any).code:'PROJECT_SCAN_FAILED';
const hash=(value:unknown)=>createHash('sha256').update(JSON.stringify(value)).digest('hex');
const live=(scan:ProjectScan|null)=>scan&&['queued','running'].includes(scan.state);
const defaults:ScanLimits={concurrency:1,milliseconds:60000,stageMilliseconds:30000,resultBytes:256*1024,queued:20};
const stageKinds:ProjectScanStageKind[]=['inventory','documents','code','analysis'];
const blank=():RecordState=>({schemaVersion:'paos_project_scan_record_v1',latest:null,lastSuccessful:null,requests:[]});
function analysisObservation(scan:ProjectScan|null):AnalysisObservation|undefined{
 const stage=scan?.stages.find(item=>item.kind==='analysis'&&['completed','partial','failed','unavailable'].includes(item.state));
 return scan&&stage?{scanId:scan.scanId,stage}:undefined;
}
/** Persisted JSON is evidence only after its version, scope and state shape validate. */
function validScan(scan:unknown,projectId:string):boolean{
 if(scan===null)return true;
 const value=scan as ProjectScan;
 return Boolean(value&&typeof value==='object'&&value.schemaVersion==='paos_project_scan_v1'&&value.projectId===projectId
  &&typeof value.scanId==='string'&&/^[a-f0-9-]{36}$/.test(value.scanId)&&Number.isSafeInteger(value.attempt)&&value.attempt>0
  &&typeof value.rootIdentity==='string'&&value.rootIdentity.length>0&&typeof value.policyVersion==='string'&&value.policyVersion.length>0
  &&['queued','running','completed','partial','cancelled','interrupted','failed','recovery_required'].includes(value.state)
  &&(value.inventoryRevision===null||typeof value.inventoryRevision==='string'&&/^[a-f0-9]{64}$/.test(value.inventoryRevision))
  &&(value.requestedRevision===null||typeof value.requestedRevision==='string'&&/^[a-f0-9]{64}$/.test(value.requestedRevision))
  &&typeof value.startedAt==='string'&&Number.isFinite(Date.parse(value.startedAt))&&typeof value.updatedAt==='string'&&Number.isFinite(Date.parse(value.updatedAt))
  &&Array.isArray(value.reasons)&&value.reasons.length<=128&&value.reasons.every(reason=>typeof reason==='string'&&reason.length<=512)
  &&Array.isArray(value.stages)&&value.stages.length>=1&&value.stages.length<=6&&value.stages[0]?.kind==='inventory'&&new Set(value.stages.map(stage=>stage.kind)).size===value.stages.length
  &&value.stages.every(stage=>stage&&['inventory','documents','code','analysis','schema','code_database'].includes(stage.kind)&&['pending','running','completed','partial','unavailable','failed','cancelled'].includes(stage.state)&&Array.isArray(stage.reasons)&&stage.reasons.length<=128&&stage.reasons.every(reason=>typeof reason==='string'&&reason.length<=512)));
}

/** Profile-owned durable orchestration. Adapters must honor signal and the final publication guard. */
export function createProjectScans(options:{store:LocalStore;analyzers?:Partial<Record<Exclude<ProjectScanStageKind,'inventory'>,ScanAnalyzer>>;limits?:Partial<ScanLimits>}){
 const {store}=options,analyzers=options.analyzers??{},limits={...defaults,...options.limits};
 const stages:ProjectScanStageKind[]=[...stageKinds,...(['schema','code_database'] as const).filter(kind=>Boolean(analyzers[kind]))];
 for(const [key,value] of Object.entries(limits))if(!Number.isSafeInteger(value)||value<1||value>defaults[key as keyof ScanLimits])fail('PROJECT_SCAN_LIMIT_INVALID');
 const capabilities:ProjectScanCapabilities={inventory:true,documents:Boolean(analyzers.documents),code:Boolean(analyzers.code),analysis:Boolean(analyzers.analysis),schema:Boolean(analyzers.schema),code_database:Boolean(analyzers.code_database)};
 const tails=new Map<string,Promise<unknown>>(),controllers=new Map<string,AbortController>(),ownedIds=new Set<string>(),work=new Set<Promise<void>>(),queue:{projectId:string;scanId:string}[]=[];
 let closed=false,pumping=false;
 const stamp=()=>new Date().toISOString();
 async function read(projectId:string):Promise<Saved>{
  const saved=await store.readProjectState(projectId,'project_scan_v1');if(!saved)return {version:0,value:blank()};const value=saved.value as unknown as RecordState;
  if(value.schemaVersion!=='paos_project_scan_record_v1'||!Array.isArray(value.requests)||value.requests.length>32
   ||!value.requests.every(item=>item&&typeof item.id==='string'&&item.id.length<=160&&typeof item.digest==='string'&&/^[a-f0-9]{64}$/.test(item.digest)&&typeof item.scanId==='string')
   ||!validScan(value.latest,projectId)||!validScan(value.lastSuccessful,projectId)
   ||value.lastAnalysis!==undefined&&(!value.lastAnalysis||!/^[a-f0-9-]{36}$/.test(value.lastAnalysis.scanId)
      ||value.lastAnalysis.stage?.kind!=='analysis'||!['completed','partial','failed','unavailable'].includes(value.lastAnalysis.stage.state))
   ||value.lastSuccessful&&!['completed','partial'].includes(value.lastSuccessful.state))fail('PROJECT_SCAN_STATE_UNAVAILABLE');
  return {version:saved.version,value};
 }
 async function save(projectId:string,saved:Saved){return await store.writeProjectState(projectId,'project_scan_v1',saved.version,saved.value as unknown as Record<string,unknown>) as unknown as Saved;}
 const serial=<T,>(projectId:string,fn:()=>Promise<T>):Promise<T>=>{const result=(tails.get(projectId)??Promise.resolve()).then(fn);tails.set(projectId,result.catch(()=>{}));return result;};
 function view(projectId:string,saved:Saved):ProjectScanView{return {schemaVersion:'paos_project_scan_view_v1',projectId,version:saved.version,latest:saved.value.latest,lastSuccessful:saved.value.lastSuccessful,capabilities:{...capabilities},limits:{...limits}};}
 async function project(projectId:string){const value=await store.project(projectId);if(!value)fail('PROJECT_NOT_FOUND');await inventoryForProject(value).assertProject(value);return value;}
 const ready=(async()=>{
  for(const p of await store.projects()){
   let saved:Saved;try{saved=await read(p.id);}catch(error){if(code(error)==='PROJECT_SCAN_STATE_UNAVAILABLE')continue;throw error;}if(!live(saved.value.latest))continue;
   saved.value.latest={...saved.value.latest!,state:'interrupted',stage:null,updatedAt:stamp(),finishedAt:stamp(),reasons:[...new Set([...saved.value.latest!.reasons,'SERVICE_RESTART_NO_REPLAY'])],stages:saved.value.latest!.stages.map(stage=>stage.state==='running'||stage.state==='pending'?{...stage,state:'cancelled',updatedAt:stamp(),reasons:['SERVICE_RESTART_NO_REPLAY']}:stage)};
   await save(p.id,saved);
  }
 })();
 async function owned(projectId:string,scanId:string,change:(scan:ProjectScan,saved:Saved)=>void){return serial(projectId,async()=>{const saved=await read(projectId),scan=saved.value.latest;if(!scan||scan.scanId!==scanId||!live(scan))fail('PROJECT_SCAN_SUPERSEDED');change(scan,saved);scan.updatedAt=stamp();return save(projectId,saved);});}
 async function guard(projectId:string,scanId:string,controller:AbortController,inventory:InventorySnapshot){
  if(closed||controller.signal.aborted)fail('PROJECT_SCAN_CANCELLED');
  const saved=await read(projectId),scan=saved.value.latest;if(!scan||scan.scanId!==scanId||!live(scan))fail('PROJECT_SCAN_SUPERSEDED');
  const p=await project(projectId);if(p.rootIdentity!==scan.rootIdentity||inventoryForProject(p).policyVersion!==scan.policyVersion)fail('PROJECT_SCAN_SCOPE_STALE');
  const current=await inventoryForProject(p).snapshot(p,{signal:controller.signal});if(current.revision!==inventory.revision)fail('PROJECT_SCAN_SOURCE_STALE');
  if(closed||controller.signal.aborted)fail('PROJECT_SCAN_CANCELLED');
 }
 function awaitAdapter<T>(operation:Promise<T>,controller:AbortController,milliseconds:number):Promise<T>{
  return new Promise<T>((resolve,reject)=>{
   const cancel=()=>{cleanup();reject(controller.signal.reason?.code==='PROJECT_SCAN_TIMEOUT'?controller.signal.reason:Object.assign(new Error('PROJECT_SCAN_CANCELLED'),{code:'PROJECT_SCAN_CANCELLED'}));};
   const timer=setTimeout(()=>{cleanup();const error=Object.assign(new Error('PROJECT_SCAN_TIMEOUT'),{code:'PROJECT_SCAN_TIMEOUT'});controller.abort(error);reject(error);},milliseconds);
   const cleanup=()=>{clearTimeout(timer);controller.signal.removeEventListener('abort',cancel);};
   // Even a pre-aborted adapter promise keeps a rejection handler; cancellation
   // must not become an unrelated unhandled rejection after the job is closed.
   operation.then(value=>{cleanup();resolve(value);},error=>{cleanup();reject(error);});
   if(controller.signal.aborted){cleanup();reject(Object.assign(new Error('PROJECT_SCAN_CANCELLED'),{code:'PROJECT_SCAN_CANCELLED'}));return;}
   controller.signal.addEventListener('abort',cancel,{once:true});
  });
 }
 async function run(projectId:string,scanId:string){
  const controller=new AbortController();controllers.set(scanId,controller);const deadline=Date.now()+limits.milliseconds;
  const jobTimer=setTimeout(()=>controller.abort(Object.assign(new Error('PROJECT_SCAN_TIMEOUT'),{code:'PROJECT_SCAN_TIMEOUT'})),limits.milliseconds);
  try{
   await owned(projectId,scanId,scan=>{scan.state='running';scan.stage='inventory';});
   const p=await project(projectId);let inventory:InventorySnapshot|undefined;
   for(const kind of (await read(projectId)).value.latest!.stages.map(stage=>stage.kind)){
    if(controller.signal.aborted||closed)fail('PROJECT_SCAN_CANCELLED');
    await owned(projectId,scanId,scan=>{scan.stage=kind;const stage=scan.stages.find(item=>item.kind===kind)!;stage.state='running';stage.startedAt=stamp();stage.updatedAt=stamp();});
    let result:ScanAnalyzerResult;
    try{
     if(kind==='inventory'){
      inventory=await awaitAdapter(inventoryForProject(p).snapshot(p,{signal:controller.signal}),controller,Math.min(limits.stageMilliseconds,Math.max(1,deadline-Date.now())));
      const saved=await read(projectId);if(saved.value.latest!.requestedRevision&&saved.value.latest!.requestedRevision!==inventory.revision)fail('PROJECT_SCAN_SOURCE_STALE');
      await guard(projectId,scanId,controller,inventory);
      result={state:inventory.coverage==='complete'?'completed':'partial',counts:{...inventory.counts},reasons:inventory.reasons};
     }else{
      await guard(projectId,scanId,controller,inventory!);const analyzer=analyzers[kind];
      if(!analyzer)result={state:'unavailable',reasons:['ANALYZER_UNAVAILABLE']};
      else result=await awaitAdapter(Promise.resolve().then(()=>analyzer({project:p,inventory:inventory!,signal:controller.signal,
       publicationGuard:()=>guard(projectId,scanId,controller,inventory!),canPublish:()=>!closed&&!controller.signal.aborted&&controllers.get(scanId)===controller,
       onProgress:async(completed,total)=>{if(!Number.isSafeInteger(completed)||!Number.isSafeInteger(total)||completed<0||total<completed||total>1000000)fail('PROJECT_SCAN_PROGRESS_INVALID');await owned(projectId,scanId,scan=>{const stage=scan.stages.find(item=>item.kind===kind)!;stage.progress={completed,total};stage.updatedAt=stamp();});}
      })),controller,Math.min(limits.stageMilliseconds,Math.max(1,deadline-Date.now())));
      await guard(projectId,scanId,controller,inventory!);
     }
     if(!result||!['completed','partial','unavailable'].includes(result.state??'completed'))fail('PROJECT_SCAN_RESULT_INVALID');
     const safe=safeVisibleValue(result) as ScanAnalyzerResult,encoded=JSON.stringify(safe);
     if(Buffer.byteLength(encoded)>limits.resultBytes)fail('PROJECT_SCAN_RESULT_LIMIT');
     const escapedRoot=JSON.stringify(p.canonicalRoot).slice(1,-1).toLowerCase();if(encoded.toLowerCase().includes(escapedRoot))fail('PROJECT_SCAN_RESULT_UNSAFE');
     await owned(projectId,scanId,scan=>{
      const stage=scan.stages.find(item=>item.kind===kind)!;Object.assign(stage,{state:safe.state??'completed',counts:safe.counts,reasons:safe.reasons??[],...(safe.data?{data:safe.data}:{}),updatedAt:stamp()});
      if(kind==='inventory'){scan.inventoryRevision=inventory!.revision;scan.counts=inventory!.counts;}
     });
    }catch(error){
     const reason=code(error);if(controller.signal.aborted||closed||/CANCELLED|SUPERSEDED|SCOPE_STALE|SOURCE_STALE|ROOT_UNAVAILABLE|SOURCE_DRIFT/.test(reason))throw error;
     await owned(projectId,scanId,scan=>{const stage=scan.stages.find(item=>item.kind===kind)!;Object.assign(stage,{state:'failed',reasons:[reason],updatedAt:stamp()});scan.reasons=[...new Set([...scan.reasons,reason])];});
     if(kind==='inventory')throw error;
    }
   }
   await guard(projectId,scanId,controller,inventory!);
   await owned(projectId,scanId,(scan,saved)=>{scan.state=scan.stages.every(stage=>stage.state==='completed')?'completed':'partial';scan.stage=null;scan.finishedAt=stamp();scan.reasons=[...new Set([...scan.reasons,...scan.stages.flatMap(stage=>stage.reasons)])];saved.value.lastSuccessful=structuredClone(scan);});
  }catch(error){
   const reason=controller.signal.reason?.code==='PROJECT_SCAN_TIMEOUT'?'PROJECT_SCAN_TIMEOUT':code(error);
   try{await owned(projectId,scanId,scan=>{scan.state=closed?'interrupted':/SCOPE_STALE|SOURCE_STALE|ROOT_UNAVAILABLE|SOURCE_DRIFT/.test(reason)?'interrupted':reason==='PROJECT_SCAN_TIMEOUT'?'failed':controller.signal.aborted?'cancelled':'failed';scan.reasons=[...new Set([...scan.reasons,reason])];scan.stage=null;scan.finishedAt=stamp();for(const stage of scan.stages)if(stage.state==='running'||stage.state==='pending'){stage.state='cancelled';stage.reasons=[reason];stage.updatedAt=stamp();}});}catch{}
  }finally{clearTimeout(jobTimer);controllers.delete(scanId);ownedIds.delete(scanId);}
 }
 function pump(){if(pumping||closed)return;pumping=true;setImmediate(()=>{pumping=false;while(!closed&&work.size<limits.concurrency&&queue.length){const next=queue.shift()!;const pending=run(next.projectId,next.scanId);work.add(pending);void pending.finally(()=>{work.delete(pending);pump();}).catch(()=>{});}});}
 async function status(projectId:string){await ready;const saved=await read(projectId);return view(projectId,saved);}
 async function latestAnalysis(projectId:string){
  await ready;
  const {value}=await read(projectId);
  return analysisObservation(value.latest)??value.lastAnalysis??analysisObservation(value.lastSuccessful);
 }
 async function start(projectId:string,input:{requestId?:string;revision?:string;stages?:ProjectScanStageKind[]}={}){
  await ready;if(closed)fail('PROJECT_SCAN_CLOSED');if(!input||typeof input!=='object'||Array.isArray(input)||Object.keys(input).some(key=>!['requestId','revision','stages'].includes(key))||input.requestId!==undefined&&(typeof input.requestId!=='string'||!/^[-A-Za-z0-9_:]{1,160}$/.test(input.requestId))||input.revision!==undefined&&(typeof input.revision!=='string'||!/^[a-f0-9]{64}$/.test(input.revision))||input.stages!==undefined&&(!Array.isArray(input.stages)||!input.stages.length||input.stages.length>stages.length||input.stages.some(kind=>!stages.includes(kind))||new Set(input.stages).size!==input.stages.length))fail('PROJECT_SCAN_INPUT_INVALID');
  const selected=input.stages?stages.filter(kind=>kind==='inventory'||input.stages!.includes(kind)):stages;
  return serial(projectId,async()=>{
   const p=await project(projectId),saved=await read(projectId),policyVersion=inventoryForProject(p).policyVersion,requestId=input.requestId??randomUUID(),digest=hash([projectId,p.rootIdentity,policyVersion,input.revision??null,selected]);
   const previous=saved.value.requests.find(item=>item.id===requestId);if(previous){if(previous.digest!==digest)fail('PROJECT_SCAN_REQUEST_CONFLICT');return {...view(projectId,saved),replayedScanId:previous.scanId};}
   const latest=saved.value.latest;
   if(live(latest)){
    if(latest!.rootIdentity!==p.rootIdentity||latest!.policyVersion!==policyVersion||latest!.requestedRevision!==(input.revision??null)||JSON.stringify(latest!.stages.map(stage=>stage.kind))!==JSON.stringify(selected))fail('PROJECT_SCAN_BUSY');
    saved.value.requests.push({id:requestId,digest,scanId:latest!.scanId});saved.value.requests=saved.value.requests.slice(-32);const persisted=await save(projectId,saved);return {...view(projectId,persisted),coalesced:true};
   }
   if(queue.length+work.size>=limits.queued)fail('PROJECT_SCAN_BUSY');
   const now=stamp(),scan:ProjectScan={schemaVersion:'paos_project_scan_v1',scanId:randomUUID(),projectId,attempt:(latest?.attempt??0)+1,rootIdentity:p.rootIdentity,policyVersion,requestedRevision:input.revision??null,inventoryRevision:null,state:'queued',stage:null,startedAt:now,updatedAt:now,counts:null,reasons:[],stages:selected.map(kind=>({kind,state:'pending',updatedAt:now,reasons:[]}))};
   const analysis=analysisObservation(latest)??saved.value.lastAnalysis??analysisObservation(saved.value.lastSuccessful);
   if(analysis)saved.value.lastAnalysis=analysis;
   saved.value.latest=scan;saved.value.requests.push({id:requestId,digest,scanId:scan.scanId});saved.value.requests=saved.value.requests.slice(-32);
   const persisted=await save(projectId,saved);ownedIds.add(scan.scanId);queue.push({projectId,scanId:scan.scanId});pump();return view(projectId,persisted);
  });
 }
 async function cancel(projectId:string,scanId:string){
  await ready;
  return serial(projectId,async()=>{const saved=await read(projectId),scan=saved.value.latest;if(!scan||scan.scanId!==scanId)fail('PROJECT_SCAN_NOT_FOUND');if(!live(scan))return view(projectId,saved);
   // Validate project ownership before touching a controller; IDs are not authority.
   controllers.get(scanId)?.abort();for(let i=queue.length-1;i>=0;i--)if(queue[i].projectId===projectId&&queue[i].scanId===scanId)queue.splice(i,1);ownedIds.delete(scanId);
   scan.state='cancelled';scan.stage=null;scan.updatedAt=stamp();scan.finishedAt=stamp();scan.reasons=[...new Set([...scan.reasons,'OWNER_CANCELLED'])];for(const stage of scan.stages)if(stage.state==='pending'||stage.state==='running'){stage.state='cancelled';stage.updatedAt=stamp();stage.reasons=['OWNER_CANCELLED'];}return view(projectId,await save(projectId,saved));});
 }
 return {initialized:async()=>{await ready;},status,start,cancel,latestAnalysis,
  async retry(projectId:string,scanId:string){await ready;const saved=await read(projectId);if(saved.value.latest?.scanId!==scanId&&!saved.value.requests.some(item=>item.id==='retry:'+scanId))fail('PROJECT_SCAN_NOT_FOUND');if(live(saved.value.latest)&&saved.value.latest!.scanId===scanId)fail('PROJECT_SCAN_BUSY');return start(projectId,{requestId:'retry:'+scanId,...(saved.value.latest?.scanId===scanId?{stages:saved.value.latest.stages.map(stage=>stage.kind)}:{})});},
  async close(){if(closed)return;closed=true;for(const controller of controllers.values())controller.abort();await ready;for(const p of await store.projects()){let saved:Saved;try{saved=await read(p.id);}catch{continue;}if(live(saved.value.latest)&&ownedIds.has(saved.value.latest!.scanId)){const scan=saved.value.latest!;scan.state='interrupted';scan.stage=null;scan.updatedAt=stamp();scan.finishedAt=stamp();scan.reasons=[...new Set([...scan.reasons,'SERVICE_SHUTDOWN_NO_REPLAY'])];try{await save(p.id,saved);}catch{}}}queue.length=0;await Promise.allSettled([...work]);}
 };
}
