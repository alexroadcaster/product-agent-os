import {normaliseRelativePath} from '../../apps/local-service/src/project-inventory/service.mts';
import type {createCodeIndex} from '../../apps/local-service/src/code-index/service.mts';

type Evidence=Awaited<ReturnType<ReturnType<typeof createCodeIndex>['architectureEvidence']>>;
type Import=Evidence['imports'][number];
const layers=['shared','entities','features','widgets','pages','app'] as const;
type Layer=typeof layers[number];
type CrossApi={consumer:string;entry:string};
type Boundary={root:string;layer:Layer;owner:string;publicApi?:string;crossApi?:CrossApi[]};
type Rule='layer_direction'|'cross_slice_import'|'private_entry'|'import_cycle';
type Finding={from:string;to:string;line:number;rule:Rule;owner:string};
type Exception=Omit<Finding,'line'>&{reason:string};
export type ArchitectureInput={
 surface:'frontend'|'backend'|'native';
 pages:{path:string;owner:string}[];
 boundaries:Boundary[];
 changeFrequency:'occasional'|'frequent'|'unknown';
 migrationCost:'low'|'medium'|'high'|'unknown';
 exceptions:Exception[];
};

const knownSource=/\.(?:[cm]?[jt]s|[jt]sx|vue|svelte)$/i;
const under=(path:string,root:string)=>path===root||path.startsWith(root+'/');
const validText=(value:unknown):value is string=>typeof value==='string'&&value.trim()===value&&value.length>0&&value.length<=160&&!/[\x00-\x1f]/.test(value);
const row=(value:unknown,fields:string[])=>value!==null&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).every(key=>fields.includes(key));
const list=(value:unknown):value is unknown[]=>Array.isArray(value)&&value.length<=50;
const path=(value:unknown)=>validText(value)&&normaliseRelativePath(value)===value;
const rules:Rule[]=['layer_direction','cross_slice_import','private_entry','import_cycle'];

export function readArchitectureInput(value:unknown):ArchitectureInput{
 if(!row(value,['surface','pages','boundaries','changeFrequency','migrationCost','exceptions']))throw Error('ARCHITECTURE_CONTEXT_INVALID');
 const input=value as ArchitectureInput;
 if(!['frontend','backend','native'].includes(input.surface)||!['occasional','frequent','unknown'].includes(input.changeFrequency)
  ||!['low','medium','high','unknown'].includes(input.migrationCost)||!list(input.pages)||!list(input.boundaries)||!list(input.exceptions))
  throw Error('ARCHITECTURE_CONTEXT_INVALID');
 if(!input.pages.every(page=>row(page,['path','owner'])&&path(page.path)&&validText(page.owner))
  ||!input.boundaries.every(item=>row(item,['root','layer','owner','publicApi','crossApi'])&&path(item.root)
   &&layers.includes(item.layer)&&validText(item.owner)&&(item.publicApi===undefined||path(item.publicApi)&&under(item.publicApi,item.root)&&item.publicApi!==item.root)
   &&(item.crossApi===undefined||item.layer==='entities'&&list(item.crossApi)&&item.crossApi.every(api=>
    row(api,['consumer','entry'])&&path(api.consumer)&&path(api.entry)&&api.entry.startsWith(item.root+'/@x/'))))
  ||!input.exceptions.every(item=>row(item,['from','to','rule','owner','reason'])&&path(item.from)&&path(item.to)
   &&rules.includes(item.rule)&&validText(item.owner)&&validText(item.reason)))throw Error('ARCHITECTURE_CONTEXT_INVALID');
 if(new Set(input.pages.map(item=>item.path)).size!==input.pages.length||new Set(input.boundaries.map(item=>item.root)).size!==input.boundaries.length
  ||new Set(input.exceptions.map(ratchetKey)).size!==input.exceptions.length
  ||input.boundaries.some(boundary=>boundary.crossApi?.some(api=>api.consumer===boundary.root
   ||!input.boundaries.some(consumer=>consumer.layer==='entities'&&consumer.root===api.consumer))))throw Error('ARCHITECTURE_CONTEXT_INVALID');
 return input;
}

/** A move in source line numbers does not remove or introduce an import obligation. */
const ratchetKey=(finding:Omit<Finding,'line'>)=>JSON.stringify([finding.from,finding.to,finding.rule,finding.owner]);
export function newBoundaryViolations(baseline:Finding[],candidate:Finding[]):Finding[]{
 const allowed=new Map<string,number>();
 for(const finding of baseline){
  const key=ratchetKey(finding);allowed.set(key,(allowed.get(key)??0)+1);
 }
 return candidate.filter(finding=>{
  const key=ratchetKey(finding),left=allowed.get(key)??0;
  if(left===0)return true;
  allowed.set(key,left-1);return false;
 });
}

