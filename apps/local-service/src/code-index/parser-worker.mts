import {parentPort,workerData} from 'node:worker_threads';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import {posix} from 'node:path';
import {createHash} from 'node:crypto';
import {buildLexicalGraph} from './lexical.mts';

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
 for(const result of results){if(!('imports' in result))continue;
  for(const dependency of result.imports){const from=hash(result.relativePath),base=posix.normalize(posix.join(posix.dirname(result.relativePath),dependency.specifier));
   const candidates=dependency.specifier.startsWith('.')&&!base.startsWith('../')?[base,...['.ts','.tsx','.js','.jsx','.mts','.mjs','.cts','.cjs'].flatMap(ext=>[base+ext,base+'/index'+ext])].filter(p=>indexed.has(p)):[];
   const unique=[...new Set(candidates)];let to:string,resolution:'lexical'|'unresolved'='lexical';
   if(unique.length===1)to=hash(unique[0]);else{to=hash(from+'|import|'+dependency.anchor.start);resolution='unresolved';result.nodes.push({id:to,kind:'unresolved',name:'ImportDeclaration',relativePath:result.relativePath,fileId:from,language:workerData.files.find((f:any)=>f.relativePath===result.relativePath).language,scope:'module:0',namespace:'dynamic',anchor:dependency.anchor,reason:unique.length?'ambiguous_module':'module_not_resolved'});}
   result.edges.push({id:hash(from+'|import|'+dependency.anchor.start),type:'import',from,to,anchor:dependency.anchor,resolution});
  }
  delete (result as any).imports;
 }
 parentPort!.postMessage({results,parser:'rolldown-1.2.18-public-utils'});
}catch{parentPort!.postMessage({error:'GRAPH_PARSER_UNAVAILABLE'});}
