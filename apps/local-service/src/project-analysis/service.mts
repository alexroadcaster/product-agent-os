import {spawn} from 'node:child_process';
import {mkdtemp,mkdir,writeFile,rm,access,readFile} from 'node:fs/promises';
import {join,dirname,relative,resolve,extname,isAbsolute} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import type {LocalStore,Project} from '../storage/local-store.mts';
import type {ScanAnalyzerContext,ScanAnalyzerResult} from '../project-scans/service.mts';
import {inventoryForProject} from '../code-index/sources.mts';
import type {ProjectAnalysisView,AnalysisSource,AnalysisEvidence} from '../../../../packages/contracts/project-analysis.ts';
import type {InventorySnapshot} from '../../../../packages/contracts/project-inventory.ts';

type Limits={files:number;bytes:number;fileBytes:number;milliseconds:number;outputBytes:number};
/** Runtime overrides belong to the trusted host/test constructor, never project or HTTP input. */
type Runtime={pythonExecutable?:string;coreScripts?:string;bridgePath?:string};
const defaults:Limits={files:200,bytes:2*1024*1024,fileBytes:64*1024,milliseconds:15000,outputBytes:128*1024};
const coreScripts=fileURLToPath(new URL('../../../../plugins/product-agent-os/scripts/',import.meta.url));
const bridgePath=fileURLToPath(new URL('./bridge.py',import.meta.url));
const coreFiles=['__init__.py','discovery.py','contracts.py','plugin_components.py','methodology_audit.py','methodology_catalog.py','methodology_synthesis.py','question_protocol.py','templates.py'];
async function adapterRevision(runtime:Runtime){
 const scripts=runtime.coreScripts??coreScripts;
 const paths=[fileURLToPath(import.meta.url),runtime.bridgePath??bridgePath,...coreFiles.map(name=>join(scripts,'product_agent_os',name)),join(scripts,'..','assets','methodology','methodology-catalog.json')];
 const digest=createHash('sha256');for(const path of paths){const bytes=await readFile(path);if(bytes.length>2*1024*1024)fail('ANALYSIS_CORE_SOURCE_LIMIT');digest.update(String(bytes.length)+':');digest.update(bytes);}return digest.digest('hex');
}
const control=['AGENTS.md','REQUIREMENTS.md','PLAN.md','TEST.md','EVALS.md','RUNLOG.md'];
const markers=new Set(['package.json','pyproject.toml','requirements.txt','mkdocs.yml','Cargo.toml','go.mod',...control]);
const language:Record<string,string>={'.ts':'TypeScript','.tsx':'TypeScript','.js':'JavaScript','.jsx':'JavaScript','.py':'Python','.rs':'Rust','.go':'Go','.java':'Java','.cs':'C#','.rb':'Ruby','.php':'PHP','.sql':'SQL'};
const hash=(value:unknown)=>createHash('sha256').update(JSON.stringify(value)).digest('hex');
const fail=(code:string):never=>{throw Object.assign(new Error(code),{code});};
const inside=(parent:string,child:string)=>{const path=relative(resolve(parent),resolve(child));return path===''||!path.startsWith('..')&&!isAbsolute(path);};
const schemaKind=(path:string):'schema'|'migration'|'orm'|'database_file'|null=>/\.(?:sqlite3?|db)$/i.test(path)?'database_file':/schema\.prisma$|models\.py$|(?:entity|model)\.(?:ts|py)$|typeorm|sequelize/i.test(path)?'orm':/migration/i.test(path)?'migration':/\.(?:sql|dbml)$|(?:^|\/)(?:schema|database|db)\//i.test(path)?'schema':null;
const contentPath=(path:string)=>markers.has(path)||/(?:^|\/)(?:\.codex-plugin\/)?plugin\.json$/.test(path);

