import {createHash} from 'node:crypto';
import {mkdir,mkdtemp,realpath,rm,writeFile} from 'node:fs/promises';
import {basename,dirname,join,relative,isAbsolute} from 'node:path';
import {tmpdir} from 'node:os';
import type {LocalStore,Project} from '../storage/local-store.mts';
import {decodeTaskProfile} from '../../../../packages/contracts/issues/task-profile.ts';
import {decodeMethodologyDecision,type MethodologyScope} from '../../../../packages/contracts/methodology-decision.ts';
import type {ProjectAnalysisView,TaskAdviceRequest,TaskAdviceView} from '../../../../packages/contracts/project-analysis.ts';
import type {InventorySnapshot} from '../../../../packages/contracts/project-inventory.ts';
import {inventoryForProject} from '../code-index/sources.mts';
import {assertCurrentSourceProject,inventoryScopeFingerprint} from '../project-inventory/scope.mts';
import {normaliseRelativePath} from '../project-inventory/service.mts';
import {safeVisibleValue} from '../redaction/persisted.mts';

type Observation = {scanId: string | null; view: ProjectAnalysisView; inventory?: InventorySnapshot};
type Runner = (projection:string,owned:string,payload:string,signal:AbortSignal)=>Promise<unknown>;
type Options = {
 store: LocalStore;
 observe: (project:Project,signal:AbortSignal)=>Promise<Observation>;
 runTaskBridge: Runner;
};
const digest = (value:string)=>createHash('sha256').update(value).digest('hex');
const fail = (code:string):never=>{throw Object.assign(new Error(code),{code});};
const token = /^[a-zA-Z0-9_-]{1,128}$/;
const checkCommand = /^python(?:3|\.exe)?(?: -B)? -m unittest [A-Za-z_][A-Za-z0-9_.]*$/;
const contextFiles = new Set(['AGENTS.md','AGENTS.override.md','TEST.md','pyproject.toml','package.json','mkdocs.yml','go.mod','Cargo.toml','requirements.txt']);

function readRequest(value:Record<string,unknown>):TaskAdviceRequest {
 const {taskId,taskRevision,mode,sourcePath,testPath,testCommand}=value;
 if(Object.keys(value).some(key=>!['taskId','taskRevision','mode','sourcePath','testPath','testCommand'].includes(key))
   ||typeof taskId!=='string'||!token.test(taskId)||typeof taskRevision!=='number'||!Number.isSafeInteger(taskRevision)||taskRevision<1
   ||mode!=='defect_fix'&&mode!=='docs_only'
   ||mode==='docs_only'&&(testPath!==undefined||testCommand!==undefined)
   ||mode==='defect_fix'&&sourcePath!==undefined
   ||testCommand!==undefined&&(typeof testCommand!=='string'||testCommand!==testCommand.trim()||testCommand.length>256||!checkCommand.test(testCommand)))return fail('TASK_ADVICE_INPUT_INVALID');
 const path=(input:unknown):string|undefined=>{
  if(input===undefined)return undefined;
  if(typeof input!=='string'||!input.trim()||input.length>300) return fail('TASK_ADVICE_INPUT_INVALID');
  try{return normaliseRelativePath(input);}catch{return fail('TASK_ADVICE_INPUT_INVALID');}
 };
 return {taskId,taskRevision,mode,sourcePath:path(sourcePath),testPath:path(testPath),testCommand};
}

function fresh(outer:AbortSignal):AbortSignal{
 return AbortSignal.any([outer,AbortSignal.timeout(20_000)]);
}