function cycleEdges(imports:(Import&{to:string})[]){
 const adjacency=new Map<string,(Import&{to:string})[]>();
 for(const edge of imports){const list=adjacency.get(edge.from)??[];list.push(edge);adjacency.set(edge.from,list);}
 const index=new Map<string,number>(),low=new Map<string,number>();
 const stack:string[]=[],active=new Set<string>(),component=new Map<string,number>();
 let next=0,group=0;
 function visit(file:string){
  index.set(file,next);low.set(file,next++);
  stack.push(file);active.add(file);
  for(const edge of adjacency.get(file)??[]){
   if(!index.has(edge.to)){
    visit(edge.to);
    low.set(file,Math.min(low.get(file)!,low.get(edge.to)!));
   }else if(active.has(edge.to))low.set(file,Math.min(low.get(file)!,index.get(edge.to)!));
  }
  if(low.get(file)!==index.get(file))return;
  for(;;){
   const member=stack.pop()!;
   active.delete(member);component.set(member,group);
   if(member===file)break;
  }
  group++;
 }
 for(const file of adjacency.keys())if(!index.has(file))visit(file);
 return imports.filter(edge=>component.get(edge.from)===component.get(edge.to));
}

export function assessArchitecture(input:ArchitectureInput,paths:string[],evidence:Evidence|null,inventoryRevision:string){
 const graphFiles=new Set(evidence?.coverage.filter(row=>row.status==='indexed').map(row=>row.relativePath)??[]);
 const permitted=new Set(paths),boundaries=[...input.boundaries].sort((a,b)=>b.root.length-a.root.length);
 const boundary=(file:string)=>boundaries.find(item=>under(file,item.root));
 const foundPages=input.pages.filter(page=>graphFiles.has(page.path)||/\.html?$/i.test(page.path)&&permitted.has(page.path));
 const imports=evidence?.imports??[];
 const resolved=imports.filter((edge):edge is Import&{to:string}=>edge.resolution==='lexical'&&edge.to!==null);
 const gaps:{path:string|null;line?:number;reason:string}[]=[];
 if(input.surface==='frontend'){
  if(!evidence)gaps.push({path:null,reason:'F14_ADAPTER_UNAVAILABLE'});
  if(evidence&&evidence.inventoryRevision!==inventoryRevision)gaps.push({path:null,reason:'INVENTORY_REVISION_MISMATCH'});
  if(evidence?.inventoryCoverage==='partial')gaps.push({path:null,reason:'INVENTORY_PARTIAL'});
  if(evidence?.limitations.includes('resolver_config_unavailable_or_unsupported'))gaps.push({path:'tsconfig.json',reason:'UNSUPPORTED_CONFIG'});
  for(const page of input.pages)if(!foundPages.includes(page))gaps.push({path:page.path,reason:'PAGE_UNOBSERVED'});
  for(const unit of boundaries)if(unit.publicApi&&!graphFiles.has(unit.publicApi))
   gaps.push({path:unit.publicApi,reason:'PUBLIC_API_UNOBSERVED'});
  for(const unit of boundaries)for(const api of unit.crossApi??[])
   if(!graphFiles.has(api.entry))gaps.push({path:api.entry,reason:'ENTITY_CROSS_API_UNOBSERVED'});
  for(const entry of evidence?.coverage??[])if(entry.status!=='indexed'&&(knownSource.test(entry.relativePath)||entry.reason==='linked_source'))
   gaps.push({path:entry.relativePath,reason:entry.reason??entry.status});
  for(const edge of imports)if(edge.resolution!=='lexical')gaps.push({path:edge.from,line:edge.line,reason:edge.reason??edge.resolution});
  if(foundPages.length===0)gaps.push({path:null,reason:'PAGE_SCOPE_REQUIRED'});
 }
 const applicable=input.surface==='frontend';
 const coupling=resolved.filter(edge=>{
  const from=boundary(edge.from),to=boundary(edge.to);
  return from&&to&&from.root!==to.root;
 });
 const findings:Finding[]=[],legacyExceptions:(Finding&{reason:string})[]=[];
 const add=(edge:Import&{to:string},rule:Rule,owner:string)=>{
  const finding={from:edge.from,to:edge.to,line:edge.line,rule,owner};
  const accepted=input.exceptions.find(item=>ratchetKey(item)===ratchetKey(finding));
  if(accepted)legacyExceptions.push({...finding,reason:accepted.reason});else findings.push(finding);
 };
 if(applicable)for(const edge of coupling){
  const from=boundary(edge.from)!,to=boundary(edge.to)!;
  if(layers.indexOf(from.layer)<layers.indexOf(to.layer))add(edge,'layer_direction',from.owner);
  else if(from.layer===to.layer){
   if(from.layer!=='entities'||!to.crossApi?.some(api=>api.consumer===from.root&&api.entry===edge.to))
    add(edge,'cross_slice_import',from.owner);
  }
  else if(edge.to!==to.publicApi)add(edge,'private_entry',from.owner);
 }
 if(applicable)for(const edge of cycleEdges(resolved))add(edge,'import_cycle',boundary(edge.from)?.owner??'project-owner');

 const change=input.changeFrequency,cost=input.migrationCost;
 const eligible=applicable&&gaps.length===0;
 const adjacency=new Map<string,string[]>();
 for(const edge of resolved){const next=adjacency.get(edge.from)??[];next.push(edge.to);adjacency.set(edge.from,next);}
 const affected=new Set([...findings,...legacyExceptions].map(finding=>finding.from));
 const reachesViolation=(page:string)=>{
  const seen=new Set([page]),queue=[page];
  for(let index=0;index<queue.length;index++){
   const file=queue[index];
   if(affected.has(file))return true;
   for(const target of adjacency.get(file)??[])if(!seen.has(target)){seen.add(target);queue.push(target);}
  }
  return false;
 };
 const pilot=eligible&&affected.size>0&&coupling.length>0&&change==='frequent'&&['low','medium'].includes(cost)
  ?foundPages.find(page=>reachesViolation(page.path)):undefined;
 const recommendation=!applicable?(input.surface==='native'?'native_boundary_policy':'backend_boundary_policy')
  :!eligible?'inspect_coverage'
  :pilot?'gradual_fsd'
  :affected.size>0?'strengthen_boundaries'
  :coupling.length>0?'retain_modular_boundaries':'retain_architecture';
 const alternatives=[
  {id:'retain_architecture',fit:findings.length===0?'limited rework; preserves stable boundaries':'keeps the observed boundary violations'},
  {id:'strengthen_boundaries',fit:coupling.length?'publish only the API used across confirmed boundaries':'avoid new layers without a demonstrated dependency'},
  {id:'gradual_fsd',fit:'consider one page only when source coverage, coupling, ownership, change frequency and migration cost support it'},
 ];
 const migration=pilot?{
  status:'proposal_only',owner:pilot.owner,ownerDecisionRequired:true,
  firstPage:pilot.path,
  baselineImports:resolved.filter(edge=>edge.from===pilot.path||edge.to===pilot.path),
  baselineFindings:findings,legacyExceptions,
  dependencies:['owner acceptance of the page scope','current F14 revision','PMETH-16 for staging and apply'],
  checkpoints:[
   {id:'page_boundary',action:'Expose only the entry points consumed by this page; preserve former entry points with compatibility re-exports.',
    acceptance:['Preserve page behavior and API semantics','Keep legacy exceptions exact','Reject additional imports that violate registered boundaries']},
   {id:'review_reuse',dependsOn:'page_boundary acceptance',action:'Move reused lower-level code only after multiple confirmed consumers and assigned ownership.'},
  ],
  rollback:'Revert only the pilot diff and compatibility re-exports; preserve dirty and authored files; rerun the same source and behavior checks.',
 }:null;
 return {
  schemaVersion:'paos_architecture_advice_v1',authority:'read_only',
  coverage:!applicable?'not_applicable':eligible?'observed':'partial',recommendation,
  revision:evidence?.revision??null,inventoryRevision,findings,legacyExceptions,gaps,
  observed:{pages:foundPages,resolvedImports:resolved.length,crossBoundaryImports:coupling.length,changeFrequency:change,migrationCost:cost,
   surfaceSignals:paths.filter(file=>input.surface==='native'?/\.(?:swift|kt|dart)$/i.test(file)
    :input.surface==='backend'?/\.(?:py|go|rs|java|cs|rb)$/i.test(file):knownSource.test(file)||/\.html?$/i.test(file)).length},
  alternatives,migration,
  nextAction:migration?'Send the proposal to the page owner for a bounded decision':recommendation==='inspect_coverage'?'Resolve the listed inventory and import evidence gaps':
   'Review the existing boundaries with the owner',
 };
}