/** Shared GET/analyzer empty state: missing evidence is explicit, never fabricated success. */
export function unavailableProjectAnalysis(project:Pick<Project,'id'|'rootIdentity'>,inventory:Pick<InventorySnapshot,'revision'|'policyVersion'>,reason='ANALYSIS_NOT_OBSERVED'):ProjectAnalysisView{
 return {schemaVersion:'paos_project_analysis_v1',projectId:project.id,sourceRevision:inventory.revision,rootIdentity:project.rootIdentity,policyVersion:inventory.policyVersion,inventoryRevision:inventory.revision,observedAt:new Date().toISOString(),availability:'unavailable',stale:false,stack:[],languages:[],components:[],controlPlane:[],findings:[],schemaCandidates:[],limitations:['BOUNDED_PROJECTION','METADATA_IS_NOT_RUNTIME_VERIFICATION','DATABASE_NOT_OPENED','SUBPROCESS_RSS_NOT_OS_LIMITED',reason],database:{available:false,reason:'DATABASE_CONNECTION_NOT_CONFIGURED'},projection:{files:0,bytes:0,omitted:0,coverage:'partial'}};
}

/** Only a fixed trusted Python entry point sees an owned projection; target code is never imported. */
function runBridge(runtime:Runtime,projection:string,owned:string,limits:Limits,signal:AbortSignal):Promise<unknown>{
 return new Promise((accept,reject)=>{
  if(signal.aborted){reject(Object.assign(Error('ANALYSIS_CANCELLED'),{code:'ANALYSIS_CANCELLED'}));return;}
  const env:NodeJS.ProcessEnv={HOME:owned,USERPROFILE:owned,TEMP:owned,TMP:owned};
  for(const key of ['SystemRoot','WINDIR'])if(process.env[key])env[key]=process.env[key];
  const pathValue=process.env.Path??process.env.PATH;if(pathValue)env.PATH=pathValue;
  const child=spawn(runtime.pythonExecutable??'python',['-I','-S','-B',runtime.bridgePath??bridgePath,runtime.coreScripts??coreScripts,projection],{cwd:owned,env,shell:false,windowsHide:true,stdio:['ignore','pipe','pipe']});
  let bytes=0;const chunks:Buffer[]=[];let failure:string|undefined;
  const stop=(code:string)=>{failure??=code;child.kill();};
  const abort=()=>stop('ANALYSIS_CANCELLED');signal.addEventListener('abort',abort,{once:true});
  const timer=setTimeout(()=>stop('ANALYSIS_TIMEOUT'),limits.milliseconds);
  child.stdout.on('data',(chunk:Buffer)=>{bytes+=chunk.length;if(bytes>limits.outputBytes)stop('ANALYSIS_OUTPUT_LIMIT');else chunks.push(chunk);});
  child.stderr.on('data',(chunk:Buffer)=>{bytes+=chunk.length;if(bytes>limits.outputBytes)stop('ANALYSIS_OUTPUT_LIMIT');});
  const cleanup=()=>{clearTimeout(timer);signal.removeEventListener('abort',abort);};
  child.once('error',()=>{cleanup();reject(Object.assign(Error('ANALYSIS_PYTHON_UNAVAILABLE'),{code:'ANALYSIS_PYTHON_UNAVAILABLE'}));});
  child.once('close',exit=>{cleanup();if(failure||exit!==0){reject(Object.assign(Error(failure??'ANALYSIS_CORE_FAILED'),{code:failure??'ANALYSIS_CORE_FAILED'}));return;}try{accept(JSON.parse(Buffer.concat(chunks).toString('utf8')));}catch{reject(Object.assign(Error('ANALYSIS_OUTPUT_INVALID'),{code:'ANALYSIS_OUTPUT_INVALID'}));}});
 });
}

