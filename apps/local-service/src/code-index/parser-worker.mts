import {parentPort,workerData as threadedData} from 'node:worker_threads';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {createIndexedModuleResolver,sanitizeModuleResolverConfig} from './module-resolver.mts';
import {buildLexicalGraph} from './lexical.mts';
import {startChildWatchdog} from '../process/child-watchdog.mts';

let workerData=threadedData,watchdog:Awaited<ReturnType<typeof startChildWatchdog>>|undefined;
if(!parentPort){let bytes=0;const chunks:Buffer[]=[];for await(const chunk of process.stdin){bytes+=chunk.length;if(bytes>20*1024*1024)throw Error('GRAPH_BUILD_LIMIT');chunks.push(Buffer.from(chunk));}workerData=JSON.parse(Buffer.concat(chunks).toString('utf8'));watchdog=await startChildWatchdog(workerData.watchdogMilliseconds??11000);}
const post=(value:unknown)=>{if(parentPort)parentPort.postMessage(value);else{const output=JSON.stringify(value);if(Buffer.byteLength(output)>16*1024*1024)throw Error('GRAPH_BUILD_LIMIT');process.stdout.write(output);}};

// Public installed parser entry only; no generated/hashed implementation imports.
try{
 const require=createRequire(new URL('../../../web/package.json',import.meta.url));
 const parser=await import(pathToFileURL(require.resolve('rolldown/utils')).href);
 const results=[];
 for(const file of workerData.files){
  try{const parsed=parser.parseSync(file.relativePath,file.text,{lang:file.language,astType:'ts'});
   results.push(parsed.errors.length?{relativePath:file.relativePath,status:'parse_error'}:{relativePath:file.relativePath,status:'indexed',...buildLexicalGraph(file,parsed.program)});
  }catch{results.push({relativePath:file.relativePath,status:'excluded',reason:'ast_limit_or_unsupported_structure'});}
 }
 const hash=(s:string)=>createHash('sha256').update(s).digest('hex');
 const indexed=new Set(results.filter(r=>r.status==='indexed').map(r=>r.relativePath));
 const sanitized=sanitizeModuleResolverConfig(workerData.resolverConfig);
 const configReasons=[...new Set([...(Array.isArray(workerData.configReasons)?workerData.configReasons.filter((reason:unknown)=>typeof reason==='string').slice(0,64):[]),...sanitized.configReasons])];
 const resolveModule=createIndexedModuleResolver(indexed,sanitized.resolverConfig);
 for(const result of results){if(!('imports' in result))continue;
  for(const dependency of result.imports){const from=hash(result.relativePath),target=resolveModule(result.relativePath,dependency.specifier);
   let to:string,resolution:'lexical'|'unresolved'='lexical';
   if(target.state==='resolved')to=hash(target.relativePath);else{to=hash(from+'|import|'+dependency.anchor.start);resolution='unresolved';result.nodes.push({id:to,kind:'unresolved',name:'ImportDeclaration',relativePath:result.relativePath,fileId:from,language:workerData.files.find((f:any)=>f.relativePath===result.relativePath).language,scope:'module:0',namespace:'dynamic',anchor:dependency.anchor,reason:target.reason});}
   result.edges.push({id:hash(from+'|import|'+dependency.anchor.start),type:'import',from,to,anchor:dependency.anchor,resolution});
  }
  delete (result as any).imports;
 }
 post({results,parser:'rolldown-1.2.18-public-utils-resolver-v1',configReasons,...(!parentPort?{metrics:{maxRssKiB:process.resourceUsage().maxRSS}}:{})});
}catch{post({error:'GRAPH_PARSER_UNAVAILABLE'});}finally{await watchdog?.terminate();}
