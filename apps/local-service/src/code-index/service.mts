import {runGraphParser} from './parser-runner.mts';
import {createHmac,randomBytes,timingSafeEqual} from 'node:crypto';
import {extname} from 'node:path';
import {readFile} from 'node:fs/promises';
import {createRequire} from 'node:module';
import type {LocalStore} from '../storage/local-store.mts';
import {safePersistedText} from '../redaction/persisted.mts';
import type {GraphNode,GraphEdge,GraphCoverage,GraphStatus,GraphEdgeType} from '../../../../packages/contracts/graph/code-graph.ts';
import {assertSourceProject,scanCheckedSources,readCheckedSource,inventoryForProject,digest,graphFail,type SourceProject} from './sources.mts';
import {relatedGraphTasks} from '../impact/service.mts';
import {assertCurrentSourceProject} from '../project-inventory/scope.mts';
import {sanitizeModuleResolverConfig,type ModuleResolverConfig} from './module-resolver.mts';
const languages:Record<string,string>={'.ts':'ts','.mts':'ts','.cts':'ts','.tsx':'tsx','.js':'js','.mjs':'js','.cjs':'js','.jsx':'jsx'};
const extensions=new Set([...Object.keys(languages),'.py','.go','.rs','.java','.cs','.c','.cpp','.rb','.vue','.svelte']);
const limits={files:1000,bytes:8*1024*1024,fileBytes:512*1024,nodes:25000,edges:50000,workerMs:10000,snapshots:8,depth:3,page:100};
const limitations=['lexical_subset_only','no_type_or_runtime_resolution','closed_inventory_module_resolution_only','no_package_exports_or_config_inheritance','import_bindings_do_not_resolve_cross_file_calls','unsupported_languages_not_indexed','jsx_and_class_semantics_partial','task_matches_bounded_first_1000','memory_only_rebuild_after_restart'];
type Manifest={files:{relativePath:string;hash:string;byteSize:number}[];excluded:string[];skipped:{relativePath:string;reason:string}[];inventoryRevision:string;policyVersion:string;parser:string;resolverConfig?:ModuleResolverConfig;configReasons:string[];moduleConfigHash:string|null;config:{limits:typeof limits;languages:typeof languages;extensions:string[]}};
type Snapshot={parserMetrics?:{maxRssKiB:number};projectId:string;revision:string;generation:string;manifest:Manifest;nodes:GraphNode[];edges:GraphEdge[];coverage:GraphCoverage[];inventory:NonNullable<GraphStatus['inventory']>};
function bounded(params:URLSearchParams,key:string,fallback:number,max:number){const text=params.get(key);if(text===null)return fallback;if(!/^\d+$/.test(text))graphFail('GRAPH_QUERY_INVALID');const n=Number(text);if(n<0||n>max)graphFail('GRAPH_QUERY_INVALID');return n;}
export type RebuildOptions={signal?:AbortSignal;expectedInventoryRevision?:string;publicationGuard?:()=>Promise<void>;canPublish?:()=>boolean};
const activeBuild=(options:RebuildOptions)=>{if(options.signal?.aborted||options.canPublish&&!options.canPublish())graphFail('GRAPH_BUILD_CANCELLED');};
export function createCodeIndex(store:LocalStore){
 const snapshots=new Map<string,Snapshot>(),busy=new Set<string>(),secret=randomBytes(32);
 async function project(id:string){const p=await store.project(id);if(!p)graphFail('PROJECT_NOT_FOUND');return p!;}
 async function inventory(p:SourceProject,options:RebuildOptions={}){
  activeBuild(options);
  const scan=await scanCheckedSources(p,extensions,{signal:options.signal}),skipped:{relativePath:string;reason:string}[]=[],planned:{path:string;bytes:number}[]=[];let bytes=0;
  const metadata=new Map(scan.inventory.entries.map(e=>[e.relativePath,e]));
  for(const path of scan.files){const size=metadata.get(path)!.byteSize;
   if(size>limits.fileBytes){skipped.push({relativePath:path,reason:'GRAPH_SOURCE_LIMIT'});continue;}
   if(bytes+size>limits.bytes){skipped.push({relativePath:path,reason:'GRAPH_TOTAL_SOURCE_LIMIT'});continue;}
   bytes+=size;planned.push({path,bytes:size});
  }
  const read=async({path,bytes}:typeof planned[number])=>{activeBuild(options);try{
    const file=await readCheckedSource(p,path,limits.fileBytes);activeBuild(options);
    if(file.byteSize!==bytes)graphFail('GRAPH_SOURCE_DRIFT');return file;
   }catch(error){
    const code=(error as {code?:string}).code;
    // A per-file budget/encoding failure does not discard other safe sources.
    // Authority and revision failures still abort publication for the whole scan.
    if(!['GRAPH_SOURCE_LIMIT','GRAPH_SOURCE_ENCODING','GRAPH_SOURCE_FORBIDDEN','EACCES','EPERM'].includes(code??''))throw error;
    skipped.push({relativePath:path,reason:code!});return undefined;
   }
  };
  // Eight checked handles overlap Windows filesystem latency; metadata reserves
  // the unchanged 8 MiB payload budget before any source bodies are retained.
  let next=0,stopped=false;const loaded:Array<Awaited<ReturnType<typeof read>>>=new Array(planned.length);
  const workers=await Promise.allSettled(Array.from({length:Math.min(8,planned.length)},async()=>{try{for(;;){if(stopped)return;const index=next++;if(index>=planned.length)return;loaded[index]=await read(planned[index]);}}catch(error){stopped=true;throw error;}}));
  const failed=workers.find((result):result is PromiseRejectedResult=>result.status==='rejected');if(failed)throw failed.reason;
  const files=loaded.filter((file):file is NonNullable<typeof file>=>Boolean(file));skipped.sort((a,b)=>a.relativePath.localeCompare(b.relativePath));
  const require=createRequire(new URL('../../../web/package.json',import.meta.url));
  const implementation=await Promise.all([readFile(new URL('./lexical.mts',import.meta.url)),readFile(new URL('./parser-worker.mts',import.meta.url)),readFile(new URL('./module-resolver.mts',import.meta.url)),readFile(new URL('./parser-runner.mts',import.meta.url)),readFile(new URL('../process/child-watchdog.mts',import.meta.url)),readFile(require.resolve('rolldown/utils')),readFile(require.resolve('rolldown/package.json'))]);
  let resolverConfig:ModuleResolverConfig|undefined,configReasons:string[]=[],moduleConfigHash:string|null=null;
  const configEntry=scan.inventory.entries.find(e=>e.relativePath==='tsconfig.json');
  if(configEntry)try{if(!configEntry.access.readable)throw Error('unavailable');const source=await readCheckedSource(p,'tsconfig.json',32768);moduleConfigHash=source.hash;const parsed=JSON.parse(source.text);if(!parsed||typeof parsed!=='object'||Array.isArray(parsed)||parsed.extends!==undefined||parsed.references!==undefined)throw Error('unsupported');const options=parsed.compilerOptions===undefined?{}:parsed.compilerOptions;if(!options||typeof options!=='object'||Array.isArray(options))throw Error('unsupported');const selected=sanitizeModuleResolverConfig({...(options.baseUrl===undefined?{}:{baseUrl:options.baseUrl}),...(options.paths===undefined?{}:{paths:options.paths})});resolverConfig=selected.resolverConfig;configReasons=selected.configReasons;}catch{configReasons=['resolver_config_unavailable_or_unsupported'];}
  return {files,excluded:scan.excluded,exclusions:scan.exclusions,inventory:scan.inventory,inventoryRevision:scan.inventoryRevision,skipped,parser:digest(Buffer.concat(implementation)),resolverConfig,configReasons,moduleConfigHash};
 }
 const manifest=(data:Awaited<ReturnType<typeof inventory>>):Manifest=>({files:data.files.map(({relativePath,hash,byteSize})=>({relativePath,hash,byteSize})),excluded:data.excluded,skipped:data.skipped,inventoryRevision:data.inventoryRevision,policyVersion:data.inventory.policyVersion,parser:'rolldown-public-utils:'+data.parser,resolverConfig:data.resolverConfig,configReasons:data.configReasons,moduleConfigHash:data.moduleConfigHash,config:{limits,languages,extensions:[...extensions]}});
 const revision=(m:Manifest)=>digest(JSON.stringify(m));
 async function state(p:SourceProject,s:Snapshot){try{const observed=await inventoryForProject(p).snapshot(p);await assertCurrentSourceProject(store,p);return p.rootIdentity===s.inventory.rootIdentity&&observed.policyVersion===s.inventory.policyVersion&&observed.revision===s.inventory.revision?'fresh' as const:'stale' as const;}catch(error){if((error as any)?.code==='PROJECT_SCOPE_STALE')throw error;return 'stale' as const;}}
 function touch(id:string,s:Snapshot){snapshots.delete(id);snapshots.set(id,s);return s;}
 function snapshot(id:string,params:URLSearchParams){const s=snapshots.get(id);if(!s)graphFail('GRAPH_INDEX_UNAVAILABLE');const requested=params.get('revision');if(!requested)graphFail('GRAPH_REVISION_REQUIRED');if(requested!==s!.revision)graphFail('GRAPH_REVISION_STALE');return touch(id,s!);}
 function page<T>(items:T[],id:string,revision:string,params:URLSearchParams){const limit=bounded(params,'limit',50,100);if(limit<1||(params.get('cursor')?.length??0)>2048)graphFail('GRAPH_QUERY_INVALID');const filters=[...params].filter(([k])=>k!=='cursor').sort(([a],[b])=>a.localeCompare(b)),binding=digest(JSON.stringify([id,revision,filters]));let offset=0;
  if(params.has('cursor')){try{const [payload,signature,extra]=params.get('cursor')!.split('.'),expected=createHmac('sha256',secret).update(payload).digest('base64url');if(extra||!signature||signature.length!==expected.length||!timingSafeEqual(Buffer.from(signature),Buffer.from(expected)))graphFail('GRAPH_CURSOR_INVALID');const data=JSON.parse(Buffer.from(payload,'base64url').toString());if(data.binding!==binding||!Number.isSafeInteger(data.offset)||data.offset<0)graphFail('GRAPH_CURSOR_INVALID');offset=data.offset;}catch{graphFail('GRAPH_CURSOR_INVALID');}}
  const selected=items.slice(offset,offset+limit);let nextCursor:null|string=null;if(offset+limit<items.length){const payload=Buffer.from(JSON.stringify({binding,offset:offset+limit})).toString('base64url');nextCursor=payload+'.'+createHmac('sha256',secret).update(payload).digest('base64url');}return {items:selected,nextCursor,total:items.length};
 }
 return {
  async status(id:string):Promise<GraphStatus>{const p=await project(id),s=snapshots.get(id);if(!s){await assertSourceProject(p);return {state:'unavailable',limitations};}touch(id,s);return {state:await state(p,s),revision:s.revision,coverage:s.coverage,counts:{files:s.manifest.files.length,nodes:s.nodes.length,edges:s.edges.length},limitations:[...limitations,...s.manifest.configReasons],inventory:s.inventory,...(s.parserMetrics?{observation:{parserMaxRssKiB:s.parserMetrics.maxRssKiB}}:{})};},
  async rebuild(id:string,options:RebuildOptions={}){activeBuild(options);if(busy.has(id))graphFail('GRAPH_BUILD_BUSY');busy.add(id);try{const p=await project(id),data=await inventory(p,options),m=manifest(data),rev=revision(m);activeBuild(options);if(options.expectedInventoryRevision&&options.expectedInventoryRevision!==data.inventoryRevision)graphFail('GRAPH_SOURCE_DRIFT');
   const parsed:any=await runGraphParser({files:data.files.filter(f=>languages[extname(f.relativePath)]).map(f=>({...f,language:languages[extname(f.relativePath)]})),resolverConfig:data.resolverConfig,configReasons:data.configReasons},{signal:options.signal,milliseconds:limits.workerMs});
   if(parsed.error)graphFail(parsed.error);const nodes:GraphNode[]=[],edges:GraphEdge[]=[],coverage:GraphCoverage[]=data.files.filter(f=>!languages[extname(f.relativePath)]).map(f=>({relativePath:f.relativePath,status:'unsupported',reason:'language_not_supported'}));
   for(const r of parsed.results){coverage.push({relativePath:r.relativePath,status:r.status,...(r.reason?{reason:r.reason}:{})});if(r.nodes)nodes.push(...r.nodes);if(r.edges)edges.push(...r.edges);}for(const entry of data.exclusions)coverage.push({...entry,status:'excluded'});for(const entry of data.skipped)coverage.push({...entry,status:'excluded'});
   if(nodes.length>limits.nodes||edges.length>limits.edges)graphFail('GRAPH_BUILD_LIMIT');if(revision(manifest(await inventory(p,options)))!==rev)graphFail('GRAPH_SOURCE_DRIFT');await assertSourceProject(p);await options.publicationGuard?.();await assertCurrentSourceProject(store,p);activeBuild(options);
   // Publish one complete revision only after validating the entire raw manifest again.
   if(!snapshots.has(id)&&snapshots.size>=limits.snapshots)snapshots.delete(snapshots.keys().next().value!);
   touch(id,{projectId:id,revision:rev,parserMetrics:parsed.metrics,generation:randomBytes(16).toString('hex'),manifest:m,nodes,edges,coverage,inventory:{rootIdentity:p.rootIdentity,policyVersion:data.inventory.policyVersion,revision:data.inventoryRevision,coverage:data.inventory.coverage,reasons:data.inventory.reasons,counts:data.inventory.counts}});return this.status(id);
  }finally{busy.delete(id);}},
  async graph(id:string,params:URLSearchParams){const s=snapshot(id,params),p=await project(id),query=(params.get('query')??'').toLowerCase(),mode=params.get('mode')??'all',direction=params.get('direction')??'both';if(query.length>256||!['all','dependencies','symbols'].includes(mode)||!['both','incoming','outgoing'].includes(direction))graphFail('GRAPH_QUERY_INVALID');const depth=bounded(params,'depth',1,3),nodeId=params.get('nodeId'),pathTo=params.get('pathTo'),types=(params.get('edgeTypes')??'').split(',').filter(Boolean);if(types.some(t=>!['import','call','define','read','write','reference'].includes(t)))graphFail('GRAPH_QUERY_INVALID');let available=s.nodes.filter(n=>(mode==='all'||mode==='dependencies'&&n.kind!=='symbol'||mode==='symbols'&&n.kind!=='file')&&(!query||n.name.toLowerCase().includes(query)||n.relativePath.toLowerCase().includes(query)));
   const filtered=s.edges.filter(e=>(mode!=='dependencies'||e.type==='import')&&(!types.length||types.includes(e.type)));let candidateEdges=filtered,path:import('../../../../packages/contracts/graph/code-graph.ts').GraphPage['path'];
   const adjacency=new Map<string,{node:string;edge:GraphEdge}[]>();
   const add=(from:string,node:string,edge:GraphEdge)=>{let entries=adjacency.get(from);if(!entries){entries=[];adjacency.set(from,entries);}entries.push({node,edge});};
   for(const edge of filtered){if(direction!=='incoming')add(edge.from,edge.to,edge);if(direction!=='outgoing')add(edge.to,edge.from,edge);}
   const adjacent=(from:string)=>adjacency.get(from)??[];
   if(nodeId&&!s.nodes.some(n=>n.id===nodeId)||pathTo&&(!nodeId||!s.nodes.some(n=>n.id===pathTo)))graphFail('GRAPH_NODE_NOT_FOUND');
   if(pathTo&&nodeId){const queue=[{node:nodeId,nodes:[nodeId],edges:[] as GraphEdge[]}],visited=new Set([nodeId]);let found:typeof queue[number]|undefined,bounded=false;
    for(let cursor=0;cursor<queue.length;cursor++){const current=queue[cursor];if(current.node===pathTo){found=current;break;}if(current.edges.length>=8){bounded=true;continue;}for(const next of adjacent(current.node)){if(visited.has(next.node))continue;if(visited.size>=1000){bounded=true;break;}visited.add(next.node);queue.push({node:next.node,nodes:[...current.nodes,next.node],edges:[...current.edges,next.edge]});}}
    path={state:found?'found':bounded?'partial':'not_found',nodeIds:found?.nodes??[],...(bounded?{reason:'path_budget_8_hops_1000_nodes'}:{})};const reached=new Set(found?.nodes??[nodeId]);available=available.filter(n=>reached.has(n.id));candidateEdges=found?.edges??[];
   }else if(nodeId){let reached=new Set([nodeId]),front=new Set([nodeId]);for(let i=0;i<depth;i++){const next=new Set<string>();for(const id of front)for(const n of adjacent(id))next.add(n.node);for(const n of next)reached.add(n);front=next;}available=available.filter(n=>reached.has(n.id));candidateEdges=filtered.filter(e=>reached.has(e.from)&&reached.has(e.to));}
   // Page primary nodes independently; hydrate only the off-page endpoints of bounded incident edges.
   const result=page(available,id+'|'+s.generation,s.revision,params),visible=new Set(result.items.map(n=>n.id)),incident=candidateEdges.filter(e=>visible.has(e.from)||visible.has(e.to)),edges=incident.slice(0,100),contextIds=new Set(edges.flatMap(e=>[e.from,e.to]).filter(id=>!visible.has(id))),contextNodes=s.nodes.filter(n=>contextIds.has(n.id));return {revision:s.revision,state:await state(p,s),nodes:result.items,contextNodes,edges,nextCursor:result.nextCursor,partial:result.total>result.items.length||incident.length>edges.length||path?.state==='partial',...(path?{path}:{})};
  },
  async node(id:string,nodeId:string,params:URLSearchParams){const s=snapshot(id,params),node=s.nodes.find(n=>n.id===nodeId);if(!node)graphFail('GRAPH_NODE_NOT_FOUND');return {revision:s.revision,state:await state(await project(id),s),node};},
  async impact(id:string,nodeId:string,params:URLSearchParams){const s=snapshot(id,params),node=s.nodes.find(n=>n.id===nodeId);if(!node)graphFail('GRAPH_NODE_NOT_FOUND');const result=page(s.edges.filter(e=>e.from===nodeId||e.to===nodeId),id+'|impact|'+s.generation+'|'+nodeId,s.revision,params);return {revision:s.revision,state:await state(await project(id),s),node,edges:result.items,nextCursor:result.nextCursor,tasks:await relatedGraphTasks(store,id,node!.relativePath,s.revision,s.manifest.files.find(f=>f.relativePath===node!.relativePath)!.hash),tasksCoverage:'bounded_first_1000'};},
  async source(id:string,params:URLSearchParams){const s=snapshot(id,params),p=await project(id),file=s.nodes.find(n=>n.id===params.get('fileId')&&n.kind==='file');if(!file)graphFail('GRAPH_SOURCE_NOT_FOUND');if(await state(p,s)!=='fresh')graphFail('GRAPH_SOURCE_STALE');const raw=await readCheckedSource(p,file!.relativePath),pin=s.manifest.files.find(f=>f.relativePath===file!.relativePath);if(raw.hash!==pin?.hash)graphFail('GRAPH_SOURCE_STALE');const start=bounded(params,'start',0,raw.text.length),end=bounded(params,'end',Math.min(start+2000,raw.text.length),raw.text.length);if(end<start||end-start>8000)graphFail('GRAPH_QUERY_INVALID');const text=safePersistedText(raw.text),content=text===raw.text?raw.text.slice(start,end):'[redacted source: sensitive content]';await assertCurrentSourceProject(store,p);return {revision:s.revision,fileId:file!.id,relativePath:file!.relativePath,start,end,sha256:raw.hash,content,redacted:text!==raw.text};}
 };
}