export function createProjectAnalysis({store,limits:configured,runtime={}}:{store:LocalStore;limits?:Partial<Limits>;runtime?:Runtime}){
 const limits={...defaults,...configured};for(const [key,value] of Object.entries(limits))if(!Number.isSafeInteger(value)||value<1||value>defaults[key as keyof Limits])fail('ANALYSIS_LIMIT_INVALID');
 async function analyze(context:ScanAnalyzerContext):Promise<ScanAnalyzerResult>{
  const {project,inventory,signal}=context,adapter=inventoryForProject(project),started=Date.now();
  const view=unavailableProjectAnalysis(project,inventory);view.limitations=view.limitations.filter(reason=>reason!=='ANALYSIS_NOT_OBSERVED');
  async function guard(){
   if(signal.aborted||!context.canPublish())fail('ANALYSIS_CANCELLED');
   if(Date.now()-started>limits.milliseconds)fail('ANALYSIS_TIMEOUT');
   const current=await store.project(project.id);if(!current||current.rootIdentity!==project.rootIdentity||current.canonicalRoot!==project.canonicalRoot)fail('ANALYSIS_ROOT_STALE');
   if(hash(current!.inventoryPolicy??{})!==hash(project.inventoryPolicy??{}))fail('ANALYSIS_POLICY_STALE');
   const next=await adapter.snapshot(project,{signal});if(next.policyVersion!==inventory.policyVersion||next.revision!==inventory.revision)fail('ANALYSIS_SOURCE_STALE');
   await context.publicationGuard();if(!context.canPublish())fail('ANALYSIS_CANCELLED');
  }
  let owned:string|undefined;
  try{
   await guard();
   try{await access(join(runtime.coreScripts??coreScripts,'product_agent_os','discovery.py'));view.adapterSourceRevision=await adapterRevision(runtime);}catch{fail('ANALYSIS_CORE_UNAVAILABLE');}
   if(inside(project.canonicalRoot,tmpdir()))fail('ANALYSIS_TEMP_UNSAFE');
   owned=await mkdtemp(join(tmpdir(),'paos-analysis-'));const projection=join(owned,'projection');await mkdir(projection);
   const sources=new Map<string,AnalysisSource>();
   const entries=inventory.entries.filter(entry=>entry.kind==='file'&&entry.access.readable&&(contentPath(entry.relativePath)||Boolean(language[extname(entry.relativePath)])||schemaKind(entry.relativePath))).sort((a,b)=>Number(contentPath(b.relativePath))-Number(contentPath(a.relativePath))||a.relativePath.localeCompare(b.relativePath));
   for(const entry of entries){
    if(signal.aborted)fail('ANALYSIS_CANCELLED');if(Date.now()-started>limits.milliseconds)fail('ANALYSIS_TIMEOUT');
    const path=entry.relativePath;if(sources.size>=limits.files){view.projection.omitted++;continue;}
    // Inventory validates the path and identity again on content reads. Metadata placeholders contain no target bytes.
    if(path.includes('\\')||path.split('/').some(part=>!part||part==='.'||part==='..')||isAbsolute(path))fail('ANALYSIS_PATH_INVALID');
    let text='',basis:AnalysisSource['basis']='metadata';
    if(contentPath(path)){
     try{const read=await adapter.read(project,{path,revision:entry.revision,maxBytes:limits.fileBytes});text=read.text;basis='content';}catch(error){if((error as any)?.code==='INVENTORY_REVISION_STALE'||(error as any)?.code==='INVENTORY_SOURCE_DRIFT')throw error;view.projection.omitted++;continue;}
     if(view.projection.bytes+Buffer.byteLength(text)>limits.bytes){view.projection.omitted++;continue;}
    }
    const output=join(projection,...path.split('/'));if(!inside(projection,output))fail('ANALYSIS_PATH_INVALID');await mkdir(dirname(output),{recursive:true});await writeFile(output,text,{flag:'wx'});
    sources.set(path,{path,line:null,basis});view.projection.files++;view.projection.bytes+=Buffer.byteLength(text);
   }
   await guard();await context.onProgress(0,1);
   const result=await runBridge(runtime,projection,owned,{...limits,milliseconds:Math.max(1,limits.milliseconds-(Date.now()-started))},signal) as any;
   if(!result||result.schemaVersion!=='paos_analysis_bridge_v1'||!Array.isArray(result.stack)||!Array.isArray(result.controlPlane)||!Array.isArray(result.components))fail('ANALYSIS_OUTPUT_INVALID');
   if(typeof result.pythonVersion==='string'&&/^3\.\d+\.\d+$/.test(result.pythonVersion))view.runtime={pythonVersion:result.pythonVersion,coreModule:'product_agent_os.discovery.analyze_workspace',deployment:'checkout_projection'};
   else fail('ANALYSIS_OUTPUT_INVALID');
   if(await adapterRevision(runtime)!==view.adapterSourceRevision)fail('ANALYSIS_ADAPTER_STALE');
   const evidence=(name:string,paths:string[]):AnalysisEvidence=>({name,confidence:'candidate',sources:paths.flatMap(path=>sources.has(path)?[sources.get(path)!]:[]).slice(0,20)});
   const stackMarkers:Record<string,string[]>={node:['package.json'],python:['pyproject.toml','requirements.txt'],docs:['mkdocs.yml'],rust:['Cargo.toml'],go:['go.mod'],monorepo:[...sources.keys()].filter(path=>path.startsWith('packages/'))};
   view.stack=[...new Set<string>(result.stack.filter((name:unknown)=>typeof name==='string'&&Object.hasOwn(stackMarkers,name)))].slice(0,20).map(name=>evidence(name,stackMarkers[name]));
   for(const name of [...new Set([...sources.keys()].map(path=>language[extname(path)]).filter(Boolean))])view.languages.push(evidence(name,[...sources.keys()].filter(path=>language[extname(path)]===name)));
   view.components=result.components.filter((path:unknown)=>typeof path==='string'&&sources.has(path)).slice(0,20).map((path:string)=>evidence('plugin',[path]));
   view.controlPlane=control.map(path=>({path,status:sources.has(path)?'present_unverified':'not_observed',source:sources.get(path)??null}));
   view.findings=view.controlPlane.filter(item=>item.status==='not_observed').map(item=>({code:'CONTROL_PLANE_NOT_OBSERVED:'+item.path,confidence:'candidate',sources:[]}));
   for(const [path,source] of sources){const kind=schemaKind(path);if(kind)view.schemaCandidates.push({...evidence(path,[path]),kind,opened:false});}
   // Unreadable database content is never projected or opened, but its permitted metadata remains a candidate.
   for(const entry of inventory.entries.filter(entry=>entry.kind==='file'&&(entry.access.readable||entry.access.reason==='database_content')&&schemaKind(entry.relativePath)==='database_file').slice(0,20))view.schemaCandidates.push({name:entry.relativePath,confidence:'candidate',sources:[{path:entry.relativePath,line:null,basis:'metadata'}],kind:'database_file',opened:false});
   view.schemaCandidates=view.schemaCandidates.slice(0,40);view.availability='available';if(view.projection.omitted)view.limitations.push('PROJECTION_ENTRIES_OMITTED');
   await guard();await context.onProgress(1,1);await context.publicationGuard();if(!context.canPublish())fail('ANALYSIS_CANCELLED');
  }catch(error){
   const code=(error as any)?.code;const reason=typeof code==='string'&&/^[A-Z_]{1,80}$/.test(code)?code:'ANALYSIS_FAILED';
   if(signal.aborted||reason==='ANALYSIS_CANCELLED')fail('ANALYSIS_CANCELLED');
   if(/STALE|DRIFT|ROOT_UNAVAILABLE/.test(reason)){view.stale=true;throw Object.assign(Error(reason),{code:reason});}
   view.availability='unavailable';view.limitations.push(reason);
  }finally{if(owned)await rm(owned,{recursive:true,force:true});}
  return {state:view.availability==='available'?'partial':'unavailable',reasons:view.limitations,counts:{projected:view.projection.files,omitted:view.projection.omitted},data:{analysis:view}};
 }
 return {analyze,currentRevision:()=>adapterRevision(runtime)};
}