export function createTaskAdvice({store,observe,runTaskBridge}:Options){
 let active=false;
 return async function taskAdvice(projectId:string,raw:Record<string,unknown>,outer:AbortSignal):Promise<TaskAdviceView>{
  const input=readRequest(raw),signal=fresh(outer);
  const {project,task}=await store.runtimeFileScope(projectId,input.taskId);
  if(!project||!task||task.projectId!==projectId||task.kind!=='task'||task.deleted)return fail('TASK_NOT_FOUND');
  if(task.revision!==input.taskRevision)return fail('TASK_ADVICE_TASK_STALE');
  const result:TaskAdviceView={
   schemaVersion:'paos_project_task_advice_v1',projectId,taskId:task.id,taskRevision:task.revision,
   selector:'project_analysis_task_bridge',status:'unavailable',sourceRevision:null,analysisScanId:null,adapterSourceRevision:null,
   warnings:[],coverage:{content:[],metadataCount:0,omittedCount:0},decision:null,
  };
  if(active)return {...result,warnings:['TASK_ADVICE_BUSY']};
  active=true;
  let owned:string|undefined,tempBase:string|undefined;
  try{
   signal.throwIfAborted();
   const {scanId,view,inventory}=await observe(project,signal);
   signal.throwIfAborted();
   result.analysisScanId=scanId;
   result.sourceRevision=scanId?view.sourceRevision:null;
   result.adapterSourceRevision=view.adapterSourceRevision??null;
   if(view.stale)return {...result,status:'stale',warnings:['ANALYSIS_SOURCE_STALE']};
   if(view.availability!=='available'||!inventory||!scanId){
    return {...result,warnings:[view.limitations.find(reason=>/^ANALYSIS_(?:CORE|PYTHON|TIMEOUT|FAILED|OUTPUT)/.test(reason))??'ANALYSIS_SCAN_REQUIRED']};
   }
   const profile=decodeTaskProfile(task.data);
   const changed=[...new Set(profile.files.map(file=>file.relativePath))];
   if(!changed.length||changed.length>20||!profile.acceptanceCriteria.length||profile.acceptanceCriteria.length>20)
    return {...result,status:'partial',warnings:['TASK_ADVICE_TASK_SCOPE_REQUIRED']};
   const supportedPath=input.mode==='docs_only'?/[.](?:md|rst|txt)$/i:/[.]py$/i;
   if(changed.some(path=>!supportedPath.test(path)))
    return {...result,status:'partial',warnings:['TASK_ADVICE_MODE_CONFLICT']};
   const requested=[...changed,...[input.sourcePath,input.testPath].filter((path):path is string=>Boolean(path))];
   const priority=new Set(requested);
   const inv=inventoryForProject(project);
   tempBase=await realpath(tmpdir());
   const relation=relative(project.canonicalRoot,tempBase);
   if(!relation||!isAbsolute(relation)&&relation!=='..'&&!relation.startsWith('..'+(process.platform==='win32'?'\\':'/')))
    return fail('ANALYSIS_TEMP_UNSAFE');
   owned=await mkdtemp(join(tempBase,'paos-advice-'));
   const projection=join(owned,'projection');
   await mkdir(projection);
   const contents=new Map<string,string>(), fileHashes=new Map<string,string>();
   const entries=inventory.entries.filter(entry=>entry.kind==='file'&&entry.access.readable);
   entries.sort((left,right)=>Number(priority.has(right.relativePath))-Number(priority.has(left.relativePath))
    ||Number(contextFiles.has(basename(right.relativePath)))-Number(contextFiles.has(basename(left.relativePath)))
    ||left.relativePath.localeCompare(right.relativePath));
   let bytes=0;
   for(const entry of entries){
    signal.throwIfAborted();
    const path=normaliseRelativePath(entry.relativePath);
    if(fileHashes.size>=200){result.coverage.omittedCount++;continue;}
    let content='';
    if(priority.has(path)||contextFiles.has(basename(path))){
     try{
      const read=await inv.read(project,{path,revision:entry.revision,maxBytes:64*1024});
      content=read.text;
     }catch(error){
      if(/STALE|DRIFT/.test(String((error as {code?:string})?.code)))throw error;
      result.coverage.omittedCount++;continue;
     }
     bytes+=Buffer.byteLength(content);
     if(bytes>2*1024*1024){result.coverage.omittedCount++;continue;}
     contents.set(path,content);
    }else result.coverage.metadataCount++;
    const destination=join(projection,...path.split('/'));
    await mkdir(dirname(destination),{recursive:true});
    await writeFile(destination,content,{flag:'wx'});
    fileHashes.set(path,digest(content));
   }
   result.coverage.content=[...contents.keys()].sort();
   if(requested.some(path=>!contents.has(path)))result.warnings.push('TASK_ADVICE_SOURCE_NOT_OBSERVED');
   if(result.coverage.omittedCount||inventory.coverage==='partial')result.warnings.push('TASK_ADVICE_BOUNDED_COVERAGE');
   const declared=input.testCommand&&contents.get('TEST.md')?.split(/\r?\n/).some(line=>
    line.trim()===input.testCommand||line.includes('`'+input.testCommand+'`'));
   const haveTest=Boolean(declared&&input.testPath&&contents.has(input.testPath));
   const verification=input.mode==='defect_fix'?(haveTest?[input.testPath!]:[]):(input.sourcePath&&contents.has(input.sourcePath)?[input.sourcePath]:[]);
   if(input.mode==='defect_fix'&&!haveTest)result.warnings.push('TASK_ADVICE_TEST_NOT_OBSERVED');
   if(input.mode==='docs_only'&&!verification.length)result.warnings.push('TASK_ADVICE_DOC_SOURCE_REQUIRED');
   const context=safeVisibleValue({
    schema_version:1,task_id:task.id,intent:profile.title,change_mode:input.mode,changed_paths:changed,
    risk_level:'low',acceptance:profile.acceptanceCriteria,
    risks:input.mode==='docs_only'?[]:[{risk_id:'local-behavior',kind:'pure_logic',
     description:profile.risks[0]??'Preserve the declared acceptance behavior',
     protected_invariants:profile.acceptanceCriteria,languages:['python']}],
    verification_paths:verification,
    ...(input.mode==='defect_fix'?{executable_test_seam:haveTest,
     checks:haveTest?[{command:input.testCommand,source:'TEST.md',test_kinds:['unit']}]:[]}:{}),
   });
   const scope:MethodologyScope={
    project_id:inventoryScopeFingerprint(project),task_id:task.id,
    source_revision:digest(JSON.stringify([inventory.revision,[...fileHashes].sort()])),
    task_revision:digest(JSON.stringify([task.revision,context])),
   };
   const payload=JSON.stringify({task:context,scope});
   if(Buffer.byteLength(payload)>16*1024)return {...result,status:'partial',warnings:['TASK_ADVICE_INPUT_LIMIT']};
   const envelope=await runTaskBridge(projection,owned,payload,signal) as {schemaVersion?:string;decision?:unknown}|null;
   if(envelope?.schemaVersion!=='paos_task_advice_bridge_v1')return fail('TASK_ADVICE_OUTPUT_INVALID');
   const decision=decodeMethodologyDecision(safeVisibleValue(envelope.decision),scope);
   if(decision.evidence.some(source=>source.kind==='file'&&(!source.path||!contents.has(source.path)||fileHashes.get(source.path)!==source.revision)))
    return fail('TASK_ADVICE_OUTPUT_INVALID');
   const latest=await observe(project,signal);
   await assertCurrentSourceProject(store,project,task);
   if(latest.inventory?.revision!==inventory.revision||latest.scanId!==scanId||latest.view.stale||latest.view.availability!=='available'
    ||latest.view.adapterSourceRevision!==result.adapterSourceRevision)return {...result,status:'stale',warnings:['ANALYSIS_SOURCE_STALE']};
   signal.throwIfAborted();
   result.decision=decision;
   result.status=result.warnings.length||decision.plan.gaps.length?'partial':'ready';
   return result;
  }catch(error){
   const code=(error as {code?:string})?.code;
   if(outer.aborted)return fail('TASK_ADVICE_CANCELLED');
   if(signal.aborted)return {...result,warnings:['ANALYSIS_TIMEOUT']};
   if(code&&/STALE|DRIFT/.test(code))return {...result,status:'stale',warnings:['ANALYSIS_SOURCE_STALE']};
   if(code&&/^ANALYSIS_[A-Z_]+$/.test(code))return {...result,warnings:[code]};
   if(code==='TASK_ADVICE_OUTPUT_INVALID'||String((error as Error)?.message).startsWith('methodology_decision:'))
    return {...result,warnings:['TASK_ADVICE_OUTPUT_INVALID']};
   return {...result,warnings:['TASK_ADVICE_UNAVAILABLE']};
  }finally{
   try{
    if(owned&&tempBase&&dirname(await realpath(owned))===tempBase&&basename(owned).startsWith('paos-advice-'))
     await rm(owned,{recursive:true,force:true});
   }finally{active=false;}
  }
 };
}
