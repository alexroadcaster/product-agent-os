import {mkdtemp,open,realpath,rm} from 'node:fs/promises';
import {basename,dirname,isAbsolute,join,relative,sep} from 'node:path';
import {tmpdir} from 'node:os';
import {bindProject} from '../apps/local-service/src/adapters/project-sources.ts';
import {inventoryForProject} from '../apps/local-service/src/code-index/sources.mts';
import {createCodeIndex} from '../apps/local-service/src/code-index/service.mts';
import {openLocalStore} from '../apps/local-service/src/storage/local-store.mts';
import {assessArchitecture,readArchitectureInput} from './project-methodology/architecture.mts';
import {planJourney} from './project-methodology/design.mts';

async function context(path:string){
 const file=await open(path,'r');
 try{
  const metadata=await file.stat();
  if(!metadata.isFile()||metadata.size>65536)throw Error('METHODOLOGY_CONTEXT_LIMIT');
  const buffer=Buffer.alloc(65537);
  const {bytesRead}=await file.read(buffer,0,buffer.length,0);
  if(bytesRead>65536)throw Error('METHODOLOGY_CONTEXT_LIMIT');
  return JSON.parse(buffer.subarray(0,bytesRead).toString('utf8'));
 }finally{await file.close();}
}

async function main([kind,workspace,metadata,...flags]:string[]){
 const withoutGraph=flags.length===1&&flags[0]==='--without-f14'&&kind==='architecture';
 if(!['design','architecture'].includes(kind)||!workspace||!metadata||flags.length&&!withoutGraph)
  throw Error('Usage: node tools/project-methodology.mts <design|architecture> <workspace> <context.json> [--without-f14]');
 const input=await context(metadata);
 const bound=await bindProject('methodology-local',await realpath(workspace));
 const project={id:bound.projectId,keyPrefix:'METH',canonicalRoot:bound.workspaceRoot,rootIdentity:bound.directoryIdentity,authorityMode:'sql' as const};
 const inventory=await inventoryForProject(project).snapshot(project);
 const paths=inventory.entries.filter(file=>file.kind==='file'&&file.access.readable).map(file=>file.relativePath);
 if(kind==='design'){
  if(input?.sourceRevision!==undefined&&input.sourceRevision!==inventory.revision)
   return {schemaVersion:'paos_design_journey_v1',status:'stale',authority:'read_only',
    gaps:['SOURCE_REVISION_MISMATCH'],next:'Refresh the design reference against the current workspace'};
  return planJourney({...input,sourceRevision:inventory.revision},new Set(paths));
 }
 const data=readArchitectureInput(input);
 const reportWithoutGraph=()=>assessArchitecture(data,paths,null,inventory.revision);
 if(withoutGraph||data.surface!=='frontend')return reportWithoutGraph();
 const base=await realpath(tmpdir()),rel=relative(project.canonicalRoot,base);
 if(!rel||!isAbsolute(rel)&&rel!=='..'&&!rel.startsWith('..'+sep))throw Error('METHODOLOGY_TEMP_INSIDE_TARGET');
 const scratch=await mkdtemp(join(base,'paos-methodology-'));
 let store:Awaited<ReturnType<typeof openLocalStore>>|undefined;
 try{
  store=await openLocalStore({databasePath:join(scratch,'profile.sqlite')});
  await store.registerProject(project);
  const graph=createCodeIndex(store);
  try{
   const status=await graph.rebuild(project.id,{expectedInventoryRevision:inventory.revision});
   if(!status.revision)return reportWithoutGraph();
   return assessArchitecture(data,paths,await graph.architectureEvidence(project.id,status.revision),inventory.revision);
  }catch(error){
   const code=(error as {code?:string})?.code;
   const gap=typeof code==='string'&&/^GRAPH_[A-Z_]+$/.test(code)?code:'GRAPH_EVIDENCE_UNAVAILABLE';
   const result=reportWithoutGraph();
   return {...result,gaps:[...result.gaps,{path:null,reason:gap}]};
  }
 }finally{
  try{await store?.close();}
  finally{
   const actual=await realpath(scratch);
   if(dirname(actual)!==base||!basename(actual).startsWith('paos-methodology-'))throw Error('METHODOLOGY_TEMP_SCOPE');
   await rm(actual,{recursive:true,force:true});
  }
 }
}

try{console.log(JSON.stringify(await main(process.argv.slice(2)),null,2));}
catch(error){
 const message=(error as Error)?.message??'';
 console.error(/^[A-Z_]{1,80}$/.test(message)||message.startsWith('Usage:')?message:'METHODOLOGY_INPUT_OR_WORKSPACE_UNAVAILABLE');
 process.exitCode=2;
}
